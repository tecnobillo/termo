import os
import cgi
import ast
import time
import socket
import random
import mimetypes
import threading
import subprocess
import webbrowser
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
	wb_name = None
	app_title = None
	app_icon = None
	brython_conf = None



def app(mainfp, gui='index.py', webapp=False, port=None, title='Termo-App', icon=None, brython_conf=dict(cdn=False, stdlib=True)):

	Vars.app_title = title
	Vars.app_icon = icon
	Vars.main_brython_script = gui

	Vars.brython_conf = ''

	if brython_conf['cdn'] == True:
		Vars.brython_conf += f'<script type="text/javascript" src="{BRYTHON_JS_URL}"></script>'
		if brython_conf['stdlib'] == True:
			Vars.brython_conf += f'<script type="text/javascript" src="{BRYTHON_STDLIB_JS_URL}"></script>'
	elif brython_conf['cdn'] == False:
		Vars.brython_conf += f'<script type="text/javascript" src="/brython.js"></script>'
		if brython_conf['stdlib'] == True:
			Vars.brython_conf += f'<script type="text/javascript" src="/brython_stdlib.js"></script>'

	cwd = os.path.split(os.path.abspath(mainfp))[0]
	if cwd: # cwd == '' si se ha ejecutado el script desde su propio directorio
		os.chdir(cwd)

	lastpid_fp = os.path.join(cwd, '.lastpid')

	if os.path.exists(lastpid_fp):

		with open(lastpid_fp, 'r') as f:
			pid = f.read()

		if pid.isdigit():
			try:
				if os.name == 'posix':
					os.kill(int(pid), 9)
				elif os.name == 'nt':
					subprocess.run(f'taskkill /f /t /pid {pid}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			except ProcessLookupError:
				pass
			except OSError:
				pass

		os.remove(lastpid_fp)

	with open(lastpid_fp, 'w') as f:
		f.write(str(os.getpid()))


	r = 0
	while r == 0:
		_port = port or random.randrange(1024, 2**16)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		r = s.connect_ex(('localhost', _port)) # 0 es que el puerto está siendo escuchado (se está utilizando)
		s.close()

	port = _port


	def class_decorator(cls):
		
		Vars.obj = cls()

		if not webapp:
			threading.Thread(target=open_browser_when_server_on, args=[port], daemon=True).start()

		if os.name == 'posix' and os.environ.get('PREFIX') and 'com.termux' in os.environ['PREFIX']:

			threading.Thread(target=lambda:(input(f'\nApp running ({os.path.split(mainfp)[-1]}) -> [ENTER] to close it.\n\n'), print('- close the browser manually -\n'), os._exit(0)), daemon=True).start()
		
		elif not webapp:

			def check_webbrowser_alive():
				while True:
					time.sleep(5)
					command = f'pgrep -f {Vars.wb_name}'.split() if os.name == 'posix' else ['cmd', '/c', f'tasklist | findstr {Vars.wb_name}']
					r = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8').strip()
					if not r:
						os._exit(0)

			threading.Thread(target=check_webbrowser_alive, daemon=True).start()
		
		run_server('0.0.0.0' if webapp else 'localhost', port)


	return class_decorator




def open_browser_when_server_on(port):

	host = f'http://localhost:{port}'

	while True:
		try:
			urllib.request.urlopen(host)
			break
		except urllib.error.URLError:
			time.sleep(0.1)
	
	if os.name == 'posix' and os.environ.get('PREFIX') and 'com.termux' in os.environ['PREFIX']:

		os.system(f'$(am start -a android.intent.action.VIEW -d {host} > /dev/null) || termux-open-url {host} || xdg-open {host}')

	elif os.name == 'posix':

		sp = subprocess.run('xdg-settings get default-web-browser', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		res = sp.stdout.decode('utf-8').strip()
		wb = Vars.wb_name = os.path.splitext(res)[0]

		if wb == 'google-chrome' or 'chrome' in wb or 'chromium' in wb:
			command = f'{wb} --app="{host}"'

		elif wb == 'firefox':
			command = f'{wb} --new-window {host}'

		else:
			command = f'{wb} {host}'

		subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	elif os.name == 'nt':

		msedge_paths = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Microsoft/Edge/Application/msedge.exe'
		
		command = None

		for msedge_path in msedge_paths:
			if os.path.exists(msedge_path):
				command = f'"{msedge_path}" --app="{host}"'
				Vars.wb_name = os.path.split(msedge_path)[-1]
				break

		if not command:
			r = subprocess.run('reg QUERY HKEY_CLASSES_ROOT\htmlfile\shell\open\command /ve', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8').strip()
			wb_path = r[r.find('"')+1:r.rfind('"')]
			command = f'"{wb_path}" {host}'
			Vars.wb_name = os.path.split(wb_path)[-1]

		if command:
			subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		else:
			webbrowser.open(host)

	else:
		print('undefined os')
		os._exit(0)



def run_server(host, port):
	with http.server.HTTPServer((host, port), Server) as httpd:
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
				data = f.read().format(app_title=Vars.app_title, brython_conf=Vars.brython_conf, main_brython_script=Vars.main_brython_script).encode('utf-8')

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
					with urllib.request.urlopen(BRYTHON_JS_URL) as r:
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
					with urllib.request.urlopen(BRYTHON_STDLIB_JS_URL) as r:
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

		elif self.path == '/favicon.ico' and Vars.app_icon:

			with open(Vars.app_icon, 'rb') as f:
				data = f.read()

			self.send_response(200)
			self.send_header('content-type', 'image/x-icon')
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
