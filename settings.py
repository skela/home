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
			self.chromecast = ChromecastSettings(name=d["chromecast"]["name"])
		else:
			self.chromecast = ChromecastSettings(name=None)

		if "xcomfort" in d:
			x = d["xcomfort"]
			self.xcomfort = XComfortSettings(ip=x["ip"],auth_key=x["auth_key"])
		else:
			self.xcomfort = XComfortSettings(ip=None,auth_key=None)

class ChromecastSettings(object):

	def __init__(self,name:str):
		self.name = name

class XComfortSettings(object):

	def __init__(self,ip:str,auth_key:str):
		self.ip = ip
		self.auth_key = auth_key
