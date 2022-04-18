import asyncio
import json
import logging

import websockets

import schemas
from database import write_offer, get_offers, clear_db, accept_offer, start_battle, move_battle
from utils import pathhandler, get_path, KNBError

async def handler(websocket, path):
    async for message in websocket:
        path_handler = get_path(path)
        #print('message', path, path_handler, message)
        try:
            result = await path_handler(websocket, message)
        except KNBError as error:
            result = json.dumps({'error': str(error)})
        #print(f'result{result}')
        logging.log(logging.INFO, f'path {path} message {message} result {result}')
        await websocket.send(result)

@pathhandler('/clear')
async def clear_battles(websocket, message):
    clear_db()
    return json.dumps('db cleared')

@pathhandler('/battles_create', schemas.create_battle)
async def battles_create(websocket, message):
    messageobj = json.loads(message)
    offerjson = write_offer(**messageobj)
    return offerjson

@pathhandler('/battles_list')
async def battles_list(websocket, message):
    battles_list = get_offers()
    return battles_list

@pathhandler('/battles_accept', schemas.accept_battle)
async def battle_accept(websocket, message):
    messageobj = json.loads(message)
    result = accept_offer(**messageobj)
    return result

@pathhandler('/battles_start', schemas.start_battle)
async def battle_start(websocket, message):
    messageobj = json.loads(message)
    result = start_battle(**messageobj)
    return result

@pathhandler('/battles_move', schemas.battle_move)
async def battles_move(websocket, message):
    messageobj = json.loads(message)
    result = move_battle(**messageobj)
    return result

async def main():
    clear_db()
    async with websockets.serve(handler, '', 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())