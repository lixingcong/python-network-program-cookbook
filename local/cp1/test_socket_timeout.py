#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/9/2015 4:20p
# 说明：测试一下处理超时
import socket

def test_socket_timeout():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print "default socket timeout: %s"%s.gettimeout() 
	s.settimeout(100)
	print "Now socket timeout: %s"%s.gettimeout()
	
if __name__=='__main__':	
	test_socket_timeout()
