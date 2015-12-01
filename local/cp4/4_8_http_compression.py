    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午9:56:38
# 说明：把内容压缩成gzip格式再提供给访问者
# 访问localhost:8800即可看到压缩版本的Hello world

import argparse
import sys
import gzip
import cStringIO
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800
HTML_CONTENT = """<html><body><h1>Compressed Hello World!</h1></body></html>"""

class RequestHandler(BaseHTTPRequestHandler):
    # Custom request handler
    def do_GET(self):
        # Handler for the GET requests
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Encoding', 'gzip')
        zbuf = self.compress_buffer(HTML_CONTENT)
        sys.stdout.write("Content-Encoding: gzip\r\n")
        self.send_header('Content-Length', len(zbuf))
        self.end_headers()
        
        # Send the message to browser
        zbuf = self.compress_buffer(HTML_CONTENT)
        sys.stdout.write("Content-Encoding: gzip\r\n")
        sys.stdout.write("Content-Length: %d\r\n" % (len(zbuf)))
        sys.stdout.write("\r\n")
        self.wfile.write(zbuf)
        return
    
    def compress_buffer(self, buf):
        zbuf = cStringIO.StringIO()
        zfile = gzip.GzipFile(mode = 'wb', fileobj = zbuf, compresslevel = 6)
        zfile.write(buf)
        zfile.close()
        return zbuf.getvalue()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Simple Http Server with gzip compression')
    parser.add_argument('--port', action = 'store', dest = 'port', type = int, default = DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    server_addr = (DEFAULT_HOST, port)
    server = HTTPServer(server_addr, RequestHandler)
    server.serve_forever()
        
