import json
from channels.generic.websocket import AsyncWebsocketConsumer

import threading
import sys
import time

class Consumer(AsyncWebsocketConsumer):
    key = None
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(self)
        if self.key is not None:
            await self.channel_layer.group_discard(
                self.key,
                self.channel_name
            )

    async def receive(self, text_data):
        jdata = json.loads(text_data)

        print(jdata)
        if 'command' in jdata.keys():
            command = jdata.get('command', None)
            if command is not None:
                if command == "connect" and 'key' in jdata.keys():
                    self.key = jdata['key']
                    await self.channel_layer.group_add(
                        self.key,
                        self.channel_name
                    )
                    await self.send(text_data=json.dumps({"status":1}))
                elif command == "send" and "data" in jdata.keys():
                    await self.channel_layer.group_send(
                        self.key,
                        {
                            'type': 'receiver',
                            'data': jdata["data"]
                        }
                    )


        # text_data_jsojson.loads(text_data)n = json.loads(text_data)
        # command = text_data_json['command']

    async def receiver(self, event):
        await self.send(text_data=json.dumps({"data":event['data']}))


    # async def chat_message(self, event):
    #     command = event['command']
    #     if command == 'start':
    #         self.start_listening()
    #     elif command == 'stop':
    #         self.stop_listening()
    #     elif command == 'send':
    #         await self.channel_layer.group_send(
    #             'broadcast',
    #             {
    #                 'data': event['data']
    #             }
    #         )

    # async def receiver(self):
    #     while True:
    #         await self.send(text_data=str(time.time()))
    #         time.sleep(0.000001)
    #         if self.killed:
    #             break

    # def start_listening(self):
    #     self.killed = False
    #     self.listener = threading.Thread(target=self.receiver)
    #     self.listener.setDaemon(True)
    #     self.listener.start()

    # def stop_listening(self):
    #     if self.listener is not None:
    #         self.killed = True
    #         self.listener = None
