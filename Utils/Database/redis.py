class Redis_Async:
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
	
	async def SetData(kimin, **parameter):
		if isinstance(parameter['data'], dict):
			for i in parameter['data']:
				if 'exp' in parameter:
					await parameter['redis'].setex(i, int(parameter['exp']), parameter['data'][i])
				else:
					await parameter['redis'].set(i, parameter['data'][i])
		
		elif isinstance(parameter['data'], list):
			for i in parameter['data']:
				kunci = list(i.keys())[0]
				value = i[kunci]
				exp = int(i['exp']) if 'exp' in i else None
				if exp:
					await parameter['redis'].setex(kunci, exp, value)
				else:
					await parameter['redis'].set(kunci, value)
	
	async def Konek(kimin, **parameter):
		if 'loader' in kimin.parameter and kimin.parameter['loader']:
			redis = kimin.parameter['loader'].Load('redis')
			return await redis(host=parameter['host'], password=parameter['password'], port=parameter['port'], decode_responses=True, db=parameter.get('db_name', 0))
		raise ValueError("Loader Tidak Valid")
	
	async def GetData(kimin, **parameter):
		if 'kunci' in parameter:
			return [await parameter['redis'].get(i) for i in parameter['kunci']] if isinstance(parameter['kunci'], list) else await parameter['redis'].get(parameter['kunci'])
		else:
			kunci = await parameter['redis'].keys("*")
			return [{"id":i, "data":await parameter['redis'].get(i)} for i in kunci]
	
	async def DelData(kimin, **parameter):
		if isinstance(parameter['kunci'], list):
			for i in parameter['kunci']:
				await parameter['redis'].delete(i)
		else:
			await parameter['redis'].delete(parameter['kunci'])