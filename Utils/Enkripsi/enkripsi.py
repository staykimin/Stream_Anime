from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

class Enkripsi_Async:
	def __init__(kimin, loader, **parameter):
		kimin.loader = loader
		kimin.parameter = parameter
	
	async def GenExpaid(kimin, durasi=5): # Buat Time Expaid
		time = kimin.loader.Load('time')
		return int(time.time()) + durasi * 60
	
	async def CheckExpaid(kimin, data): # Validasi Masa Berlaku
		time = kimin.loader.Load('time')
		return int(time.time()) > data
	
	async def SecurePassword(kimin, **parameter):
		hasil = {'status':False}
		try:
			hasil['data'] = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=parameter['salt'], iterations=100000, backend=default_backend()).derive(parameter['password'].encode())
			hasil['status'] = True
		except Exception as e:
			kimin.modul['ext'](loader=kimin.loader).Log("./")
			hasil['error'] = str(e)
		return hasil
	
	async def AES256Enc(kimin, **parameter): # Enkripsi AES 256
		hasil = {'status':False}
		os = kimin.loader.Load('os')
		base64 = kimin.loader.Load('base64')
		try:
			parameter['salt'] = os.urandom(16)
			kunci = await kimin.SecurePassword(**parameter)
			if not kunci['status']:
				return kunci
			iv = os.urandom(16)
			cipher = Cipher(algorithms.AES(kunci['data']), modes.CBC(iv), backend=default_backend()).encryptor()
			padder = PKCS7(algorithms.AES.block_size).padder()
			data = padder.update(parameter['data'].encode()) + padder.finalize()
			data = cipher.update(data) + cipher.finalize()
			hasil['data'] = base64.b64encode(parameter['salt'] + iv + data).decode()
			hasil['status'] = True
		except Exception as e:
			kimin.modul['ext'](loader=kimin.loader).Log("./")
			hasil['error'] = str(e)
		return hasil
	
	async def AES256Dec(kimin, **parameter): # Dekripsi AES 256
		hasil = {'status':False}
		base64 = kimin.loader.Load('base64')
		try:
			parameter['data'] = base64.b64decode(parameter['data'])
			parameter['salt'] = parameter['data'][:16]
			iv = parameter['data'][16:32]
			raw = parameter['data'][32:]
			kunci = await kimin.SecurePassword(**parameter)
			if not kunci['status']:
				return kunci
			cipher = Cipher(algorithms.AES(kunci['data']), modes.CBC(iv), backend=default_backend()).decryptor()
			padder = cipher.update(raw) + cipher.finalize()
			unpadder = PKCS7(algorithms.AES.block_size).unpadder()
			hasil['data'] = unpadder.update(padder) + unpadder.finalize()
			hasil['data'] = hasil['data'].decode('utf-8')
			hasil['status'] = True
		except Exception as e:
			kimin.modul['ext'](loader=kimin.loader).Log("./")
			hasil['error'] = str(e)
		return hasil
	
	async def E2EEnc(kimin, **parameter): # Enkripsi E2E / End-to-End Dengan Public Key
		hasil = {"status":False}
		base64 = kimin.loader.Load('base64')
		try:
			kunci = serialization.load_der_public_key(base64.b64decode(parameter['kunci']))
			hasil['data'] = kunci.encrypt(parameter['data'].encode('utf-8'), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
			hasil['data'] = base64.b64encode(hasil['data']).decode("utf-8")
			hasil['status'] = True
		except Exception as e:
			kimin.modul['ext'](loader=kimin.loader).Log("./")
			hasil['error'] = str(e)
		return hasil
	
	async def E2EDec(kimin, **parameter):
		hasil = {'status':False}
		try:
			parameter['data'] = eval(parameter['data'])
			kunci = serialization.load_pem_private_key(parameter['kunci'].encode('utf-8'), password=None)
			hasil['data'] = kunci.decrypt(parameter['data'], padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode('utf-8')
			hasil['status'] = True
		except Exception as e:
			kimin.modul['ext'](loader=kimin.loader).Log("./")
			hasil['error'] = str(e)
		return hasil