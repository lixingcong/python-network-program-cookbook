#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/12/2015 8:47p
# 说明：不使用任何第三方的库创建一个简单的sntp客户端

import socket
import struct
import sys
import time

NTP_SERVER='time-nw.nist.gov'
TIME1970=2208988800L

def sntp_client():
	client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	data='\x1b'+47*'\0'
	client.sendto(data,(NTP_SERVER,123))
	print "sent request."
	data,address=client.recvfrom(1024)
	if data:
		print "respone from :",address
	# 可以查一下 stuct.unpack 用法	
	# 对字节型数据进行解包,方便传输
	# 该模块的主要作用就是对python基本类型值与用python字符串格式表示的C struct类型间的转化
 	t=struct.unpack('!12I',data)[10]
	t-=TIME1970	
	print "Time is %s"%time.ctime(t) 
	
if __name__=='__main__':
    sntp_client()
