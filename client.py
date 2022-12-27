import asyncio
import json

import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection')

@sio.event
async def Boss(data):
    data=json.loads(data)
    print('Boss', data)
@sio.event
async def Orders(data):
    print('Orders',json.loads(data))

@sio.event
async def disconnect():
    print('disconnected')

async def main():
    # await sio.connect('https://websocket-for-orderwebsite.onrender.com')
    await sio.connect('http://localhost:8000')
    await sio.emit('Boss','Me')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())