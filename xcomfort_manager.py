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


class XComfortDevice(object):

	def __init__(self,id:int,name:str,dimmable:bool,on:bool):
		self.id = id
		self.name = name
		self.dimmable = dimmable
		self.on = on

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

	@staticmethod
	def parse_devices(devices):
		device_list = list()
		print(f"Found {len(devices)} xComfort Devices:")
		for (id,device) in devices.items():						
			on = device.state.value.switch == True
			# print(f'A"id":{id}, "name":"{device.name}", "state":{device.state.value}')
			device_list.append(XComfortDevice(id,device.name,device.dimmable,on))
			if on:
				on = "on"
			else:
				on = "off"
			# print(f'B"id":{id}, "name":"{device.name}", "dimmable":{device.dimmable}, "on: {on}')
			print(f'"id":{id}, "name":"{device.name}", "dimmable":{device.dimmable}, "on: {on}')

		return device_list

	# devices is a list of XComfortDevice
	@staticmethod
	def get_device(devices:list,id:int) -> XComfortDevice:		
		for device in devices:
			if device.id == id:
				return device
		return None

	async def _download_devices(self):
		bridge = XComfortBridge(self.settings.ip, self.settings.auth_key)
			
		asyncio.create_task(bridge.run())
		
		devices = await bridge.get_devices()
		
		await bridge.close()

		return XComfortManager.parse_devices(devices)

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
		elif command == "toggle":
			devices = await self._download_devices()
			xdev = XComfortManager.get_device(devices,device.id)
			if xdev is not None:
				if xdev.on:
					cmd = False
				else:
					cmd = True
		else:
			exit(f"Command '{command} was not recognized, should be either on, off or toggle")

		bridge = XComfortBridge(self.settings.ip, self.settings.auth_key)
		
		await bridge._connect()		

		# if xdev is not None and xdev.on != cmd:
		await bridge.switch_device(device.id, cmd)
		if command and device.dimmable:
			bridge.dimm_device(device.id, 100)

		await bridge.close()
