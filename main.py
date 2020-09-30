import json
import getpass
from pathlib import Path
from pprint import pprint
import datetime
import asyncio

from settings import Settings
from doorbell import DoorbellManager
from chromecast import ChromecastManager

from xcomfort import Bridge
from xcomfort.bridge import State
from xcomfort.devices import LightState,Light
from xcomfort.connection import setup_secure_connection

def main():
	settings = Settings()
	ring = DoorbellManager()
	chromecast = ChromecastManager(settings)
	ding = ring.get_last_ding()
	if ding is not None:
		print("Last Ding:")
		ding.print()
		if ding.timesince < 60:
			chromecast.play_doorbell()

class XComfortBridge(Bridge):

	def __init__(self, ip_address:str, authkey:str, session = None):
		super().__init__(ip_address, authkey, session)

	def _handle_SET_ALL_DATA(self, payload):
		
		if 'lastItem' in payload:
			self.state = State.Ready
		
		if 'devices' in payload:
			for device in payload['devices']:
				device_id = device['deviceId']
				name = device['name']
				dimmable = device['dimmable']
				state = LightState(device['switch'], device['dimmvalue'])

				light = Light(self, device_id, name, dimmable, state)

				self._add_device(light)

async def main_xcomfort():
	xcomfort = Settings().xcomfort
	bridge = XComfortBridge(xcomfort.ip, xcomfort.auth_key)
	
	await bridge._connect()
	# await bridge.run()
	
	await bridge.switch_device(48, True)

	await asyncio.sleep(10) 

	
	# devices = await bridge.get_devices()
	# devices = bridge._devices

	

	# print(len(devices))
	await bridge.close()

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-tcd","--test_chromecast_doorbell", help="Test doorbell sound on Chromecast",action="store_true")
	parser.add_argument("-txc","--test_xcomfort_bridge", help="Test xComfort Bridge",action="store_true")
	args = parser.parse_args()
	if args.test_chromecast_doorbell:
		settings = Settings()
		chromecast = ChromecastManager(settings)		
		chromecast.play_doorbell()
	elif args.test_xcomfort_bridge:
		asyncio.run(main_xcomfort())
	else:
		main()
