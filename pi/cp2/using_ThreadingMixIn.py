#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/18/2015 7:24p
# 说明：继承socketserver 的多线程类，对应的是forkingMixin类的处理方式

import os 
import socket
import threading 
import SocketServer

SERVER_HOST='0.0.0.0'
SERVER_PORT=0
BUF_SIZE=1024

def client(ip,port,message):
	# A client to test the threading minin server
	# Connect the server
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((ip,port))
	try:
		sock.sendall(message)
		response=sock.recv(BUF_SIZE)
		print "Client received %s"%response
	finally:
		sock.close()
		
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):		
	def handle(self):
		data=self.request.recv(1024)
		current_thread=threading.current_thread()
		response='%s: %s'%(current_thread.name,data)
		self.request.sendall(response)
		
class ThreadedTCPServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):		
	# Nothing to add here, all inherited from parents
	pass
	
if __name__=='__main__':
    # Run server
	server=ThreadedTCPServer((SERVER_HOST,SERVER_PORT),ThreadedTCPRequestHandler)
	ip,port=server.server_address
	
	# Start a thread --- One Thread per request
	server_thread=threading.Thread(target=server.serve_forever)
	
	# Exit the server thread when the main thread exits
	server_thread.daemon=True
	server_thread.start()
	print "Server Loop running on thread %s"%server_thread.name
	
	# Run Clients
	client(ip,port,"Hi.this is one")
	client(ip,port,"Hi.this is two")
	client(ip,port,"Hi.this is three")
	client(ip,port,"Hi.this is four")
	client(ip,port,"Hi.this is five")
	client(ip,port,"Hi.this is six")
	client(ip,port,"Hi.this is seven")
	
	# Server clean up
	server.shutdown()
	
	

		

		
