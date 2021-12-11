import asyncio
import websockets
import time
import json
import serial
import sys

uart = serial.Serial('/dev/ttyS0', 9600, timeout=None)

uri = "ws://192.168.31.110:8000/ws/arduino/"

async def get_data_from_user():
	async with websockets.connect(uri, ping_interval=None) as websocket:
		await websocket.send(json.dumps(
			{"command":"connectrpi", "key":input('Your TOKEN: ')},
		))
		answer = await websocket.recv()
		sys.stdout.write(answer)
		sys.stdout.write('\n')
		while True:
			data = json.loads(await websocket.recv())
			command = str(data).encode()
			uart.write(command)
			if command == b'4':
				ans = uart.readline().decode('utf-8')
				await websocket.send(json.dumps(
					{'command':'send', 'data': ans},
				))

asyncio.run(get_data_from_user())
