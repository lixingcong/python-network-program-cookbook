#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create Time: 9/9/2015 7:14p
# 套接字的创建
"""
To handle every connection we need a separate handling code to run along 
with the main server accepting connections. One way to achieve this is 
using threads. The main server program accepts a connection and creates
a new thread to handle communication for the connection, and then the
 server goes back to accept more connections.
"""

import socket
import thread

def Main():
    HOST = '0.0.0.0'
    PORT = 8001
    
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created.'
    
    # Bind socket to local host and port 
    try:
        new_socket.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error code:', str(msg[0]) + 'Message' + msg[1]
        return 
    print 'Socket bind complete'

    # Listening on socket
    new_socket.listen(10)
    print 'Socket now listening on port %d'%PORT
    
    # Now keep talking with client
    while 1:
        # Wait to accept a connection 
        conn, addr = new_socket.accept()
        print 'Connected with', addr[0], ':', str(addr[1])
        
        thread.start_new_thread(clientThread, (conn, ))
    
    new_socket.close()
    
    
# Function for handling connections. This will be used to create threads.
def clientThread(conn):
    # Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n')
    
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        reply = 'I am pi, your message is ' + data
        conn.sendall(reply)
    
    conn.close()
    

if __name__ == '__main__':
    Main()
