#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/12/2015 9:26p
# 说明：1.14一个简单的回显客户端/服务端程序

import socket

# 每次接受的缓冲大小
data_payload=2048


def echo_system_server():
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind(('0.0.0.0',8001))
	sock.listen(3)
	while True:
		print "waiting for client"
		client,address=sock.accept()
		data=client.recv(data_payload)
		if data:
			print "data is %s"%data
			client.send(data)
			print "sent %s bytes back to %s"%(data,address)
		client.close()	
		
if __name__=='__main__':
    echo_system_server()
