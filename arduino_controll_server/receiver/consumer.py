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
                        f'{self.key}_interface',
                        self.channel_name
                    )
                    await self.channel_layer.group_send(
                        f'{self.key}_interface',
                        {
                            'type': 'send_status_interface',
                            'target': 'sconnect',
                            'data': True
                        }
                    )
                elif command == "connectrpi" and 'key' in jdata.keys():
                    self.key = jdata['key']
                    await self.channel_layer.group_add(
                        f'{self.key}_rpi',
                        self.channel_name
                    )
                    await self.channel_layer.group_send(
                        f'{self.key}_rpi',
                        {
                            'type': 'send_status_rpi',
                            'data': 'Connected!'
                        }
                    )
                    await self.channel_layer.group_send(
                        f'{self.key}_interface',
                        {
                            'type': 'send_status_interface',
                            'target': 'sconnectrpi',
                            'data': True
                        }
                    )
                elif command == 'send_to_rpi' and 'data' in jdata.keys() :
                    await self.channel_layer.group_send(
                        f'{self.key}_rpi',
                        {
                            'type': 'send_to_rpi',
                            'data': jdata['data']
                        }
                    )

    async def send_status_interface(self, event):
        await self.send(text_data=json.dumps({"target":event["target"], "data":event["data"]}))

    async def send_status_rpi(self, event):
        await self.send(text_data=event["data"])

    async def send_to_rpi(self, event):
        await self.send(text_data=event["data"])
