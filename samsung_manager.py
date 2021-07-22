import os

from settings import Settings

# from samsungtvws import SamsungTVWS
# import samsungctl

class SamsungManager(object):

	def __init__(self, settings:Settings):
		self.settings = settings	

	def start(self):
		pass
		# token = None		
		# # tv = SamsungTVWS(host='10.0.1.155', port=8002, token=token)
		# # if token is None:
		# # 	tv.rest_device_info()
		# # 	# tv.open_browser('https://duckduckgo.com/')
		# # 	token = tv._get_token()
		# # 	print(f"Got token: {token}")
		# # else:
		# # 	tv.open_browser('https://duckduckgo.com/')
		# # 	# tv.shortcuts().power()

		# config = samsungctl.Config(host='10.0.1.155')

		# with samsungctl.Remote(config) as remote:
		# 	remote.KEY_MENU()

		# config.save('arse.txt')
