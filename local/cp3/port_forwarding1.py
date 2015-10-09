#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月1日 下午6:54:24
# 说明：使用一个asyncore.dipatcher类进行端口转发，貌似没有什么卵用。流量总是转发失败。或者提示length不对


import argparse
import socket
import asyncore

LOCAL_SERVER_HOST = 'localhost'
REMOTE_SERVER_HOST = 'breed.hackpascal.net'
BUFSIZE = 4096

class PortForawarder(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, backlog = 5):
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)
        
    def handle_accept(self):
        conn, addr = self.accept()
        print "Connected to ", addr
        Sender(Receiver(conn), self.remoteip, self.remoteport)
        
class Receiver(asyncore.dispatcher):
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = ''
        self.to_remote_buffer = ''
        self.sender = None        
        
    def handle_connect(self):
        pass
    
    def handle_read(self):
        read = self.recv(BUFSIZE)
        self.from_remote_buffer += read
        
    def writable(self):
        return (len(self.to_remote_buffer) > 0)
    
    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[sent:]
        
    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()
            
class Sender(asyncore.dispatcher):
    def __init__(self, reciever, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = reciever
        reciever.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))
        
    def handle_connect(self):
        pass
    def handle_read(self):
        read = self.recv(BUFSIZE)
        self.receiver.to_remote_buffer += read
    
    # Don't change the method name of "writeable"
    # Because it inheritated from father class    
    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)
    
    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]
        
    def handle_close(self):
        self.close()
        self.receiver.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Stackless Socket Server Example')
    parser.add_argument('--local_host', action = "store", dest = "local_host", default = LOCAL_SERVER_HOST)
    parser.add_argument('--local_port', action = "store", dest = "local_port", type = int, required = True)
    parser.add_argument('--remote_host', action = "store", dest = "remote_host", default = REMOTE_SERVER_HOST)
    parser.add_argument('--remote_port', action = "store", dest = "remote_port", type = int, default = 80)
    given_args = parser.parse_args()
    local_host, remote_host = given_args.local_host, given_args.remote_host
    local_port, remote_port = given_args.local_port, given_args.remote_port
    print "Starting Port Forwarding...\nlocal %s:%s => remote %s:%s" % (local_host, local_port, remote_host, remote_port)
    PortForawarder(local_host, local_port, remote_host, remote_port)
    asyncore.loop()      
