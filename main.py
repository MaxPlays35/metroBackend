import asyncio
import json
from typing import Union

from fastapi import FastAPI
from fastapi_socketio import SocketManager
from metro_model import Metro

app = FastAPI()
socket_manager = SocketManager(app=app)

metro: Union[Metro, None] = None


@socket_manager.on('connect')
async def connect(sid, *args, **kwargs):
    print(f'Connected: {sid}')


@socket_manager.on('start')
async def start(sid, *args, **kwargs):
    global metro
    ar = args[0]
    trains, speed = ar["trains"], ar["speed"]
    metro = Metro(trains, speed, socket_manager)
    await metro.init()


@socket_manager.on('disconnect')
async def disconnect(sid, *args, **kwargs):
    print(f'Disconnected: {sid}')
    global metro
    # if metro != None:
    #     metro.stop()
