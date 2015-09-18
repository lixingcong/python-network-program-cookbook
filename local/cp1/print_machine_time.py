#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/11/2015 8:13p
# 说明：从网络上获得的时间,使用库,接下来例子是不用任何库写一个ntp客户端

import ntplib
from time import ctime

def print_time():
	ntp_client=ntplib.NTPClient()
	# Microsoft NTP server
	response=ntp_client.request('time-nw.nist.gov')
	print ctime(response.tx_time)
	
if __name__=='__main__':
    print_time()	
