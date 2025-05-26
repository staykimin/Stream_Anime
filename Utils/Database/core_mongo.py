class Database:
	def __init__(kimin, modul, cfg):
		kimin.modul, kimin.cfg = modul, cfg
		kimin.modul['colorama'].init(autoreset=True)
	
	def Koneksi(kimin):
		try:
			kimin.koneksi = kimin.modul['pymongo'].MongoClient(
				kimin.cfg['database']['host'].replace("<db_password>", kimin.cfg['database']['password']),
				serverSelectionTimeoutMS=5000,   # Maksimal waktu menunggu pemilihan server
				connectTimeoutMS=10000,          # Maksimal waktu koneksi
				retryWrites=True
				)
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Konek ke MongoDB{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!")
		except Exception as e:
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Konek ke MongoDB{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		return kimin.koneksi
	
	def IsDBReady(kimin, **parameter):
		try:
			db = kimin.koneksi.list_database_names()
			target = parameter['db']
			if target in db:
				if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
					print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Database{kimin.modul['colorama'].Fore.MAGENTA} {target}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} FOUND!")
				return True
			else:
				if 're-create-db' in kimin.cfg['database'] and kimin.cfg['database']['re-create-db']:
					kimin.koneksi[target]
					if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
						print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Membuat Database{kimin.modul['colorama'].Fore.MAGENTA} {target}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!")
					return True
				else:
					if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
						print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Database{kimin.modul['colorama'].Fore.MAGENTA} {target}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} NOT FOUND!")
		except Exception as e:
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Cek Database{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		return False
	
	def IsColReady(kimin, **parameter):
		try:
			db = kimin.koneksi[parameter['db']]
			col = db.list_collection_names()
			parameter['collation'] = parameter['tabel']
			if parameter['collation'] in col:
				if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
					print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Collation{kimin.modul['colorama'].Fore.MAGENTA} {parameter['collation']}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} FOUND!")
				return True
			else:
				if 're-create-col' in kimin.cfg['database'] and kimin.cfg['database']['re-create-db']:
					db[parameter['collation']]
					if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
						print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Membuat Collation{kimin.modul['colorama'].Fore.MAGENTA} {parameter['collation']}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!")
					return True
				else:
					if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
						print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Collation{kimin.modul['colorama'].Fore.MAGENTA} {parameter['collation']}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} NOT FOUND!")
		except Exception as e:
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Cek Collation{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		return False
	
	def GetData(kimin, **parameter):
		exclude = ['db', 'tabel']
		data = {i:parameter[i] for i in parameter if not i in exclude}
		hasil = {"status":False}
		if not kimin.IsDBReady(**parameter) or not kimin.IsColReady(**parameter):
			hasil['error'] = "database atau collation tidak tersedia"
			return hasil
		db = kimin.koneksi[parameter['db']]
		col = db[parameter['tabel']]
		try:
			hasil['data'] = [{a:i[a] if not a == "_id" else str(i[a]) for a in i} for i in col.find(parameter.get('filter', {}))]
			hasil['status'] = True
		except Exception as e:
			hasil['error'] = 'Ada Kesalahan Di Server'
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Operasi Data{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		return hasil
	
	def Data(kimin, **parameter):
		exclude = ['db', 'tabel', 'mode', 'data']
		data = {i:parameter[i] for i in parameter if not i in exclude}
		hasil = {"status":False}
		if not kimin.IsDBReady(**parameter) or not kimin.IsColReady(**parameter):
			hasil['error'] = "database atau collation tidak tersedia"
			return hasil
		
		db = kimin.koneksi[parameter['db']]
		col = db[parameter['tabel']]
		try:
			if parameter['mode'] == 'add':
				now_utc = kimin.modul['datetime'].datetime.now(kimin.modul['datetime'].timezone.utc)
				now_str = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f+%z")
				parameter['data']['created_at'] = kimin.modul['datetime'].datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%f+%z")
				parameter['data']['update_at'] = kimin.modul['datetime'].datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%f+%z")
				hasil['data'] = str(col.insert_one(parameter['data']).inserted_id)
			elif parameter['mode'] == 'add_many':
				hasil['data'] = str(col.insert_many(parameter['data']).inserted_ids)
			elif parameter['mode'] == 'update':
				hasil['data'] = col.update_one(filter=parameter['filter'], update={"$set":parameter['data']})
			elif parameter['mode'] == 'update_many':
				hasil['data'] = col.update_many(filter=parameter['filter'], update={"$set":parameter['data']})
			elif parameter['mode'] == 'delete':
				hasil['data'] = col.delete_one(filter=parameter['filter'])
			elif parameter['mode'] == 'delete_many':
				hasil['data'] = col.delete_many(filter=parameter['filter'])
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} {parameter['mode']}{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!")
			hasil['status'] = True
		except Exception as e:
			hasil['error'] = 'Ada Kesalahan Di Server'
			if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log']:
				print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Operasi Data{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!")
			log = kimin.modul['ext'](modul=kimin.modul).Log(kimin.cfg['log']['path'])
			if 'log' in kimin.cfg and 'notif' in kimin.cfg['log'] and 'status' in kimin.cfg['log']['notif'] and kimin.cfg['log']['notif']['status'] and 'token' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['token'] == "" and 'id_account' in kimin.cfg['log']['notif'] and not kimin.cfg['log']['notif']['id_account'] == "":
				kimin.modul['ext'](modul=kimin.modul).TeleNotif(chat_id=kimin.cfg['log']['notif']['id_account'], token=kimin.cfg['log']['notif']['token'], text=log['log'] if not 'static_text' in kimin.cfg['log']['notif'] or kimin.cfg['log']['notif']['static_text'] == "" else f"{kimin.cfg['log']['notif']['static_text']}{log['log']}")
			print(f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.GREEN} SUCCESS!" if 'log' in kimin.cfg and 'show_log' in kimin.cfg['log'] and kimin.cfg['log']['show_log'] and log['status'] else f"{kimin.modul['colorama'].Fore.CYAN}[{kimin.modul['ext'](modul=kimin.modul).GetTime()['data']}]{kimin.modul['colorama'].Fore.YELLOW} Simpan Log{kimin.modul['colorama'].Fore.WHITE} ->{kimin.modul['colorama'].Fore.RED} FAILED!\n{kimin.modul['colorama'].Fore.WHITE}Error : {kimin.modul['colorama'].Fore.RED}{log['error']}")
		return hasil