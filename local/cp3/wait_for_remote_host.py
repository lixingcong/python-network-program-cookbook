    #!/usr/bin/.env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月6日 下午3:43:57
# 说明：等待远程服务器在线，有bug。不清楚。

import argparse
import socket
from time import time as now

DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = "45.78.21.134"    # "lixingcong1.ddns.net"
DEFAULT_SERVER_PORT = 80

class NetServiceChecker(object):
    def __init__(self, host, port, timeout = DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def end_wait(self):
        self.sock.close()
    def check(self):
        if self.timeout:
            end_time = now() + self.timeout
        while True:
            try:
                if self.timeout:
                    next_timeout = end_time - now()
                    if next_timeout < 0:
                        return False
                    else:
                        print "Setting socket next timeout %ss" % round(next_timeout)
                        self.sock.settimeout(next_timeout)
                self.sock.connect((self.host, self.port))
            except socket.timeout, err:
                if self.timeout:
                    return False
            except socket.error, err:
                print "Exception: %s" % err
            # Everything goes well
            else:
                self.end_wait()
                return True
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'wait for network device')
    parser.add_argument('--host', action = "store", dest = "host", default = DEFAULT_SERVER_HOST)
    parser.add_argument('--port', action = "store", dest = "port", type = int, default = DEFAULT_SERVER_PORT)
    parser.add_argument('--timeout', action = "store", dest = "timeout", type = int, default = DEFAULT_TIMEOUT)
    given_args = parser.parse_args()
    host, port, timeout = given_args.host, given_args.port, given_args.timeout
    serv = NetServiceChecker(host, port, timeout = timeout)
    print "Checking the remote server %s:%s" % (host, port)
    if serv.check():
        print "Server is avaliable again!"
                
