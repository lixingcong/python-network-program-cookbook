    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年12月4日 下午8:27:09
# 说明：建立一个https服务器
# 依赖第三方库：先安装lib: sudo apt-get install libffi-dev
# 再安装sudo pip install pyopenssl   还有 sudo pip install six cryptography
# 生成RSA密钥：openssl genrsa -out privkey.pem 2048 
# 生成自签证书请求：openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1095 
# privkey.pem和cacert.pem文件后就可以在自己的程序中使用了
# 使用Chrome的“忽略证书错误”模式进入localhost:4443

import os
import socket
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from OpenSSL import SSL

class SecureHTTPServer(HTTPServer):
    def __init__(self,server_addrress,HandleClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx=SSL.Context(SSL.SSLv23_METHOD)
        # Location of the server private key and the server certificate
        private_key='/tmp/privkey.pem'
        ca_cert='/tmp/cacert.pem'
        ctx.use_privatekey_file(private_key)
        ctx.use_certificate_file(ca_cert)
        self.socket=SSL.Connection(ctx,socket.socket(self.server_family,self.socket_type))
        self.server_bind()
        self.server_activate()
        
class SecureHttpRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection=self.request
        self.rfile=socket._fileobject(self.request,"rb",self.rbufsize)
        self.wfile=socket._fileobject(self.request,"wb",self.wbufsize)
        
class run_server(ServerClass=SecureHTTPServer,HandlerClass=SecureHttpRequestHandler):
    # Ports needs to be accessible by user
    server_address=('',4443)
    server=ServerClass(server_address,HandlerClass)
    running_address=server.socket.getsockname()
    print "Serving HTTPS server on %s:%s"%(running_address[0],running_address[1])
    server.serve_forever()
    
if __name__=="__main__":
    run_server()
    
    
