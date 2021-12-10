import asyncio
import websockets
import time
import json
import serial

uart = serial.Serial('/dev/ttyS0', 9600, timeout=None)

uri = "ws://192.168.31.110:8000/ws/arduino/"


async def get_data_from_user():
	async with websockets.connect(uri, ping_interval=None) as websocket:
		await websocket.send(
			json.dumps(
				{"command":"connectrpi", "key":input('Key: ')},
			),
		)
		answer = await websocket.recv()
		print(answer)
		while True:
			data = json.loads(await websocket.recv())
			command = str(data).encode()
			uart.write(command)

asyncio.run(get_data_from_user())
