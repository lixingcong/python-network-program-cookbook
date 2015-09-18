#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/12/2015 9:59p
# 说明：这是一个回显服务端+客户端,运行在单机即可
# 继承一个ForkingMixIn类,异步处理

# TODO：弄清楚那个socketserver模块里面的几个基本函数是干什么用的

import os
import socket
import threading
import SocketServer

SERVER_HOST='0.0.0.0'
# using port 0 indicate that tell the kernel to pick up a port dynamically
SERVER_PORT=0
BUF_SIZE=1024
ECHO_MSG="hello,i am a test message"

class ForkingClient():
	def __init__(self,ip,port):
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect((ip,port))
		
	def run(self):	
		# send data to the server
		current_pid=os.getpid()
		print "PID %s is sending echo message to the server:%s"%(current_pid,ECHO_MSG)
		send_data_len=self.sock.send(ECHO_MSG)
		print "Sent: %d chars..."%send_data_len
		response=self.sock.recv(BUF_SIZE)
		print "PID %s recieved %s"%(current_pid,response[5:])
		
		
	def shutdown(self):	
		self.sock.close()
				
class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):		
	# you can just redefine a handle function here
	def handle(self):
		data=self.request.recv(BUF_SIZE)
		current_pid=os.getpid()
		response='%s: %s'%(current_pid,data)
		print "Server sending response [current_pid:data]=[%s]"%response
		self.request.send(response)
		return
		
# The class "forkingserver" inherited from two classes,and its init function is TCPServer.__init__()
# the class "socketserver.forkingminxin" have no init function.
# you can visit http://zhidao.baidu.com/question/572258895.html to get more details		
class ForkingServer(SocketServer.ForkingMixIn,SocketServer.TCPServer):
	'''Nothing adding here, inherited everything necessary from parents'''
	pass
	
def main():	
	# launch the server
	server=ForkingServer((SERVER_HOST,SERVER_PORT),ForkingServerRequestHandler)
	ip,port=server.server_address # retrieve the port number
	server_thread=threading.Thread(target=server.serve_forever)
	server_thread.setDaemon(True)
	server_thread.start()
	print "Server loop running PID: %s"%os.getpid()
	
	# launch the client
	client1=ForkingClient(ip,port)
	client1.run()
	
	client2=ForkingClient(ip,port)
	client2.run()

	
	# clean them up
	server.shutdown()
	client1.shutdown()
	client2.shutdown()
	server.socket.close()
	
if __name__=='__main__':
    main()

