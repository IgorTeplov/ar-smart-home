import asyncio
import websockets
import time
import json

uri = "ws://localhost:8000/ws/arduino/"

async def get_data_from_arduino():
	
	async with websockets.connect(uri, ping_interval=None) as websocket:
		await websocket.send(json.dumps({"command":"connect", "key":'secretkey'}))
		answer = await websocket.recv()
		print(answer)
		while True:
			await websocket.send(json.dumps({"command":"send", "data":str(time.time())}))
			print(await websocket.recv())
			await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(get_data_from_arduino())