import requests
import json
import logging
import sys

from signalrcore.hub_connection_builder import HubConnectionBuilder

from settings import EaseeSettings

def _log(msg:str):
	print(f"[Easee] {msg}")

class EaseeManager(object):

	def __init__(self, settings:EaseeSettings):
		self.settings = settings
		self.cli = EaseeCLI()
		self.token = None
		self.signals = None		

	def start(self):	
		try:
			self._start_signals()
		except Exception as e:
			_log(f"Failed to start SignalR - {sys.exc_info()[0]}")

	def stop(self):
		self.token = None
		try:
			self._stop_signals()
		except Exception as e:
			_log(f"Failed to stop SignalR - {sys.exc_info()[0]}")

	def _start_signals(self):
		url = "https://api.easee.cloud/hubs/chargers"
		options = {"access_token_factory": self._get_access_token,"headers":{"APP":"no.easee.apps.bridge"}}
		self.signals = HubConnectionBuilder().with_url(url,options).configure_logging(logging.ERROR).with_automatic_reconnect({
				"type": "raw",
				"keep_alive_interval": 30,
				"reconnect_interval": 5,
				"max_attempts": 5
			}).build()
		
		self.signals.on_open(lambda: self.on_open())
		self.signals.on_close(lambda: self.on_close())
		self.signals.on_error(lambda data: print(f"An exception was thrown closed{data.error}"))
		self.signals.on("ProductUpdate", self.product_update)
		self.signals.start()

	def _stop_signals(self):		
		for device in self.settings.devices:
			self.signals.send("Unsubscribe", [device.id])
		self.signals.stop()

	def _get_access_token(self) -> str:
		if self.token is not None:
			return self.token.access
		_log("Obtaining new jwt token")
		self.token = self.cli.login(self.settings.username,self.settings.password)
		if self.token is not None:
			return self.token.access
		raise requests.exceptions.ConnectionError()		

	def on_open(self):
		_log("SignalR connection opened and handshake received ready to send messages")
		for device in self.settings.devices:
			self.signals.send("SubscribeWithCurrentState", [device.id, True])

	def on_close(self):
		_log("SignalR connection closed")

	def product_update(self,stuff: list): 
		_log(f"SignalR msg received {stuff}")

class EaseeToken(object):
	
	def __init__(self,d:dict):
		self.access = d["accessToken"]
		self.refresh = d["refreshToken"]
		self.expiresIn = d["expiresIn"]

class EaseeCLI(object):

	def __init__(self):
		self.api_url = "https://api.easee.cloud/api"
		self.default_headers = {"Content-Type": "application/json"}

	def login(self,username:str,password:str) -> EaseeToken:
		url = f'{self.api_url}/accounts/token'
		data = {"userName":username,"password":password}
		try:
			r = requests.post(url, data = json.dumps(data), headers=self.default_headers)
			if r.status_code == 200:
				d = r.json()
				token = EaseeToken(d)
				_log(f"Logged in successfully - {token.access}")
				return token
			_log(f"Failed to login - {r.status_code}")
			return None
		except:
			_log(f"An error ocurred - {r.status_code}")
			return None
