#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/9/2015 3:58p
# 说明：通过指定端口和协议找到服务名

import socket

def find_service_name():
	protocol_name='tcp'
	for port in [80,22,25,79]:
		print "Port %s => service name: %s"%(port,socket.getservbyport(port,protocol_name))
	print "port 53 => service name: %s"%socket.getservbyport(53,'udp')
	
if __name__=='__main__':	
	find_service_name()
