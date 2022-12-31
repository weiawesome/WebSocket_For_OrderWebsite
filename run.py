import datetime
import json
import os

# import eventlet as eventlet
import pandas as pd
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
Bosses=[]
Clients=[]

def getCustomerId():
    try:
        df=pd.read_csv('./Datas/IdOfOrders/{} Id.csv'.format(datetime.date.today()))
        return max(df['CustomerId'])+1
    except:
        return 0
def getTempOrders():
    try:
        df=pd.read_csv('./Datas/TempOrders.csv')
        return df
    except:
        return pd.DataFrame()
def TodayCheck():
    Time=open('./Datas/Date.txt','r+')
    if(str(datetime.date.today())!=Time.read()):
        if os.path.exists('./Datas/TempOrders.csv'):
            os.remove('./Datas/TempOrders.csv')
            file=open('./Datas/TempOrders.csv', 'a+')
            file.close()
            file = open('./Datas/TempId.csv', 'a+')
            file.close()
            file=open('./Datas/Orders/{} Orders.csv'.format(datetime.date.today()),'a+')
            file.close()
            file=open('./Datas/IdOfOrders/{} Id.csv'.format(datetime.date.today()),'a+')
            file.close()
        else:
            file=open('./Datas/TempOrders.csv', 'a+')
            file.close()
            file = open('./Datas/TempId.csv', 'a+')
            file.close()
            file=open('./Datas/Orders/{} Orders.csv'.format(datetime.date.today()), 'a+')
            file.close()
            file=open('./Datas/IdOfOrders/{} Id.csv'.format(datetime.date.today()), 'a+')
            file.close()
    Time.close()
    Time=open('./Datas/Date.txt','w+')
    Time.write(str(datetime.date.today()))
    Time.close()
def concatdf(df1,df2):
    return pd.concat([df1,df2],axis=0,ignore_index=True)
def mergerId(df,Id):
    tmp=pd.DataFrame({'CustomerId':[Id]*len(df)})
    return pd.concat([df,tmp],axis=1)

def getTime():
    return datetime.datetime.now().strftime('%H:%M')
def saveFiles(df,Id,Time):
    try:
        tmp=pd.read_csv('./Datas/Orders/{} Orders.csv'.format(datetime.date.today()))
    except:
        tmp=pd.DataFrame()
    df=concatdf(tmp,df)
    df.to_csv('./Datas/Orders/{} Orders.csv'.format(datetime.date.today()),index=0)
    try:
        tmp = pd.read_csv('./Datas/IdOfOrders/{} Id.csv'.format(datetime.date.today()))
    except:
        tmp=pd.DataFrame()
    dfId=pd.DataFrame({'Time':[Time],'CustomerId':[Id]})
    dfId=concatdf(tmp,dfId)
    dfId.to_csv('./Datas/IdOfOrders/{} Id.csv'.format(datetime.date.today()),index=0)

def saveTempFiles(df,id,Time):
    df.to_csv('./Datas/TempOrders.csv',index=0)
    try:
        tmp=pd.read_csv('./Datas/TempId.csv')
    except:
        tmp=pd.DataFrame()
    tmpdf=pd.DataFrame({'Time':[Time],'CustomerId':[id]})
    tmp=concatdf(tmp,tmpdf)
    tmp.to_csv('./Datas/TempId.csv',index=0)
def GetResultToBosses():
    try:
        Orders = pd.read_csv('./Datas/TempOrders.csv')
        IDs = pd.read_csv('./Datas/TempId.csv')
        tmp = {}
        Result = []
        for index, i in enumerate(IDs['CustomerId']):
            tmp[i] = index
            Result.append([])
        for i in range(len(Orders)):
            Result[tmp[Orders.iloc[i]['CustomerId']]].append(dict(Orders.iloc[i]))
        Json = {'Orders': Result}
        Json = json.dumps(Json,default=int)
    except:
        Json= {'Orders': []}
        Json = json.dumps(Json, default=int)
    Json=Json.replace('NaN','""')
    return Json
@sio.event
def connect(sid, environ):
    TodayCheck()
    print('connect ', sid)
    Clients.append(sid)
    Json={'Boss':len(Bosses)!=0}
    Json=json.dumps(Json)
    sio.emit('Boss', Json)
@sio.event
def TakeOrder(sid, data):
    if sid in Bosses:
        data=json.loads(data)
        tmp=pd.read_csv('./Datas/TempId.csv')
        tmp=tmp.loc[tmp['CustomerId']!=data['CustomerId']]
        tmp.to_csv('./Datas/TempId.csv',index=0)

        tmp=pd.read_csv('./Datas/TempOrders.csv')
        tmp=tmp.loc[tmp['CustomerId']!=data['CustomerId']]
        tmp.to_csv('./Datas/TempOrders.csv',index=0)
        ResultJson=GetResultToBosses()
        for i in Bosses:
            sio.emit('Orders',ResultJson, to=i)
    else:
        print(sid,' not Boss!')

@sio.event
def Boss(sid, data):
    Clients.remove(sid)
    Bosses.append(sid)
    Json={'Boss':len(Bosses)!=0}
    Json=json.dumps(Json)
    for i in Clients:
        sio.emit('Boss',Json,to=i)

    ResultJson=GetResultToBosses()
    for i in Bosses:
        sio.emit('Orders',ResultJson, to=i)

@sio.event
def SentOrder(sid,data):
    print('Order',data)
    t = getTime()
    df=pd.DataFrame(json.loads(data)['Orders'])
    Id=getCustomerId()
    df=mergerId(df,Id)
    saveFiles(df,Id,t)
    tmpdf=getTempOrders()
    df=concatdf(df,tmpdf)
    print(df)
    saveTempFiles(df,Id,t)

    ResultJson=GetResultToBosses()
    for i in Bosses:
        sio.emit('Orders',ResultJson,to=i)

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