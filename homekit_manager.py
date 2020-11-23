# import locale
# from homekit.controller import Controller
# from homekit import HomeKitServer
# from homekit.model import Accessory, LightBulbService

import sys
sys.path.append('lib')

import asyncio
import logging
import signal
from pyhap.accessory_driver import AccessoryDriver

from pyhap.accessory import Accessory, Bridge
from pyhap.const import CATEGORY_LIGHTBULB
from xcomfort_manager import XComfortManager
from settings import Settings
from settings import XComfortDevice

class HomeKitXComfortLight(Accessory):

	category = CATEGORY_LIGHTBULB

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		settings = Settings()
		self.xcomfort = XComfortManager(settings.xcomfort)

		chars = [('On',self.set_on)]

		server = self.add_preload_service('Lightbulb', chars = [ name for (name,_) in chars ])

		for (name, setter) in chars:
			server.configure_char(name, setter_callback = setter)
		self.is_on = False

	def set_on(self, value):
		print(f"OMG value is {value}")
		if isinstance(value, str):
			if value == "1" or value.lower() == "on":
				self.is_on = True
			elif value == "0" or value.lower() == "off":
				self.is_on = False
			else:
				self.is_on = bool(value)
		else:
			self.is_on = bool(value)
		self.set_bulb()

	def set_bulb(self):
		if self.is_on:
			self.xcomfort.send_command(self.display_name,"on")
		else:
			self.xcomfort.send_command(self.display_name,"off")

	def stop(self):
		super().stop()

class HomeKitManager(object):

	def __init__(self, settings:Settings):
		self.settings = settings		
	
	def start(self):
		try:
			logging.basicConfig(level=logging.INFO)
			driver = AccessoryDriver(port=51827)
			bridge = Bridge(driver, 'Bridge')			
			for device in self.settings.xcomfort.devices:
				if not device.add_to_homekit:
					continue
				lamp = HomeKitXComfortLight(driver, device.name)
				bridge.add_accessory(lamp)
			driver.add_accessory(accessory=bridge)
			signal.signal(signal.SIGTERM, driver.signal_handler)
			driver.start()

		except KeyboardInterrupt:
			print('Stopping...')

# # controller = Controller()
# # stuff = controller.get_pairings()
# # print(stuff)
# results = Controller.discover_ble(30)
# for info in results:
# 	print('Name: {name}'.format(name=prepare_string(info['name'])))
# 	print('Url: http_impl://{ip}:{port}'.format(ip=info['address'], port=info['port']))
# 	print('Configuration number (c#): {conf}'.format(conf=info['c#']))
# 	print('Feature Flags (ff): {f} (Flag: {flags})'.format(f=info['flags'], flags=info['ff']))
# 	print('Device ID (id): {id}'.format(id=info['id']))
# 	print('Model Name (md): {md}'.format(md=prepare_string(info['md'])))
# 	print('Protocol Version (pv): {pv}'.format(pv=info['pv']))
# 	print('State Number (s#): {sn}'.format(sn=info['s#']))
# 	print('Status Flags (sf): {sf} (Flag: {flags})'.format(sf=info['statusflags'], flags=info['sf']))
# 	print('Category Identifier (ci): {c} (Id: {ci})'.format(c=info['category'], ci=info['ci']))
# 	print()
