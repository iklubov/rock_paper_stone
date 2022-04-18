import asyncio
import json
from random import randint

import websockets

async def clear():
    async with websockets.connect("ws://localhost:8001/clear") as websocket:
        await websocket.send('')
        result = await websocket.recv()
        return result

async def create_battle(ntr_id, player_id):
    async with websockets.connect("ws://localhost:8001/battles_create") as websocket:
        data = {
                    "ntf_id": ntr_id,
                    "player_id": player_id,
                }
        await websocket.send(json.dumps(data))
        result = await websocket.recv()
        return result

async def get_battle_list():
    async with websockets.connect("ws://localhost:8001/battles_list") as websocket:
        await websocket.send('')
        result = await websocket.recv()
        return result

async def accept_battle(offer_id, ntf_id, player_id):
    async with websockets.connect("ws://localhost:8001/battles_accept") as websocket:
        data = {
            "offer_id": offer_id,
            "ntf_id": ntf_id,
            "player_id": player_id,
        }
        await websocket.send(json.dumps(data))
        result = await websocket.recv()
        return result

async def start_battle(accept_id, offer_id):
    async with websockets.connect("ws://localhost:8001/battles_start") as websocket:
        data = {
            "offer_id": offer_id,
            "accept_id": accept_id
        }
        await websocket.send(json.dumps(data))
        result = await websocket.recv()
        return result

async def move_battle(battle_id, player_id, choice_id, round_id):
    async with websockets.connect("ws://localhost:8001/battles_move") as websocket:
        data = {
            "battle_id": battle_id,
            "player_id": player_id,
            "choice_id": choice_id,
            "round_id": round_id,
        }
        await websocket.send(json.dumps(data))
        result = await websocket.recv()
        return result

async def test_double_create():
    clear_result = await clear()
    create_battle_result1 = await create_battle(0,0)
    create_battle_result2 = await create_battle(0,0)
    battles_list1 = await get_battle_list()
    print(clear_result)
    print(create_battle_result1)
    print(create_battle_result2)
    print(battles_list1)

async def test_case():
    clear_result = await clear()
    create_battle_result1 = await create_battle(0,0)
    create_battle_result2 = await create_battle(1,1)
    battles_list1 = await get_battle_list()
    create_battle_result3 = await create_battle(1,0)
    create_battle_result4 = await create_battle(0,1)
    battles_list2 = await get_battle_list()
    print(clear_result)
    print(create_battle_result1)
    print(create_battle_result2)
    print(create_battle_result3)
    print(create_battle_result4)
    print(battles_list1)
    print(battles_list2)

    accept_battle_result1 = await accept_battle(0, 1, 1)
    accept_battle_result2 = await accept_battle(0, 1, 1)
    battles_list3 = await get_battle_list()
    print(accept_battle_result1)
    print(accept_battle_result2)
    print(battles_list3)

    start_battle_result = await start_battle(0, 0)
    print(start_battle_result)
    battle_finished = False
    round_number = 0
    while not battle_finished:
        move_result_1 = await move_battle(0, 0, randint(0,2), round_number)
        move_result_2 = await move_battle(0, 1, randint(0,2), round_number)
        print(move_result_1)
        print(move_result_2)
        battle_finished = 'battle_result' in move_result_2 or 'error' in move_result_1 or 'error' in move_result_2
        round_number += 1


asyncio.run(test_case())
#asyncio.run(test_double_create())


