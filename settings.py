import os
import json

class Settings(object):

	def __init__(self):
		self.doorbell_file = "https://raw.githubusercontent.com/skela/home/master/static/bell1.mp3"

		d = dict()
		if os.path.exists("settings.json"):
			f = open("settings.json")
			s = f.read()
			f.close()
			d = json.loads(s)

		if "chromecast" in d:
			self.chromecast = ChromecastSettings(d=d["chromecast"])
		else:
			self.chromecast = ChromecastSettings(name=None)

		if "xcomfort" in d:			
			self.xcomfort = XComfortSettings(d=d["xcomfort"])
		else:
			self.xcomfort = XComfortSettings()

class ChromecastSettings(object):

	def __init__(self,name:str=None,d:dict=None):
		if d is None:
			self.name = name
		else:
			self.name = d["name"]


class XComfortDevice(object):

	def __init__(self,id:int=None,name:str=None,dimmable:bool=None,add_to_homekit:bool=None,d:dict=None):

		if d is None:
			self.id = id
			self.name = name
			self.dimmable = dimmable
			self.add_to_homekit = add_to_homekit
		else:
			self.id = d["id"]
			self.name = d["name"]
			self.dimmable = d["dimmable"]
			self.add_to_homekit = d["add_to_homekit"]

		if self.add_to_homekit is None:
			self.add_to_homekit = False
	
class XComfortSettings(object):

	def __init__(self,ip:str=None,auth_key:str=None,devices:list=None,d:dict=None):
		if d is None:
			self.ip = ip
			self.auth_key = auth_key
			self.devices = devices
		else:
			self.ip = d["ip"]
			self.auth_key = d["auth_key"]
			l = list()
			if "devices" in d:
				for dev in d["devices"]:
					l.append(XComfortDevice(d=dev))
			self.devices = l

	def get_device(self, device_name:str) -> XComfortDevice:
		for dev in self.devices:
			if dev.name == device_name:
				return dev
		return None
