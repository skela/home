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
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-tcd","--test_chromecast_doorbell", help="Test doorbell sound on Chromecast",action="store_true")
	args = parser.parse_args()
	if args.test_chromecast_doorbell:
		settings = Settings()
		chromecast = ChromecastManager(settings)		
		chromecast.play_doorbell()
	else:
		main()
