class Database:
	def __init__(kimin, modul, cfg):
		kimin.modul = modul
		if cfg['type'] == 'mongodb':
			kimin.key = cfg['password']
			kimin.base_url = cfg['host']
			kimin.source = cfg['source']
	
	def Get_Header(kimin):
		return {
			"api-key":kimin.key,
			"Content-Type":"application/json",
			"Access-Control-Request-Headers": "*"
		}
	
	def Get_TimeStamp(kimin, tambah=None):
		return {"$timestamp":{"t":int(kimin.modul['datetime'].datetime.now().timestamp()), "i":1}}
	
	def Get_Data(kimin, **parameter):
		exclude = ['db', 'tabel']
		data = {i:parameter[i] for i in parameter if not i in exclude}
		data['dataSource'], data['database'], data['collection'] = kimin.source, parameter['db'], parameter['tabel']
		respon = kimin.modul['Executor'](
			modul=kimin.modul,
			method="POST",
			header = kimin.Get_Header(),
			url = f"{kimin.base_url}/find",
			data=kimin.modul['json'].dumps(data),
			data_type="form"
			).Execute()
		
		return respon
	
	def Data(kimin, **parameter):
		exclude = ['db', 'tabel', 'mode', 'data']
		data = {i:parameter[i] for i in parameter if not i in exclude}
		data['dataSource'], data['database'], data['collection'] = kimin.source, parameter['db'], parameter['tabel']
		if parameter['mode'] == 'add':
			url = f"{kimin.base_url}/insertOne"
			parameter['data']['created_at'] = kimin.Get_TimeStamp()
			parameter['data']['update_at'] = kimin.Get_TimeStamp()
			data['document'] = parameter['data']
		
		elif parameter['mode'] == 'add_many':
			url = f"{kimin.base_url}/insertMany"
			parameter['data']['created_at'] = kimin.Get_TimeStamp()
			parameter['data']['update_at'] = kimin.Get_TimeStamp()
			data['document'] = parameter['data']
		
		elif parameter['mode'] == 'update':
			url = f"{kimin.base_url}/updateOne"
			parameter['data']['update_at'] = kimin.Get_TimeStamp()
			data['update'] = {"$set":parameter['data']}
		
		elif parameter['mode'] == 'delete':
			url = f"{kimin.base_url}/deleteOne",
		
		elif parameter['mode'] == 'delete_many':
			url = f"{kimin.base_url}/deleteMany"
		
		respon = kimin.modul['Executor'](
			modul=kimin.modul,
			method="POST",
			header = kimin.Get_Header(),
			url = url,
			data=kimin.modul['json'].dumps(data),
			data_type="form"
			).Execute()
		
		return respon