import asyncio
import json

import websockets

async def clear():
    async with websockets.connect("ws://localhost:8001/clear") as websocket:
        await websocket.send('')
        result = await websocket.recv()
        return result

async def create_battle():
    async with websockets.connect("ws://localhost:8001/battles_create") as websocket:
        data = {
                    "arena_id": 3,
                    "player_id": 0,
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
    create_battle_result = await create_battle()
    battles_list = await get_battle_list()
    print(clear_result)
    print(create_battle_result)
    print(battles_list)

asyncio.run(test_case())