from stem import Signal
from stem.control import Controller
class Proxy_Handler:
	def __init__(kimin, modul):
		kimin.modul = modul
		kimin.cfg = {
			"controller-port":3001,
			"proxy-port":9050
		}
	
	def ChangeIP(kimin):
		with Controller.from_port(port=kimin.cfg['controller-port']) as controller:
			controller.authenticate()  # Pastikan autentikasi berhasil
			controller.signal(Signal.NEWNYM)  # Sinyal untuk mereset sirkuit
	
	def Konek(kimin, **parameter):
		hasil = {"status":False}
		proxies = {
			'http': f'socks5h://127.0.0.1:{kimin.cfg["proxy-port"]}',
			'https':f'socks5h://127.0.0.1:{kimin.cfg["proxy-port"]}'
		}
		if 'rotate' in parameter and parameter.get('rotate', False) == True:
			kimin.ChangeIP()
		
		parameter = {i:parameter[i] for i in parameter if not i == 'rotate'}
		if not 'method' in parameter:
			hasil['error'] = '"method" Belum Didefinisikan'
			return hasil
		
		if not 'url' in parameter:
			hasil['error'] = '"url" Belum Didefinisikan'
			return hasil
		
		parameter['proxy'] = proxies
		respon = kimin.modul['Driver'](modul=kimin.modul, **parameter).Execute()
		return respon