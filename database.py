import json
import sys
from os import getenv
from random import randint

from redis.client import Redis

from utils import KNBError, Choices

offerIdGen = iter(range(sys.maxsize))
acceptIdGen = iter(range(sys.maxsize))
battleIdGen = iter(range(sys.maxsize))

def get_db():
    password = getenv('REDIS_PASSWORD', 'redispwd')
    isLocal = getenv('IS_LOCAL', True)
    hostName = 'localhost' if isLocal == True else 'db'
    redis = Redis(
        host=hostName,
        port= '6379', password=password)
    return redis

def clear_db():
    global offerIdGen, acceptIdGen, battleIdGen
    db = get_db()
    db.flushall()
    offerIdGen = iter(range(sys.maxsize))
    acceptIdGen = iter(range(sys.maxsize))
    battleIdGen = iter(range(sys.maxsize))
    db.close()

def write_offer(player_id, ntf_id):
    db = get_db()
    key = f'players:{player_id}_{ntf_id}'
    if db.get(key):
        db.close()
        raise KNBError(f' offer with player_id {player_id} and nft_id {ntf_id} already exists')

    db.set(key, 1)
    offer_id = next(offerIdGen)
    db.hset('offers', offer_id, json.dumps([{'player_id':player_id, 'ntf_id':ntf_id}]))
    result = json.dumps({'player_id':player_id, 'ntf_id':ntf_id, 'offer_id':offer_id})
    db.close()
    return result

def get_offers():
    db = get_db()
    offers = db.hgetall('offers')
    offer_dicts = []
    for offer_id, offer_b in offers.items():
        offer_loaded_list = json.loads(offer_b)
        for offer_loaded in offer_loaded_list:
            offer_loaded['offer_id'] = int(offer_id)
        offer_dicts.append(offer_loaded_list)
    result = json.dumps(offer_dicts)
    db.close()
    return result

def accept_offer(offer_id, player_id, ntf_id):
    db = get_db()
    offer = db.hget('offers', offer_id)
    if offer is None:
        db.close()
        raise KNBError(f' offer with offer_id {offer_id} doesnt exist')
    offer_list = json.loads(offer)
    if len(offer_list) != 1:
        db.close()
        raise KNBError(f' offer with offer_id {offer_id} has more than 1 accepts')
    elif offer_list[0]['player_id'] == player_id:
        db.close()
        raise KNBError(f' offer with offer_id {offer_id} and player_id {player_id} has sent than 1 times')

    accept_id = next(acceptIdGen)
    offer_list.append({'player_id':player_id, 'ntf_id':ntf_id})
    db.hset('offers', offer_id, json.dumps(offer_list))
    db.hset('accepts', accept_id, offer_id)

    result = json.dumps({'offer_id': offer_id, 'accept_id': accept_id})
    db.close()
    return result

def start_battle(offer_id, accept_id):
    db = get_db()
    offer_id_b = db.hget('accepts', accept_id)
    if offer_id_b is None or int(offer_id_b) != offer_id:
        db.close()
        raise KNBError(f'Offer_id {offer_id} whith accept_id {accept_id} does not exist')
    offer_b = db.hget('offers', offer_id)
    if offer_b is None:
        db.close()
        raise KNBError(f'Offer_id {offer_id} does not exist')

    offer_list = json.loads(offer_b)
    players_ids = (offer['player_id'] for offer in offer_list)

    battle_id = next(battleIdGen)
    db.hset('battles', battle_id, json.dumps({'moves':[], 'rounds':[], 'players': {pid:100 for pid in players_ids}}))
    result = json.dumps({'battle_id': battle_id})
    db.close()
    return result

def move_battle(battle_id, player_id, choice_id, round_id):
    move_obj = {
        'battle_id': battle_id,
        'player_id': player_id,
        'choice_id': choice_id,
        'round_id' : round_id
    }
    db = get_db()
    battle_obj_b = db.hget('battles', battle_id)
    if battle_obj_b is None:
        db.close()
        raise KNBError(f'battle with battle_id {battle_id} does not exist')
    if choice_id not in Choices.ALL:
        db.close()
        raise KNBError(f'choice with {choice_id} does not exist')
    battle_obj = json.loads(battle_obj_b)
    current_moves = battle_obj['moves']
    players_ids = (int(pid) for pid in battle_obj['players'].keys())
    if player_id not in players_ids:
        db.close()
        raise KNBError(f'player with {player_id} does not exist in battle {battle_id}')

    result = {}

    if len(current_moves) != 0:
        last_move = current_moves[-1]
        # start new round - do nothing
        if len(current_moves) % 2 == 1:
            if last_move['round_id'] != round_id:
                db.close()
                raise KNBError(f'Another round {round_id} after not finished round{last_move["round_id"]}')
            if last_move['player_id'] == player_id:
                db.close()
                raise KNBError(f'Second move with the same player_id {player_id}')
        # second player answered - process round results
        else:
            if last_move['round_id'] == round_id:
                db.close()
                raise KNBError(f'The same round {round_id} after finished round{last_move["round_id"]}')

            win_index = Choices.who_wins(last_move['choice_id'], choice_id)
            winner_id, looser_id = -1, -1
            if win_index != 0:
                points_to_delete = randint(10, 20)
                looser_id = player_id if win_index == 2 else last_move['player_id']
                winner_id = player_id if win_index == 1 else last_move['player_id']
                current_player_points = battle_obj['players'][str(looser_id)]
                new_player_points = current_player_points - points_to_delete
                battle_obj['players'][str(looser_id)] = new_player_points
            # round finished
            battle_obj['rounds'].append({'round_id':round_id, 'winner_id':winner_id})
            result = {
                'round': {'round_id':round_id, 'winner_id':winner_id, 'current_points': battle_obj['players']},
            }

    current_moves.append(move_obj)
    battle_finished = any(pp <= 0 for pp in battle_obj['players'].values())
    if battle_finished:
        result['battle_result'] = {'battle_id':battle_id, 'result': battle_obj['players']}

    db.hset('battles', battle_id, json.dumps(battle_obj))
    db.close()
    return json.dumps(result)



