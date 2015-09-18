#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/9/2015 3:55p
# 说明：转换ipv4地址

import socket
from binascii import hexlify

def convert_ipv4_adress():
	for ip_add in ['127.0.0.1','192.168.1.1']:
		packed_ip_add=socket.inet_aton(ip_add)
		unpacked_ip_add=socket.inet_ntoa(packed_ip_add)
		print "IP address : %s > Packed: %s , Unpacked :%s"%(ip_add,hexlify(packed_ip_add),unpacked_ip_add)
		
if __name__=='__main__':		
	convert_ipv4_adress()
