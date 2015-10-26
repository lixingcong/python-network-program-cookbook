    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月16日 下午7:59:53
# 继承HTTPServer类，建立一个简易服务器
# 说明：linux下的服务器，在windows测试会失败，莫名其妙。
# 使用方法：运行后打开localhost:4000，看到hello from server

import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 4000

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		# send the message to the browser
		self.wfile.write("Hello from server!")
		return

class CustomHTTPServer(HTTPServer):
	def __init__(self, host, port):
		server_address = (host, port)
		HTTPServer.__init__(self, server_address, RequestHandler)

def run_server(port):
		try:
			server = CustomHTTPServer(DEFAULT_HOST, port)
			print "Custom HTTP Server started on port %s" % port
			server.serve_forever()
		except Exception, err:
			print "Error :%s" % err
		except KeyboardInterrupt:
			print "Server Interrupted and is shutting down..."
			server.socket.close()
			
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Simple Http server example")
	parser.add_argument('--port', action = "store", dest = "port", type = int, default = DEFAULT_PORT)
	given_args = parser.parse_args()
	port = given_args.port
	run_server(port)
