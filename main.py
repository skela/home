from settings import Settings
from doorbell import DoorbellManager
from chromecast import ChromecastManager
from xcomfort_manager import XComfortManager
from homekit_manager import HomeKitManager
from samsung_manager import SamsungManager

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
	parser.add_argument("-txc","--test_xcomfort_bridge", help="Test xComfort Bridge",action="store_true")
	parser.add_argument("-hk","--homekit", help="Start Homekit Service",action="store_true")
	parser.add_argument("-xc","--xcomfort", help="Issue command to xComfort device",action="store_true")		
	parser.add_argument("-c","--command", help="Command to send to xComfort device, either on or off")	
	parser.add_argument("-dl","--download", help="Download a list of configured xComfort devices",action="store_true")
	parser.add_argument("-d","--device", help="Name of xComfort device, as defined in settings.json")
	
	parser.add_argument("-s","--samsung", help="Issue command to Samsung device",action="store_true")	

	args = parser.parse_args()
	if args.test_chromecast_doorbell:
		settings = Settings()
		chromecast = ChromecastManager(settings)
		chromecast.play_doorbell()
	elif args.test_xcomfort_bridge:
		settings = Settings()
		xcomfort = XComfortManager(settings.xcomfort)
		xcomfort.test()		
	elif args.xcomfort:
		settings = Settings()
		xcomfort = XComfortManager(settings.xcomfort)
		if args.download:
			xcomfort.download_devices()
		else:
			xcomfort.send_command(args.device,args.command)
	elif args.homekit:
		settings = Settings()
		hk = HomeKitManager(settings)
		hk.start()
	elif args.samsung:
		settings = Settings()
		samsung = SamsungManager(settings)
		samsung.start()
	else:
		main()
