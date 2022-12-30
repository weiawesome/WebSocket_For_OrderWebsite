import asyncio
import json

import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection')
    await sio.emit('Boss', 'Me')
    print('ya')

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
    while(True):
        a=input()
        if(a=='q'):
            break
        elif(a=='g'):
            print('Number: ',end='')
            b=int(input())
            await sio.emit('TakeOrder',json.dumps({'CustomerId':b}))
        await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())