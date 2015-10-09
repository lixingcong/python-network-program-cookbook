    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月1日 下午4:31:05
# 说明：本例子依赖diesel高于3.0版本，因为需要编译，所以还需下载py-dev依赖
# sudo apt-get install python-dev diesel
# 用法：python xx.py --port=8800
# 然后新建一个终端telnet localhost 8800

import diesel
import argparse

class EchoServer(object):
    def handler(self, remote_addr):
        host, port = remote_addr[0], remote_addr[1]
        print "Echo Client connected from: %s:%d" % (host, port)
        while True:
            try:
                message = diesel.until_eol()
                your_message = ':'.join(['You said', message])
                diesel.send(your_message)
            except Exception, e:
                print "error:", e
                break
            
def main(server_port):
    app = diesel.Application()
    server = EchoServer()
    app.add_service(diesel.Service(server.handler, server_port))
    try:
        app.run()
    except:
        print "exit."
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Echo Server with diesel")
    parser.add_argument('--port', action = "store", dest = "port", type = int, required = True)
    given_args = parser.parse_args()
    port = given_args.port
    main(port)
        
