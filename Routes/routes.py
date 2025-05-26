from fastapi import Request, WebSocket, Response
from itertools import cycle

class Routes:
	temp_db = {"websocket": {}, "cache":{}}  # Static property
	temp_func = {"redis":{}}
	def __init__(kimin, loader, **parameter):
		kimin.loader, kimin.parameter = loader, parameter
		middle = loader.Load('middle')
		template = loader.Load('template')
		kimin.version = ['v1']
		sesi = kimin.loader.Load('session')
		
		server = kimin.parameter['server']
		if not hasattr(server, '_session_middlerware'):
			server.add_middleware(sesi, secret_key=kimin.parameter['cfg']['server']['secret_key'])
			server._session_middlerware = True
		
		if not hasattr(server, '_cors_middlerware'):
			server.add_middleware(
				middle,
				allow_origins=["*"],  # Anda bisa mengganti "*" dengan domain ngrok spesifik untuk keamanan
				allow_methods=["*"],
				allow_headers=["*"],
			)
			server._cors_middlerware = True
		
		kimin.parameter['temp_db'] = Routes.temp_db
		kimin.parameter['temp_func'] = Routes.temp_func
		kimin.template = template(directory=kimin.parameter['cfg']['server']['template_path'])
		# kimin.manager = kimin.modul['ws_connector'](modul=kimin.modul, **kimin.parameter)
		
		# kimin.parameter['server'].add_event_handler("startup", kimin.OnStart)
		# kimin.parameter['server'].add_event_handler("shutdown", kimin.OnExit)
		
		kimin.parameter['limiter'] = {
			"durasi":60,
			"threshold":{
				"ip":3,
				"fp":3,
			},
			"max":{
				"ip":1000,
				"fp":1000,
			},
			"prefix":{
				"ip":"rate_limit:ip:",
				"fp":"rate_limit:fp:"
			}
		}
		# kimin.parameter['cookie'] = ['id_gcp', 'usr_key', 'id_hcp']
		# kimin.parameter['cookie_exp'] = 3600
		# kimin.parameter['request_exp'] = 1800
		# kimin.parameter['limiter'] = {
			# "bot":{
				# "count":3, "duration":600, "block":600
			# },
			# "human":{
				# "count":120, "duration":60, "block":120
			# }
		# }
		
		# @kimin.parameter['server'].exception_handler(404)
		# async def Handler404(request: Request, exc):
			# return kimin.template.TemplateResponse("content/404.html", {"request":request}, status_code=404)
		
		# if not getattr(server, '_middleware_registered', False):
			# server._middleware_registered = True
			
			# @server.middleware("http")
			# async def log_requests(request: Request, call_next):
				# if request.url.path.startswith("/static") or request.url.path.endswith((".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".woff2", ".ttf")):
					# return await call_next(request)
				# security = kimin.loader.Load('secure_request')
				# cek = await security(loader=kimin.loader).Execute(
					# request=request, config=kimin.parameter['limiter'], 
					# redis=kimin.parameter['temp_func']['redis']
				# )
				# gid = request.cookies.get('gid')
				# if not cek['status']:
					# fi_json = kimin.loader.Load('f_json')
					# return fi_json(
						# content={"message":cek.get('data', 'No Identifier'), "status":cek['status']},
						# status_code=cek['code']
					# )
				# response = await call_next(request)
				# if not gid or not gid == cek['id_sesi']:
					# datetime = kimin.loader.Load('datetime')
					# response.set_cookie(
						# key="gid",
						# value=cek['id_sesi'],
						# httponly=True,
						# secure=kimin.parameter['cfg']['server']['https'],
						# samesite='Lax',
						# max_age=3600,
						# expires=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600)
					# )
				# return response
		
		# if not getattr(server, '_ws_route', False):
			# server._ws_route = True
			# @server.websocket("/kimin-access/{client_id}")
			# async def Ws_Handler(websocket: WebSocket, client_id:str):
				# print(f"New connection attempt from client_id: {client_id}")
				# konek = await kimin.manager.Konek(ws=websocket, id=str(client_id))
				# try:
					# if konek['status']:
						# while True:
							# data = await websocket.receive_json()
							# await kimin.manager.OnMessage(data)
					# else:
						# await kimin.manager.Terminate(id=client_id)
				# except kimin.modul['WebSocketDisconnect']:
					# await kimin.manager.Terminate(id=client_id)
	
	
	async def Robot_Txt(kimin):
		return """User-agent: *
Disallow: /"""
	
	async def Home(kimin, request: Request):
		data = {
			"cfg":
				{
					"title":"Kimin Stream Server"
				}
			}
		return kimin.template.TemplateResponse("content/home.html", {"request":request, "data":data})
		
	async def Player(kimin, path, request: Request):
		data = {
			"cfg":
				{
					"title":path.replace("-"," ")
				}
			}
		return kimin.template.TemplateResponse("content/player.html", {"request":request, "data":data})
	
	async def API(kimin, version, mode, request: Request, response: Response):
		hasil = {"status": False}
		api = kimin.loader.Load('api')
		not_found = kimin.loader.Load('404')
		if version in kimin.version:
			return await api(loader=kimin.loader, **kimin.parameter).Execute(request=request, response=response, mode=mode)
		else:
			raise not_found(status_code=404)
		return hasil
	
	# async def API(kimin, version, mode, request: Request):
		# hasil = {"status": False}
		# if version in kimin.version:
			# x = await kimin.api.Data(request, mode)
			# return x
		# return hasil
