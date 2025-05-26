class API_Handler:
	def __init__(kimin, loader, **parameter):
		kimin.loader, kimin.parameter = loader, parameter
		kimin.static_key = parameter['cfg']['server']['secret_key']
	
	async def DataVal(kimin, data, allow):
		return all([i in data for i in allow])
	
	async def Filter(kimin, **parameter):
		os = kimin.loader.Load('os')
		allowed = ['png', 'jpeg', 'jpg']
		ori = [i for i in os.listdir(parameter['base_path']) if os.path.isdir(f"{parameter['base_path']}/{i}") and parameter['cari'] in i]
		ori.sort(key=lambda x: os.path.getmtime(f"{parameter['base_path']}/{x}"), reverse=True)
		start = (parameter['page'] - 1 ) * 12
		end = start + 12
		data = ori[start:end]
		x = {i:{"base_path":f"{parameter['base_path']}/{i}", "data":[a for a in os.listdir(f"{parameter['base_path']}/{i}") if a.split(".")[-1] in parameter['allowed']], 'thumbnail':[a for a in os.listdir(f"{parameter['base_path']}/{i}") if a.split(".")[-1] in allowed]} for i in data}
		math = kimin.loader.Load('math')
		x['total_pages'] = math.ceil(len(ori) / 12)
		return x
	
	async def Execute(kimin, **parameter):
		hasil = {'status':False}
		allowed = ["mp4"]
		# base_path = "/mnt/Data_Server1/Data"
		# base_path = "/mnt/Data_Server1/Data"
		base_path = kimin.parameter['cfg']['server']['base_path']
		request = parameter.get('request')
		mode = parameter.get('mode')
		response = parameter.get('response')
		os = kimin.loader.Load('os')
		not_found = kimin.loader.Load('404')
		file = kimin.loader.Load('file')
		if not mode:
			return hasil
		
		if not response:
			return hasil
		
		if request.method == 'POST':
			id, header, data = dict(request.query_params), dict(request.headers), await request.json()
			if mode == 'data':
				x = await kimin.Filter(base_path=base_path, allowed=allowed, page=1 if not 'page' in data or not data['page'] else data['page'], cari="" if not 'cari' in data or data['cari'] == "" else f"{data['cari']}")
				hasil['data'] = {i:x[i] for i  in x if not i == 'total_pages'}
				hasil['total_pages'] = x['total_pages']
				hasil['status'] = True
			
			elif mode == 'find':
				if os.path.exists(f"{base_path}/{data['data']}"):
					hasil['data'] = [i for i in os.listdir(f"{base_path}/{data['data']}") if i.split(".")[-1] in allowed]
					hasil['data'].sort()
					hasil['status'] = True
		
		elif request.method == 'GET':
			url = dict(request.query_params)
			if mode == 'thumbnail':
				if 'path' in url and os.path.exists(f"{base_path}/{url['path']}"):
					return file(f"{base_path}/{url['path']}")
				else:
					raise not_found(status_code=404, detail="File not found")
			elif mode == 'player':
				if 'path' in url and 'base' in url and os.path.exists(f"{base_path}/{url['base']}") and os.path.exists(f"{base_path}/{url['base']}/{url['path']}"):
					return file(f"{base_path}/{url['base']}/{url['path']}")
				else:
					raise not_found(status_code=404, detail="File not found")
		return hasil
