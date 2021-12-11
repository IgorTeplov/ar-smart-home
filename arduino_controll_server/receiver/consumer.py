import json
import sys
import time

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import User, Log


class Consumer(AsyncWebsocketConsumer):
    key = None
    device = None
    user = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.key is not None:
            await self.channel_layer.group_discard(
                f'{self.key}_{self.device}',
                self.channel_name
            )
            if self.device == 'rpi':
                await self.log({'who':self.user, 'event':'DISCONNECT from RPI'})
                await self.channel_layer.group_send(
                    f'{self.key}_interface',
                    {
                        'type': 'send_status_interface',
                        'target': 'sconnectrpi',
                        'data': False
                    }
                )
            else:
                await self.log({'who':self.user, 'event':'DISCONNECT from INTERFACE'})

    async def receive(self, text_data):
        jdata = json.loads(text_data)

        sys.stdout.write(text_data)
        sys.stdout.write('\n')
        if 'command' in jdata.keys():
            command = jdata.get('command', None)
            if command is not None:
                if command == "connect" and 'key' in jdata.keys():
                    self.user = await self.get_user({'token':jdata['key']})
                    if self.user != None:
                        await self.log({'who':self.user, 'event':'CONNECT to INTERFACE'})
                        self.key = self.user.group
                        self.device = 'interface'
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
                        if f'{self.key}_rpi' in self.channel_layer.groups.keys():
                            await self.channel_layer.group_send(
                                f'{self.key}_interface',
                                {
                                    'type': 'send_status_interface',
                                    'target': 'sconnectrpi',
                                    'data': True
                                }
                            )
                            await self.channel_layer.group_send(
                                f'{self.key}_rpi',
                                {
                                    'type': 'send_to_rpi',
                                    'data': '4'
                                }
                            )
                elif command == "connectrpi" and 'key' in jdata.keys():
                    self.user = await self.get_user({'token':jdata['key']})
                    if self.user != None:
                        await self.log({'who':self.user, 'event':'CONNECT to RPI'})
                        self.key = self.user.group
                        self.device = 'rpi'
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
                        await self.channel_layer.group_send(
                            f'{self.key}_rpi',
                            {
                                'type': 'send_to_rpi',
                                'data': '4'
                            }
                        )
                elif command == 'send_to_rpi' and 'data' in jdata.keys():
                    if self.key != None:
                        await self.channel_layer.group_send(
                            f'{self.key}_rpi',
                            {
                                'type': 'send_to_rpi',
                                'data': jdata['data']
                            }
                        )
                elif command == 'send' and 'data' in jdata.keys():
                    if self.key != None:
                        if f'{self.key}_interface' in self.channel_layer.groups.keys():
                            await self.channel_layer.group_send(
                                f'{self.key}_interface',
                                {
                                    'type': 'send_status_interface',
                                    'target': 'usercontroll',
                                    'data': jdata['data']
                                }
                            )

    @sync_to_async
    def get_user(self, auth_obj):
        if User.objects.filter(**auth_obj):
            return User.objects.get(**auth_obj)
        return None


    @sync_to_async
    def log(self, obj):
        log = Log(**obj)
        log.save()

    async def send_status_interface(self, event):
        await self.send(text_data=json.dumps({"target":event["target"], "data":event["data"]}))

    async def send_status_rpi(self, event):
        await self.send(text_data=event["data"])

    async def send_to_rpi(self, event):
        if event["data"] == '1':
            self.log({'who': self.user, 'event':'OPEN WINDOW'})
        elif event["data"] == '2':
            self.log({'who': self.user, 'event':'CLOSE WINDOW'})
        elif event["data"] == '3':
            self.log({'who': self.user, 'event':'CHANGE MOD'})
        await self.send(text_data=event["data"])