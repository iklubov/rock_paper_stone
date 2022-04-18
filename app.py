import asyncio
import json
import logging

import websockets

import schemas
from database import write_offer, get_offers, clear_db, accept_offer, start_battle
from utils import pathhandler, get_path, KNBError

async def handler(websocket, path):
    async for message in websocket:
        path_handler = get_path(path)
        print('message', path, path_handler, message)
        try:
            result = await path_handler(websocket, message)
        except KNBError as error:
            result = str(error)
        except BaseException as error:
            result = f'BaseException {str(error)}'
        print(f'result{result}')
        logging.log(logging.INFO, f'path {path} message {message} result {result}')
        await websocket.send(result)

@pathhandler('/clear')
async def clear_battles(websocket, message):
    clear_db()
    return json.dumps('db cleared')

@pathhandler('/battles_create', schemas.create_battle)
async def battles_create(websocket, message):
    messageobj = json.loads(message)
    print('battles create', message, messageobj)
    offerjson = write_offer(**messageobj)
    return offerjson

@pathhandler('/battles_list')
async def battles_list(websocket, message):
    battles_list = get_offers()
    return battles_list

#todo
@pathhandler('/battles_accept', schemas.accept_battle)
async def battle_accept(websocket, message):
    messageobj = json.loads(message)
    result = accept_offer(**messageobj)
    return result

#todo
@pathhandler('/battles_start', schemas.start_battle)
async def battle_start(websocket, message):
    messageobj = json.loads(message)
    result = start_battle(**messageobj)
    return result

#todo
@pathhandler('/battles_move', schemas.battle_move)
async def battles_move(websocket, message):
#     На эндпоинт battles_move передаются JSON параметры {userId: 0, battleId: 1, choice: 0, round: 0}, ход записывается в лог битвы.
# Как только оба игрока сделали выбор симулируем камень ножницы бумагу и записываем результат в объект битвы в массив логов с номером раунда и игрока который выиграл. Обоим игрокам отправляется battles_round c выборами игроков и результатом.


    battles_list = get_offers()
    return battles_list

async def main():
    clear_db()
    async with websockets.serve(handler, '', 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())