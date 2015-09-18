#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/11/2015 7:02p
# 说明：修改socket发送和接收的缓冲大小

import socket

SEND_BUF_SIZE=4096
RECV_BUF_SIZE=4096

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
bufsize=sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
print "buffer size [before] :",bufsize

sock.setsockopt(socket.SOL_TCP,socket.TCP_NODELAY,1)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,SEND_BUF_SIZE)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RECV_BUF_SIZE)

bufsize=sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
print "buffer size [after] :",bufsize
