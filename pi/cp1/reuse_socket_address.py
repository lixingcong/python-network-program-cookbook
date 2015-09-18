#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/11/2015 7:39p
# 如果在某个端口上面运行一个socket服务端，连接一次后便终止运行，
# 就不能在使用这个端口，如果再次连接，抛出错误。本例使用重用避免错误
# 测试方法，服务端运行本文件，另一端运行telnet 192.168.0.118 8282
# 单线程，如果另一个客户端加入，会掉线
# 说明：重用套接字地址，

import socket
import sys

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
old_reuse_state=sock.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print "Ruse state is:",old_reuse_state

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
new_reuse_state=sock.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print "New reuse state is",new_reuse_state

local_port=8282
srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
srv.bind(('0.0.0.0',local_port))
srv.listen(1)
print "listening on port",local_port

while True:
	try:
		connection,addr=srv.accept()
		print "Connnected by %s:%s"%(addr[0],addr[1])
	except KeyboardInterrupt:	
		break
	except socket.error,e:	
		print e
		
		
