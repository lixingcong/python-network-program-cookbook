#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/9/2015 4:26p
# 说明：执行 python THIS_FILE.py --host=www.qq.com --port=80
# 现象：返回400错误，还有一串信息
# 创建socket对象，连接服务器，发送数据，等待应答

import sys
import socket
import argparse

def main():
	#设置形参的检查
	parser=argparse.ArgumentParser(description='Socket Errot Examples')
	parser.add_argument('--host',action="store",dest="host",required=False)
	parser.add_argument('--port',action="store",dest="port",type=int,required=False)

	given_args=parser.parse_args()
	host=given_args.host
	port=given_args.port


	#建立socket
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	except socket.error,e:
		print "error creating socket!%s"%e
		sys.exit(1)
	#连接socket 
	try: 
		s.connect((host,port))
	except socket.gaierror,e:
		print "error Address-related error connecting to server: %s"%e
		sys.exit(1)
	except socket.error,e:
		print "error connection!%s"%e
		sys.exit(1)
	#发送数据 
	try: 
		s.sendall("GET HTTP/1.0\r\n\r\n")
	except socket.error,e: 
		print "error sending data: %s"%e
		sys.exit(1);
	#接收数据  
	while 1: 
		try:
			buf=s.recv(2048)
		except socket.error,e:  
			print "error recieving data: %s"%e
			sys.exit(1)
		if not len(buf): 
			break
			#写入数据 
		sys.stdout.write(buf)
	  
if __name__=='__main__': 
	main()   
