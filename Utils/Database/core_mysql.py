import mysql.connector
class Database:
	def __init__(kimin, modul, cfg):
		kimin.modul, kimin.cfg = modul, cfg
		kimin.modul['colorama'].init(autoreset=True)
		kimin.data = {}
	
	def Konek(kimin):
		hasil = {'status':False}
		try:
			kimin.data['koneksi'] = mysql.connector.connect(
				host=kimin.cfg['database']['host'],
				user=kimin.cfg['database']['user'],
				password=kimin.cfg['database']['password']
			)
			if kimin.data['koneksi'].is_connected():
				hasil['koneksi'] = kimin.data['koneksi']
			
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				if hasil['status']:
					print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Konek ke Mysql{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!")
				else:
					print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Konek ke Mysql{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			hasil['status'] = True
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Konek ke Mysql{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		return hasil
	
	def CheckDB(kimin, koneksi):
		hasil = {'status':False}
		try:
			kimin.data['cursor'] = koneksi.cursor()
			db = kimin.cfg['database']['source']
			kimin.data['cursor'].execute(f"SHOW DATABASES LIKE '{db}'")
			kimin.data['db_ready'] = kimin.data['cursor'].fetchone()
			kimin.data['db_ready'] = True if kimin.data['db_ready'] else False
			
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and kimin.data['db_ready']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Database{kimin.modul['colorama'].Fore.MAGENTA} {kimin.cfg['database']['source']}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} FOUND!")
			else:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Database{kimin.modul['colorama'].Fore.MAGENTA} {kimin.cfg['database']['source']}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} NOT FOUND!")
			hasil['status'] = True
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Cek Database{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		finally:
			kimin.data['cursor'].close()
		return hasil
	
	def CheckTabel(kimin, koneksi, tabel):
		hasil = {'status':False}
		try:
			kimin.data['cursor'] = koneksi.cursor(dictionary=True)
			db = kimin.cfg['database']['source']
			kimin.data['cursor'].execute(f"USE {db}")
			kimin.data['cursor'].execute(f"SHOW TABLES LIKE '{tabel}'")
			kimin.data['tabel_ready'] = kimin.data['cursor'].fetchone()
			kimin.data['tabel_ready'] = True if kimin.data['tabel_ready'] else False
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and kimin.data['tabel_ready']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Tabel{kimin.modul['colorama'].Fore.MAGENTA} {tabel}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} FOUND!")
			else:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Tabel{kimin.modul['colorama'].Fore.MAGENTA} {tabel}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} NOT FOUND!")
			hasil['status'] = True
		
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Cek Database{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		finally:
			kimin.data['cursor'].close()
		return hasil
	
	def AddData(kimin, **parameter):
		hasil = {'status':False}
		try:
			koneksi = kimin.Konek()
			if koneksi['status']:
				db = kimin.CheckDB(koneksi['koneksi'])
				tabel = kimin.CheckTabel(koneksi=koneksi['koneksi'], tabel=parameter['tabel'])
				if db['status'] and tabel['status']:
					kursor = koneksi['koneksi'].cursor(dictionary=True)
					kursor.execute(f"USE {kimin.cfg['database']['source']}")
					kolom = ", ".join([i for i in parameter['data']])
					value = ", ".join([f"'{parameter['data'][i]}'" for i in parameter['data']])
					query = f"INSERT INTO {parameter['tabel']} ({kolom}) VALUES ({value})"
					kursor.execute(query)
					koneksi['koneksi'].commit()
					hasil['status'] = True
			return hasil
		except mysql.connector.Error as error:
			if error.errno == 1062:
				hasil['error'] = 'Data Ada Yang Duplicate'
			else:
				hasil['error'] = error
		
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Tambah{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		finally:
			kursor.close()
			kimin.Disconnect(koneksi['koneksi'])
		return hasil
	
	def UpdateData(kimin, **parameter):
		hasil = {'status':False}
		try:
			koneksi = kimin.Konek()
			if koneksi['status']:
				db = kimin.CheckDB(koneksi['koneksi'])
				tabel = kimin.CheckTabel(koneksi=koneksi['koneksi'], tabel=parameter['tabel'])
				if db['status'] and tabel['status']:
					kursor = koneksi['koneksi'].cursor(dictionary=True)
					kursor.execute(f"USE {kimin.cfg['database']['source']}")
					data = ", ".join([f"'{i}' = '{parameter['data'][i]}'" for i in parameter['data']])
					query = f"UPDATE {parameter['tabel']} SET {data} {parameter['query']}"
					kursor.execute(query)
					koneksi['koneksi'].commit()
					hasil['status'] = True
			return hasil
		except mysql.connector.Error as error:
			if error.errno == 1062:
				hasil['error'] = 'Data Ada Yang Duplicate'
			else:
				hasil['error'] = error
		
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Tambah{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		finally:
			kursor.close()
			kimin.Disconnect(koneksi['koneksi'])
		return hasil
	
	def Hapus(kimin, **parameter):
		hasil = {'status':False}
		try:
			koneksi = kimin.Konek()
			if koneksi['status']:
				db = kimin.CheckDB(koneksi['koneksi'])
				tabel = kimin.CheckTabel(koneksi=koneksi['koneksi'], tabel=parameter['tabel'])
				if db['status'] and tabel['status']:
					kursor = koneksi['koneksi'].cursor(dictionary=True)
					kursor.execute(f"USE {kimin.cfg['database']['source']}")
					query = f"DELETE FROM {parameter['tabel']} WHERE {parameter['query']}"
					kursor.execute(query)
					koneksi['koneksi'].commit()
					# hasil['result'] = kursor.lastrowid 
					hasil['status'] = True
			return hasil
		
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Delete{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		finally:
			kursor.close()
			kimin.Disconnect(koneksi['koneksi'])
		return hasil
		
	def ExecuteSQL(kimin, **parameter):
		hasil = {'status':False}
		try:
			koneksi = kimin.Konek()
			if koneksi['status']:
				db = kimin.CheckDB(koneksi['koneksi'])
				tabel = kimin.CheckTabel(koneksi=koneksi['koneksi'], tabel=parameter['tabel'])
				if db['status'] and tabel['status']:
					kursor = koneksi['koneksi'].cursor(dictionary=True)
					kursor.execute(f"USE {kimin.cfg['database']['source']}")
					hasil['query'] = parameter['query']
					kursor.execute(parameter['query'])
					hasil['result'] = kursor.fetchall() if not parameter.get('mode', None) else []
					hasil['status'] = True
			return hasil
		
		except Exception as e:
			hasil['error'] = e
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Cek Database{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		finally:
			kursor.close()
		return hasil
	
	def Disconnect(kimin, koneksi):
		if koneksi.is_connected():
			koneksi.close()
	