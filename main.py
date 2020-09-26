import json
import getpass
from pathlib import Path
from pprint import pprint
import datetime

from settings import Settings
from doorbell import DoorbellManager
from chromecast import ChromecastManager

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

if __name__ == "__main__":
	main()
