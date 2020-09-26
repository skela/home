import pychromecast
from settings import Settings
from pprint import pprint

class Chromecast(object):

	def __init__(self,cast):
		self.cast = cast

	def play_mp3(self,url:str):
		self.cast.wait()
		mc = self.cast.media_controller
		mc.play_media(url, 'audio/mp3')		

class ChromecastManager(object):

	def __init__(self, settings:Settings):
		self.settings = settings		
		
	def get_chromecast(self, name:str = None) -> Chromecast:
		friendly_name = name
		if friendly_name is None:
			friendly_name = self.settings.chromecast_name
		chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])	
		cast = chromecasts[0]		
		return Chromecast(cast)

	def get_chromecasts(self) -> list:
		c = list()
		chromecasts = pychromecast.get_chromecasts()
		pprint(chromecasts)
		for cast in chromecasts:
			c.append(Chromecast(cast))
		return c

	def play_doorbell(self):
		cast = self.get_chromecast()
		cast.play_mp3(self.settings.doorbell_file)
