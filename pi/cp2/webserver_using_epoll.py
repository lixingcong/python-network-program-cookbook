#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年9月29日 下午4:06:56
# 说明：这是个简单的服务器，向每一个连接服务器的网页浏览器返回一行文本
# 使用：执行python xx.py --port=4000然后浏览器访问localhost:4000

import socket
import select
import argparse

SERVER_HOST = "localhost"

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
# This Content-length should be calculated accurately.
# If the number set is larger than the fact ,the browser will say its length is incorrect.
# Smaller is ok.
SERVER_RESPONSE = b"""HTTP/1.1 200 OK\r\n\Date: Mon, 1 Apr 2013 01:01:02
GMT\r\nContent-Type: text/plain\r\nContent-Length:18\r\n\r\nHello from Server!"""


class EpollServer():
    # A socket server using epoll

    def __init__(self, host = SERVER_HOST, port = 0):
        # Create a socket for listening
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Re-use the address and port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)
        # Set the socket un-blocking
        self.sock.setblocking(0)
        # No Delay. Any data in socket.send()function 
        # will be sent immediately instead of being cached
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Create a handle of epoll
        self.epoll = select.epoll()
        # Register a READABLE event for listening to socket
        self.epoll.register(self.sock.fileno(), select.EPOLLIN)
        print "Started Epoll Server"

    def run(self):
        try:
            connections, requests, responses = {}, {}, {}
            while True:
                # Scan for dealing,timeout is set to 1 second
                events = self.epoll.poll(1)
                for fileno, event in events:
                    # if the the listening port is activated
                    if fileno == self.sock.fileno():
                        connection, address = self.sock.accept()
                        # set un-blocking
                        connection.setblocking(0)
                        self.epoll.register(connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = b''
                        responses[connection.fileno()] = SERVER_RESPONSE
                    # if READABLE event is activated:
                    elif event & select.EPOLLIN:
                        requests[fileno] += connections[fileno].recv(1024)
                        print "The server got a request from client:"
                        # EOL1 is for Unix,EOL2 is for Win.
                        # Judge if the return exist.
                        if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                            # change the file description to EPOLLPUT
                            self.epoll.modify(fileno, select.EPOLLOUT)
                            # decode()[-2:]表示解码后截取到倒数第二个字符
                            print ('-' * 40 + '\n' + requests[fileno].decode()[:-2])
                    # if WRITEABLE event is activated
                    elif event & select.EPOLLOUT:
                        # Send data to the client
                        byteswritten = connections[fileno].send(responses[fileno])
                        print "Now server is wiriting to the client.\nthe bytewritten is", byteswritten
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            self.epoll.modify(fileno, 0)
                            # Close the connection and disable READ and WRITE
                            connections[fileno].shutdown(socket.SHUT_RDWR)
                    # if hung up(client closed)
                    elif event & select.EPOLLHUP:
                        self.epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        finally:
            self.epoll.unregister(self.sock.fileno())
            self.epoll.close()
            self.sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Epoll Server")
    parser.add_argument('--port', action = "store", dest = "port", type = int, required = True)
    given_args = parser.parse_args()
    port = given_args.port
    server = EpollServer(host = SERVER_HOST, port = port)
    server.run()
