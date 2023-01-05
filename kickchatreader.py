#!/usr/bin/env python3
import asyncio
import websockets
import json
from datetime import datetime



# to find chatroom id go to https://kick.com/api/v1/{USERNAME}/chatroom
# look for "chatroom":{"id":NUMBERS,

async def main():
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
        print("{}  {:<20} {}".format(timestamp,user,message))

asyncio.run(main())
