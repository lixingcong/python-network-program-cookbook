    #!/usr/bin/env python    
# -*- coding: utf-8 -*-
# Create on: 2015年10月9日 下午9:07:03
# 说明：配合unix域套接字服务端使用的。，本例是UDS客户端。
# IPC(Inter-Process Communication,进程间通信) 

import socket
import sys

SERVER_PATH = "/tmp/py_unix_socket_server"

def run_unix_domain_socket_client():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_address = SERVER_PATH
    print "Connecting to %s" % server_address
    try:
        sock.connect(server_address)
    except socket.error, msg:
        # what is sys.stderr?
        print >> sys.stderr, msg
        sys.exit(1)
        
    try:
        message = "This is the message. This will be echoed back!"
        print "Sending [%s]" % message
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received = amount_received + len(data)
            print >> sys.stderr, "Received [%s]" % data
            
    finally:
        print "Closing client."
        sock.close()
        
if __name__ == "__main__":
    run_unix_domain_socket_client()        
            
