    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月9日 下午8:50:08
# 说明：linux相连的套接字，socketpair实验。适用于两个脚本通过两个进程进行彼此通讯
# 关联知识点：linux下的进程间通讯

import socket
import os

BUFSIZE = 1024

def test_socketpair():
    parent, child = socket.socketpair()
    pid = os.fork()
    try:
        if pid:
            print "@Parent, sending message..."
            child.close()
            parent.sendall("hello from parents！")
            response = parent.recv(BUFSIZE)
            print "Response from child", response
            parent.close()
        else:
            print "@Child, waiting for message from parent"
            parent.close()
            message = child.recv(BUFSIZE)
            print "Message from parent:", message
            child.sendall("hello from child !")
            child.close()
    except Exception, err:
        print "Error:", err
        
if __name__ == "__main__":
    test_socketpair()        
