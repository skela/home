import asyncio
import aiohttp

from xcomfort import Bridge
from xcomfort.bridge import State
from xcomfort.devices import LightState,Light
from xcomfort.connection import setup_secure_connection,ConnectionState

from settings import XComfortSettings

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
				dev_type = device["devType"]

				if dev_type == 100 or dev_type == 101:
					dimmable = device['dimmable']
					state = LightState(device['switch'], device['dimmvalue'])
					light = Light(self, device_id, name, dimmable, state)
					self._add_device(light)
				else:
					print(f"Unknown device type {dev_type} named '{name}' - Skipped")


class XComfortManager(object):

	def __init__(self, settings:XComfortSettings):
		self.settings = settings

	def test(self):		
		asyncio.run(self._test())
	
	async def _test(self):
		bridge = XComfortBridge(self.settings.ip, self.settings.auth_key)
			
		asyncio.create_task(bridge.run())
		
		devices = await bridge.get_devices()

		print(len(devices))
		await bridge.close()

	def download_devices(self):		
		asyncio.run(self._download_devices())

	async def _download_devices(self):
		bridge = XComfortBridge(self.settings.ip, self.settings.auth_key)
			
		asyncio.create_task(bridge.run())
		
		devices = await bridge.get_devices()
		
		await bridge.close()

		print(f"Found {len(devices)} xComfort Devices:")
		for (id,device) in devices.items():
			print(f'"id":{id}, "name":"{device.name}", "dimmable":{device.dimmable}')

	def send_command(self, device_name:str, command:str):
		asyncio.run(self._send_command(device_name, command))

	async def _send_command(self, device_name:str, command:str):

		device = self.settings.get_device(device_name)

		if device is None:
			exit(f"Device '{device_name} is missing from settings.json")

		cmd = True
		if command == "off":
			cmd = False
		elif command == "on":
			cmd = True
		else:
			exit(f"Command '{command} was not recognized, should be either on or off")

		bridge = XComfortBridge(self.settings.ip, self.settings.auth_key)
		
		await bridge._connect()

		await bridge.switch_device(device.id, cmd)

		await bridge.close()
