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
		print('ID:       %s' % self.id)
		print('Kind:     %s' % self.kind)
		print('Answered: %s' % self.answered)
		print('When:     %s' % self.created_at)		
		print('--' * 50)

def main():
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

	ring = Ring(auth)
	ring.update_data()

	devices = ring.devices()
	bell = devices["doorbots"][0]
	pprint(bell)

	dings = bell.history(limit=15,kind="ding")
	# for event in dings:
	if len(dings) > 0:
		ding = DoorbellEvent(dings[0])
		# ding = DoorbellEvent(event)
		print("Last Ding:")
		ding.print()
		delta = datetime.datetime.now(ding.created_at.tzinfo) - ding.created_at
		print(f"Seconds since event: {delta.total_seconds()}")

	# alerts = ring.active_alerts()
	# pprint(alerts)


if __name__ == "__main__":
	main()
