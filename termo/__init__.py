import os
import cgi
import ast
import time
import socket
import random
import mimetypes
import threading
import http, http.server
import urllib, urllib.request



mime = mimetypes.MimeTypes()

PKG_DIR = os.path.split(__file__)[0]
HTML_TEMPLATE_PATH = os.path.join(PKG_DIR, 'template.html')
PKG_WWW_DIR = os.path.join(PKG_DIR, 'www')
BRYTHON_JS_PATH = os.path.join(PKG_WWW_DIR, 'brython.js')
BRYTHON_STDLIB_JS_PATH = os.path.join(PKG_WWW_DIR, 'brython_stdlib.js')
BRYTHON_JS_URL = 'https://cdn.jsdelivr.net/gh/brython-dev/brython/www/src/brython.min.js'
BRYTHON_STDLIB_JS_URL = 'https://cdn.jsdelivr.net/gh/brython-dev/brython/www/src/brython_stdlib.min.js'
TERMO_BRYTHON_PATH = os.path.join(PKG_WWW_DIR, 'termo.py')
TERMO_JS_PATH = os.path.join(PKG_WWW_DIR, 'termo.js')

class Vars:
	main_brython_script = None
	obj = None



def app(mainfp, gui='index.py'):

	Vars.main_brython_script = gui

	cwd = os.path.split(mainfp)[0]
	os.chdir(cwd)

	lastpid_fp = os.path.join(cwd, '.lastpid')

	if os.path.exists(lastpid_fp):

		with open(lastpid_fp, 'r') as f:
			pid = f.read()

		if pid.isdigit():
			try:
				os.kill(int(pid), 9)
			except ProcessLookupError:
				pass

		os.remove(lastpid_fp)

	with open(lastpid_fp, 'w') as f:
		f.write(str(os.getpid()))


	def class_decorator(cls):
		
		Vars.obj = cls()

		r = 0
		while r == 0:
			port = random.randrange(1024, 2**16)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			r = s.connect_ex(('localhost', port)) # 0 es que el puerto está siendo escuchado (se está utilizando)
			s.close()

		threading.Thread(target=open_browser_when_server_on, args=[port], daemon=True).start()
		threading.Thread(target=lambda:(input(f'\nApp running ({os.path.split(mainfp)[-1]}) -> [ENTER] to close it.\n\n'), print('- close the browser manually -\n'), os._exit(0)), daemon=True).start()
		run_server(port)


	return class_decorator




def open_browser_when_server_on(port):

	while True:
		try:
			urllib.request.urlopen(f'http://localhost:{port}')
			break
		except urllib.error.URLError:
			time.sleep(0.1)
	
	os.system(f'am start -a android.intent.action.VIEW -d http://localhost:{port} > /dev/null') # f'termux-open-url http://localhost:{port}'




def run_server(port):
	with http.server.HTTPServer(('localhost', port), Server) as httpd:
		httpd.serve_forever()




class Server(http.server.SimpleHTTPRequestHandler):

	def log_request(self, *args):
		pass

	def _404(self):

		data = '<!DOCTYPE html><html><head><meta charset="utf-8"/><title>404 - NOT FOUND</title></head><body><h1>404 - NOT FOUND</h1></body></html>'.encode('utf-8')

		self.send_response(404)
		self.send_header('content-type', 'text/html')
		self.send_header('content-length', len(data))
		self.end_headers()
		self.wfile.write(data)
		return

	def do_GET(self):

		if self.path == '/':

			with open(HTML_TEMPLATE_PATH, 'r') as f:
				data = f.read().format(main_brython_script=Vars.main_brython_script).encode('utf-8')

			self.send_response(200)
			self.send_header('content-type', 'text/html')
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return

		elif os.path.exists(self.path[1:]):

			target = self.path[1:]
			with open(target, 'rb') as f:
				data = f.read()

			self.send_response(200)
			self.send_header('content-type', mime.guess_type(target)[0])
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return

		elif self.path == '/brython.js':

			if not os.path.exists(BRYTHON_JS_PATH):
				
				try:
					with request.urlopen(BRYTHON_JS_URL) as r:
						data = r.read()
				except:
					return self._404()

				with open(BRYTHON_JS_PATH, 'wb') as f:
					f.write(data)

			else:

				with open(BRYTHON_JS_PATH, 'rb') as f:
					data = f.read()

			self.send_response(200)
			self.send_header('content-type', 'text/javascript')
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return

		elif self.path == '/brython_stdlib.js':

			if not os.path.exists(BRYTHON_STDLIB_JS_PATH):
				
				try:
					with request.urlopen(BRYTHON_STDLIB_JS_URL) as r:
						data = r.read()
				except:
					return self._404()

				with open(BRYTHON_STDLIB_JS_PATH, 'wb') as f:
					f.write(data)

			else:

				with open(BRYTHON_STDLIB_JS_PATH, 'rb') as f:
					data = f.read()

			self.send_response(200)
			self.send_header('content-type', 'text/javascript')
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return

		elif self.path[1:] == Vars.main_brython_script or self.path[1:self.path.find('?')] == Vars.main_brython_script:

			if not os.path.exists(Vars.main_brython_script):
				return self._404()

			with open(Vars.main_brython_script, 'rb') as f:
				data = f.read()

			self.send_response(200)
			self.send_header('content-type', 'text/python3')
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return

		elif self.path[1:] == 'termo.py' or self.path[1:self.path.find('?')] == 'termo.py':

			if not os.path.exists(TERMO_BRYTHON_PATH):
				return self._404()

			with open(TERMO_BRYTHON_PATH, 'rb') as f:
				data = f.read()

			self.send_response(200)
			self.send_header('content-type', 'text/python3')
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return

		elif self.path == '/termo.js':

			if not os.path.exists(TERMO_JS_PATH):
				return self._404()

			with open(TERMO_JS_PATH, 'rb') as f:
				data = f.read()

			self.send_response(200)
			self.send_header('content-type', 'text/javascript')
			self.send_header('content-length', len(data))
			self.end_headers()
			self.wfile.write(data)
			return	

		else:
			return self._404()

	def do_POST(self):

		func_name = self.path[1:]

		if func_name not in Vars.obj.__class__.__dict__:
			return self._404()
		
		ctype = self.headers.get('content-type')

		if not ctype:
			kwargs = {}

		elif ctype.startswith('application/x-www-form-urlencoded'):

			clen = int(self.headers['content-length'])
			data = urllib.parse.parse_qs(self.rfile.read(clen).decode('utf-8'))
			
			kwargs = {}
			for i in data:
				kwargs[i] = data[i][0]

		elif ctype.startswith('multipart/form-data'):

			try:
				data = cgi.FieldStorage(
					fp=self.rfile,
					headers=self.headers,
					environ={'REQUEST_METHOD':'POST',
						'CONTENT_TYPE':self.headers['content-type'],
						})
			except ValueError:
				print('wrong multipart/form-data request')
				data = {}

			kwargs = {}
			for key in data.keys():

				attrs = []
				if hasattr(data[key], 'filename') and data[key].filename != None:
					attrs.append(data[key].filename)
				if hasattr(data[key], 'value') and data[key].value != None:
					attrs.append(data[key].value)

				kwargs[key] = attrs if len(attrs) > 1 else attrs[0]
			


		if self.headers.get('termo-repr-args'):
			repr_args = self.headers.get('termo-repr-args').split(';')
			for i in repr_args:
				kwargs[i] = ast.literal_eval(kwargs[i])

		_kwargs = {i:j for i,j in kwargs.items() if not i.startswith('termo-arg-')}

		args_dict = {int(i[i.rfind('-')+1:]):j for i,j in kwargs.items() if i.startswith('termo-arg-')}
		
		_args = [None]*len(args_dict)
		for k in args_dict:
			_args[k] = args_dict[k]

		r =  Vars.obj.__class__.__dict__[func_name](Vars.obj, *_args, **_kwargs)
		rtype = r.__class__.__name__

		if isinstance(r, str):
			r = r.encode('utf-8')
		elif not isinstance(r, bytes):
			r = repr(r).encode('utf-8')

		self.send_response(200)
		self.send_header('content-type', 'application/octect-stream')
		self.send_header('content-length', len(r))
		self.send_header('termo-response-type', rtype)
		self.end_headers()
		self.wfile.write(r)
		return
