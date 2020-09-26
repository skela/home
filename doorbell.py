import json
import getpass
from pathlib import Path
from pprint import pprint
import datetime

from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError

cache_file = Path("test_token.cache")

def token_updated(token):
	cache_file.write_text(json.dumps(token))

def otp_callback():
	auth_code = input("2FA code: ")
	return auth_code

class DoorbellEvent(object):

	def __init__(self,event:dict):
		self.id = event['id']
		self.kind = event['kind']
		self.answered = event["answered"]
		self.created_at = event["created_at"]

	def print(self):
		print('ID:\t\t%s' % self.id)
		print('Kind:\t\t%s' % self.kind)
		print('Answered:\t%s' % self.answered)
		print('When:\t\t%s' % self.created_at)
		print(f"Timesince:\t{self.timesince}")
		print('--' * 50)

	@property
	def timesince(self):
		delta = datetime.datetime.now(self.created_at.tzinfo) - self.created_at
		return delta.total_seconds()

class DoorbellManager(object):

	def __init__(self):
		if cache_file.is_file():
			auth = Auth("MyProject/1.0", json.loads(cache_file.read_text()), token_updated)
		else:
			username = input("Username: ")
			password = getpass.getpass("Password: ")
			auth = Auth("MyProject/1.0", None, token_updated)
			try:
				auth.fetch_token(username, password)
			except MissingTokenError:
				auth.fetch_token(username, password, otp_callback())
		self.ring = Ring(auth)
		self.ring.update_data()

	def get_doorbell(self):
		devices = self.ring.devices()
		bell = devices["doorbots"][0]		
		return bell

	def get_dings(self) -> DoorbellEvent:
		bell = self.get_doorbell()
		events = bell.history(limit=15,kind="ding")
		dings = list()
		for event in events:		
			ding = DoorbellEvent(event)
			# ding.print()
			dings.append(ding)
		dings = sorted(dings, key=lambda ding: ding.timesince) 
		return dings

	def get_last_ding(self) -> DoorbellEvent:		
		dings = self.get_dings()
		if len(dings) > 0:
			ding = dings[0]
			return ding
		return None
