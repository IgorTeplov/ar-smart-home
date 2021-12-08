import serial
import time
import os
import requests

def send(text):
	print('send text...')
	TOKEN = "1851687350:AAEzbGAle4rncIcbarvViu2hutLPWRQCm-U"
	chat = 631456992
	r = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(TOKEN), {
			'chat_id':chat,
			'text':text
	})
	print(r.text)

GLOBAL_COUNT = 0
GLOBAL_MAX = 1500

print('start data stream from uart...')
def connect_and_read():
	global GLOBAL_COUNT, GLOBAL_MAX
	try:
		uart = serial.Serial('/dev/ttyS0', 9600, timeout=None)
	except:
		print('Got reconfigurate port')
		time.sleep(5)
		return

	while True:
		if GLOBAL_COUNT == GLOBAL_MAX:
			GLOBAL_COUNT = 0
			time.sleep(2)
		else:
			GLOBAL_COUNT += 1
		if not uart.nonblocking():
			try:
				charWaiting = uart.inWaiting()
			except:
				print('Got OSError')
				break
			if charWaiting > 0:
				try:
					info = uart.readline().decode('utf-8').strip()
					if info != '\n':
						info = info.replace('\n', '')
						if len(info) in [10, 11, 12]:
							print(info)
							data = str(info).split('/')
							fire = False
							CO = False
							GAS = False
							if float(data[0]) > 700:
								GAS = True
							if float(data[1]) > 250:
								CO = True
							if float(data[2]) > 0.0:
								fire = True
							if fire:
								send('Hello. You have fire!')
							if GAS:
								send('Hello. You have GAS!')
							if CO:
								send('Hello. You have CO!')
							if fire or CO or GAS:
								time.sleep(30)		
				except:
					print('Got no data')
			time.sleep(0.01)
while True:
	connect_and_read()

