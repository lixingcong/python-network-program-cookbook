#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/12/2015 9:36p
# 说明：1.14一个简单的回显客户端程序

import socket
import sys

def echo_system_client():
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(('192.168.0.118',8001))
	try:
		message="this is a test message will be echoed to the server please wait for a while"
		sock.sendall(message)
		amount_recv=0
		amount_expect=len(message)
		while amount_recv<amount_expect:
			data=sock.recv(16)
			amount_recv+=len(data)
			print "Recieved %s"%data
	except socket.error,e:	
		print "socket error: %s"%e
	except Exception,e:
		print "other exception: ",e
		
	# try...finally的用处是无论是否发生异常都要确保资源释放代码的执行。 
	# finally的代码是一定被执行的
	finally:
		print "closing connection to the server"
		sock.close()
		
if __name__=='__main__':
    echo_system_client()
			
