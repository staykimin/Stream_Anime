import asyncio

class Security:
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
		kimin.cfg = {
			"score":{
				"max_sesi":{
					"max":1,
					"score":20
				},
				"score":{
					"low":30,
					"medium":60,
					"high":80
				},
				"ip_change":{
					"min":300,
					"score":30
				},
				"fingerprint":{
					"score":30
				},
				"user-agent":{
					"score":20
				},
				"current":0
			},
		}
	
	async def _IsLimit(kimin, ip:str):
		return False
	
	async def _BlockIP(kimin, ip: str):
		print(f"{ip} Diblokir")
	
	async def _AddCount(kimin, **parameter):
		if not 'redis' in parameter:
			raise ValueError("Redis Tidak Valid")
		
		count = await parameter['redis']['limiter'].incr(parameter['kunci'])
		if count == 1:
			await parameter['redis']['limiter'].expire(parameter['kunci'], parameter['config']['durasi'])
		return count
	
	async def _GetIP(kimin, **parameter):
		return ip.split(",")[0].strip() if parameter['request'].get('X-Forwarded-For') else parameter['request'].client.host
	
	async def _GetUA(kimin, **parameter):
		return parameter['request'].headers.get("user-agent", "-")
	
	async def _Scoring(kimin, **parameter):
		hasil = {"status":False}
		if not 'redis' in parameter:
			raise ValueError("Redis Tidak Valid")
		if not 'request' in parameter:
			raise ValueError('Request Tidak Valid')
		
		request = parameter['request']
		id_sesi = request.cookies.get("gid") if not 'id_sesi' in parameter else parameter['id_sesi']
		redis = kimin.parameter['loader'].Load('db_redis')
		json = kimin.parameter['loader'].Load('json')
		time = kimin.parameter['loader'].Load('time')
		now = int(time.time())
		headers = dict(request.headers) if not 'headers' in parameter else parameter['headers']
		if parameter['ua'] == '-':
			hasil['data'] = f"Terdeteksi Aktivitas Mencurigakan"
			hasil['code'] = 429
			return hasil
		
		if id_sesi:
			db = await redis().GetData(redis=parameter['redis'], kunci=id_sesi)
			if not db:
				hasil['data'] = f"Terdeteksi Aktivitas Mencurigakan"
				hasil['code'] = 429
				return hasil
			
			db = json.loads(db)
			if len(db['ip']) <= kimin.cfg['score']['max_sesi']['max']:
				kimin.cfg['score']['current'] += kimin.cfg['score']['max_sesi']['score']
			
			if not parameter['ip'] in db['ip']:
				selisih = now - int(db.get('ts', 0))
				if selisih > kimin.cfg['score']['ip_change']['min']:
					kimin.cfg['score']['current'] += kimin.cfg['score']['ip_change']['score']
				db['ip'].append(parameter['ip'])
				db['ts'] = now
			
			if parameter['ua'] == db.get('ua', ''):
				kimin.cfg['score']['current'] += kimin.cfg['score']['user-agent']['score']
			
			if 'HI' in headers and isinstance(headers['HI'], str):
				if db['fp'] is None:
					kimin.cfg['score']['current'] += kimin.cfg['score']['fingerprint']['score']
				elif headers['HI'] == db['fp']:
					kimin.cfg['score']['current'] += kimin.cfg['score']['fingerprint']['score']
			
			db = json.dumps(db)
			await redis().SetData(redis=parameter['redis'], data=[{id_sesi:db, "exp":3600}])
			hasil['status'] = True
			hasil['sesi'] = id_sesi
		else:
			db = await redis().GetData(redis=parameter['redis'])
			sesi = [i for i in db if parameter['ip'] in json.loads(i['data'])['ip']]
			if len(sesi) > 0:
				parameter['id_sesi'] = sesi[-1]['id']
				parameter['headers'] = headers
				return await kimin._Scoring(**parameter)
			else:
				uuid = kimin.parameter['loader'].Load('uuid')
				hashlib = kimin.parameter['loader'].Load('hashlib')
				token = str(uuid.uuid4())
				sesi = hashlib.sha256(f"{now}{token}{parameter['ip']}{parameter['ua']}".encode()).hexdigest()
				parameter['id_sesi'] = sesi
				parameter['headers'] = headers
				tmp = {
					"ip":[parameter['ip']],
					"ts":now,
					"ua":parameter['ua'],
					"fp":None
				}
				await redis().SetData(redis=parameter['redis'], data=[{sesi:json.dumps(tmp), "exp":3600}])
				return await kimin._Scoring(**parameter)
		
		hasil['score'] = 'high' if kimin.cfg['score']['current'] >= kimin.cfg['score']['score']['high'] else 'medium' if kimin.cfg['score']['current'] > kimin.cfg['score']['score']['low'] and kimin.cfg['score']['current'] < kimin.cfg['score']['score']['high'] else 'low'
		hasil['id_sesi'] = id_sesi
		return hasil
		
	async def Execute(kimin, **parameter):
		hasil = {"status":False}
		request = parameter['request']
		ip = await kimin._GetIP(**parameter)
		ua = await kimin._GetUA(**parameter)
		
		# if ua == "-":
			# hasil['data'] = f"Traffic Mencurigakan"
			# hasil['code'] = 429
			# return hasil
		
		fp = request.headers.get('HI')
		# Cek Limit IP
		prefix = parameter['config']['prefix']
		threshold = parameter['config']['threshold']
		rate = parameter['config']['max']
		ip_key = prefix['ip'] + ip
		parameter['kunci'] = ip_key
		ip_count = await kimin._AddCount(**parameter)
		if ip_count > rate['ip']:
			if threshold['ip'] < ip_count - rate['ip']:
				asyncio.create_task(kimin._BlockIP(ip))
			hasil['data'] = f"Too many requests."
			hasil['code'] = 429
			return hasil
		
		# Cek Limit FP
		if fp:
			fp_key = prefix['fp'] + fp
			parameter['kunci'] = fp_key
			fp_count = await kimin._AddCount(**parameter)
			if fp_count > rate['fp']:
				if threshold['fp'] < fp_count - rate['fp']:
					asyncio.create_task(kimin._BlockIP(ip))
				hasil['data'] = f"Too many request"
				hasil['code'] = 429
				return hasil
		
		cek_sesi = await kimin._Scoring(redis=parameter['redis']['req'], request=request, ip=ip, ua=ua)
		return cek_sesi
		# if id_sesi:
			# sesi = await kimin._GenSesi()
		# hasil['status'] = True
			# else:
				# hasil['status'] = True
		# else:
			# hasil['data'] = f"Traffic Incosistent"
			# hasil['code'] = 429
		# return hasil