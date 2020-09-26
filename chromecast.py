import pychromecast
from settings import Settings
from pprint import pprint

class Chromecast(object):

	def __init__(self,cast):
		self.cast = cast

	def play_mp3(self,url:str):		
		mc = self.cast.media_controller
		mc.play_media(url, 'audio/mpeg')

class ChromecastManager(object):

	def __init__(self, settings:Settings):
		self.settings = settings		
		
	def get_chromecast(self, name:str = None) -> Chromecast:
		friendly_name = name
		if friendly_name is None:
			friendly_name = self.settings.chromecast_name
		chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])	
		cast = chromecasts[0]
		cast.wait()
		return Chromecast(cast)

	def get_chromecasts(self) -> list:
		c = list()		
		chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["*"])
		pprint(chromecasts)
		for cast in chromecasts:		
			cast.wait()
			c.append(Chromecast(cast))
		return c

	def play_doorbell(self):
		cast = self.get_chromecast()
		cast.play_mp3(self.settings.doorbell_file)
		# casts = self.get_chromecasts()
		# for cast in casts:
		# 	cast.play_mp3(self.settings.doorbell_file)
		# services, browser = pychromecast.discovery.discover_chromecasts()
		# pprint(services)
		# pychromecast.discovery.stop_discovery(browser)
