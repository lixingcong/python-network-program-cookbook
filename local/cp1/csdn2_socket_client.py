#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/9/2015 7:46p
# 说明：多线程socket范例

import socket

def Main():
	try:
		# Address Family : AF_INET (this is IP version 4 or IPv4)
		# Type :  SOCK_STREAM (this means connection oriented TCP protocol)
        #         SOCK_DGRAM indicates the UDP protocol. 
		new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to creat socket. Error code:', str(msg[0]), 
		print 'Error message:', msg[1]
		return
		
	new_socket.connect(('192.168.199.118',8001))
	print 'Socket Connected.' 
	# Send some data to remote server | socket.sendall(string[, flags]) 
	import time
	while 1:
		message = raw_input('message to pi:')
		try:
			new_socket.sendall(message)
		except socket.error:
			print 'Send fail.'
			break 
		print 'Message send successfully.'
		time.sleep(1)
		#Receive data | socket.recv(bufsize[, flags]) 
		reply = new_socket.recv(4096)
		print reply
    
    #Close the socket
	new_socket.close()
    
    
if __name__ == '__main__':
    Main()
