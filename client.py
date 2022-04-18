import asyncio
import json

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

asyncio.run(test_case())