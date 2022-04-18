import asyncio
import json
import logging
import sys
from collections import defaultdict
from os import getenv

import itertools
from redis.client import Redis

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
    db = get_db()
    db.flushall()
    db.close()

def write_offer(player_id, ntf_id):
    db = get_db()
    if not db.get(f'players:{player_id}_{ntf_id}'):
        db.set(f'players:{player_id}_{ntf_id}', True)
        offer_id = next(offerIdGen)
        db.hset('offers', offer_id, json.dumps([{'player_id':player_id, 'ntf_id':ntf_id}]))
        jsonobj = json.dumps({'player_id':player_id, 'ntf_id':ntf_id, 'offer_id':offer_id})
    else:
        errorstr = f' offer with player_id {player_id} and nft_id {ntf_id} already exists'
        logging.log(logging.ERROR, errorstr)
        jsonobj = json.dumps({'error':errorstr})
    db.close()
    return jsonobj


def get_offers():
    db = get_db()
    offers = db.hgetall('offers')
    print(offers)
    result = json.dumps([json.loads(offer) for offer in offers.values()])
    db.close()
    return result

#todo
def accept_offer(offer_id, player_id, ntf_id):
    db = get_db()
    offer = db.hget('offers', offer_id)
    offer_list = json.loads(offer)
    if len(offer_list) != 1:
        pass
    elif offer_list[0]['player_id'] == player_id:
        pass
    else:
        accept_id = next(acceptIdGen)
        offer_list.append({'player_id':player_id, 'ntf_id':ntf_id})
        db.hset('offers', offer_id, json.dumps(offer_list))
        db.hset('accepts', accept_id, offer_id)

    result = json.dumps({'offer_id': offer_id, 'accept_id': accept_id})
    db.close()
    return result

#todo
def start_battle(offer_id, accept_id):
    db = get_db()
    # what for
    offer_id = db.get('accepts', accept_id)
    battle_id = next(battleIdGen)
    db.hset('battles', battle_id, json.dumps([]))
    result = json.dumps({'battle_id': battle_id})
    db.close()
    return result

# todo
def move_battle(battle_id, player_id, choice_id, round_id):
    db = get_db()
    # what for
    #offer_id = db.get('accepts', accept_id)
    battle_id = next(battleIdGen)
    db.hset('battles', offer_id, battle_id)
    result = json.dumps({'battle_id': battle_id})
    db.close()
    return result


# clear_db()
# for arena_id in range(10):
#     print(write_offer(0, arena_id))
# print(get_offers())

