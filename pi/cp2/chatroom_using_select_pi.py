    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-Stamp: 9/18/2015 8:24p
# 说明：使用select 模块解决创建单独进程或线程的消耗大量cpu问题
# 实际上cpu占用率还是很高的，ubuntu 14.04 @ 3317u 占用25%的资源
# 本例子用于，处理上百个聊天室客户端
# 使用方法：在本地开通三个终端：分别敲入python 1.py --name=server --port=8999
# python 1.py --name=lixingcong--port=8999
# python 1.py --name=carl --port=8999
# 然后在客户端进行发送
# 缺点很明显：每次一旦有人发送消息会把当前窗口里面消息清空。。。终端就是这样的。
# TODO:改善客户端忽然断开连接导致全部异常。

import select
import socket
import sys
import signal
import cPickle
import struct
import argparse

SERVER_HOST = '127.0.0.1'
CHAT_SERVER_NAME = 'server'

# Some utilities
def send(channel, *args):
	# Python object serialization,using cPickle(the same as pickle)
	# similary to htonl or ltonh
	# in order to transform list to bin code serialization
	buffer1 = cPickle.dumps(args)
	value = socket.htonl(len(buffer1))
	size = struct.pack("L", value)
	# Send length of data first
	channel.send(size)
	# Then send data.
	channel.send(buffer1)
	
# the reservse operation of send(channel,*args)	
def receive(channel):	
	# Calc the length of a package of unsigned long
	size = struct.calcsize("L")
	# Receive the size package
	size = channel.recv(size)
	try:
		# Try to unpack the size
		size = socket.ntohl(struct.unpack("L", size)[0])
	except struct.error, e:
		print e
		return ''
	buf = ""	
	while len(buf) < size:
		buf = channel.recv(size - len(buf))
	return cPickle.loads(buf)[0]	
	
class ChatServer(object):	
	# An example chat server using select
	def __init__(self, port, backlog = 5):
		self.clients = 0
		# Clientmap is a dictionary
		self.clientmap = {}
		# list output sockets
		self.outputs = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((SERVER_HOST, port))
		print "Listening to port %s..." % port 
		self.server.listen(backlog)
		# Catch keyboard interrupts
		signal.signal(signal.SIGINT, self.sighandler)
		
	def sighandler(self, signum, frame):	
		# Clean up clients ouputs 
		# Close the server
		print "shutting down the server..."
		# Close the existing clients sockets
		for output in self.outputs:
			output.close()
		self.server.close() 
		
	def get_client_name(self, client):	
		# Return the name of client
		info = self.clientmap[client]
		host, name = info[0][0], info[1]
		return '@'.join((name, host))
		
	# define some important methods of class ChatServer	
	def run(self):  
		inputs = [self.server, sys.stdin]
		self.outputs = []
		running = True
		print "run"
		while running:
			try:
				readable, writeable, exceptional = select.select(inputs, self.outputs, [])
			except select.error , e:
				print e
				break
			for sock in readable: 
				if sock == self.server:
					# handle the server socket
					client, address = self.server.accept()
					print "Chat Server: Got connection %d from %s" % (client.fileno(), address)
					# Read the login name
					temp = receive(client)
					cname = temp.split('NAME: ')[1]
					# Compute client name and send back
					self.clients += 1
					# ATTENTION: "CLIENT: "then follow a space ,it has a strong relationship to the following code "data.split("CLIENT: ")"
					send(client, 'CLIENT: ' + str(address[0]))
					inputs.append(client)
					self.clientmap[client] = (address, cname)
					# Send joining information to other clients
					msg = "\n(Conneted: New client (%d) from %s)" % (self.clients, self.get_client_name(client))
					for output in self.outputs:
						send(output, msg)
					self.outputs.append(client)
				elif sock == sys.stdin: 
					# handle standard input
					sys.stdin.readline()
					running = False
				else:
					# handle all other sockets
					try:
						data = receive(sock)
						if data:
							# Send as new client's message
							msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
							# Send data to all except ourself
							for output in self.outputs:
								if output != sock:
									send(output, msg)
						else:   
							print "Chat Server: %d hung up" % sock.fileno()
							self.client -= 1
							sock.close()
							inputs.remove(sock)
							# Sending client leaving information to others
							msg = "\n(Now hung up: Client from %s)" % self.get_client_name(sock)
							print msg
							for output in self.outputs:
								send(output, msg)
					except socket.error , e :
						# Remove
						inputs.remove(sock)
						self.outputs.remove(sock)
		self.server.close()   
		
class ChatClient(object):
	def __init__(self, name, port, host = SERVER_HOST):
		self.name = name
		self.connected = False
		self.host = host
		self.port = port
		# Initial prompt
		self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']>'
		# Connect to server at port
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((SERVER_HOST, self.port))
			print "Now connected to chat server at port %d" % self.port
			self.connected = True
			# Send my name
			send(self.sock, "NAME: " + self.name)
			data = receive(self.sock)
			# Contains client address ,set it
			addr = data.split('CLIENT: ')[1]
			self.prompt = '[' + '@'.join((self.name, addr)) + ']>'
		except socket.error, e: 
			print "Failed to connect to chat server @ port %d %s" % (self.port, e)
			sys.exit(1)
			
	def run(self):		
		# Chat client main loop
		print "run"
		while self.connected:
			try:
				sys.stdout.write(self.prompt)
				sys.stdout.flush()
				# Wait for input from stdin and socket
				readable, writeable, exceptional = select.select([0, self.sock], [], [])
				for sock in readable: 
					if sock == 0:
						data = sys.stdin.readline().strip()
						if data:send(self.sock, data)
					elif sock == self.sock: 
						data = receive(self.sock)
						if not data:
							print "Client shutting down."
							self.connected = False
							break
						else: 
							sys.stdout.write(data + '\n')
							sys.stdout.flush()
			except KeyboardInterrupt:
				print "Client interrupts."
				self.sock.close()
				break
				
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Socket server example')
	parser.add_argument('--name', action = "store", dest = "name", required = True)
	parser.add_argument('--port', action = "store", dest = "port", type = int, required = True)
	given_args = parser.parse_args()
	
	port = given_args.port
	name = given_args.name
	if name == CHAT_SERVER_NAME:
		server = ChatServer(port)
		server.run()
	else : 
		client = ChatClient(name = name, port = port)
		client.run()
		
	
					
