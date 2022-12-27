import json
import eventlet as eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
Bosses=[]
Clients=[]
Orders=[]
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    Clients.append(sid)
    Json={'Boss':len(Bosses)!=0}
    Json=json.dumps(Json)
    sio.emit('Boss', Json)
@sio.event
def Boss(sid, data):
    Clients.remove(sid)
    Bosses.append(sid)
    Json={'Boss':len(Bosses)!=0}
    Json=json.dumps(Json)
    for i in Clients:
        sio.emit('Boss',Json,to=i)
    Json = {'Orders': Orders}
    Json = json.dumps(Json)
    for i in Bosses:
        sio.emit('Orders', Json, to=i)

@sio.event
def SentOrder(sid,data):
    print('Order',data)
    order=(json.loads(data))
    for i in order:
        Orders.append(i)
    Json={'Orders':Orders}
    Json=json.dumps(Json)
    for i in Bosses:
        sio.emit('Orders',Json,to=i)

@sio.event
def disconnect(sid):
    if(sid in Bosses):
        Bosses.remove(sid)
        Json={'Boss':len(Bosses)!=0}
        Json=json.dumps(Json)
        for i in Clients:
            sio.emit('Boss', Json,to=i)
    print('disconnect ', sid)

# if __name__ == '__main__':
#     eventlet.wsgi.server(eventlet.listen(('', 8000)), app)