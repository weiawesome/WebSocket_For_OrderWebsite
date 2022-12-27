import asyncio
import json

import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def Boss(data):
    print('message received with ', data)
    data=json.loads(data)
    print(type(data))

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('https://websocket-for-orderwebsite.onrender.com')
    await sio.emit('Boss','Me')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())