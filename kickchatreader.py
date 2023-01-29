import asyncio
import websockets
import json
import sys
from datetime import datetime

async def hello():
    async with websockets.connect("ws://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7") as websocket:
        await websocket.send('{"event":"pusher:subscribe","data":{"auth":"","channel":"chatrooms.77526"}}')
        while True:
            processmsg(await websocket.recv())

def processmsg(msg):
    msg = json.loads(msg)
    if 'ChatMessageSentEvent' in msg['event']:
        data = json.loads(msg['data'])
        message = data['message']['message']
        user = data['user']['username']
        epoch = data['message']['created_at']
        timestamp = datetime.utcfromtimestamp(epoch).strftime("%Y/%m/%d %H:%M")
        if not message:
            if data['message']['action'] == 'subscribe':
                months = data['message']['months_subscribed']
                print("{}  *{:<20} has subscribed and has been for {} month(s)".format(timestamp,user,months))
            elif data['message']['action'] == 'gift':
                count = data['message']['subscriptions_count']
                try:
                    countint = int(count)
                    for x in range(0,countint):
                        print("{}  *{:<20} has gifted a sub".format(timestamp,user))
                except:
                    print("{}  *{:<20} has gifted {} subs".format(timestamp,user,count))
            return
        print("{}  {:<20} {}".format(timestamp,user,message))

asyncio.run(hello())
while True:
    try:
        asyncio.run(hello())
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass
