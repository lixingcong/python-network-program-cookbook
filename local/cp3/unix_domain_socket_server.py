    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月9日 下午8:59:06
# 说明：Unix域套接字处理两个进程间的通讯。需要配对一个uds客户端进行实验
# IPC(Inter-Process Communication,进程间通信) 

import socket
import os 

SERVER_PATH = "/tmp/py_unix_socket_server"

def run_unix_domain_socket_server():
    if os.path.exists(SERVER_PATH):
        os.remove(SERVER_PATH)
    print "Starting unix domain server."
    server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server.bind(SERVER_PATH)
    
    print "Listening on path: %s" % SERVER_PATH
    while True:
        datagram = server.recv(1024)
        if not datagram:
            break
        else:
            print "-"*20
            print datagram
        if "DONE" == datagram:
            break
    print "-"*20
    print "Server is shutting down now..."
    server.close()
    os.remove(SERVER_PATH)
    print "Server shutdown and path removed"
    
if __name__ == "__main__":
    run_unix_domain_socket_server()    
