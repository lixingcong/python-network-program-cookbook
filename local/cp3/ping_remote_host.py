    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月1日 下午9:58:58
# 说明：使用root用户执行一个icmp查验主机的服务。

import argparse
import os
import socket
import struct
import select
import time

ICMP_ECHO_REQUEST = 8
DEFAULT_TIMEOUT = 2
DEFAULT_COUNT = 4

class Pinger(object):
    def __init__(self, target_host, count = DEFAULT_COUNT, timeout = DEFAULT_TIMEOUT):
        self.target_host = target_host
        self.count = count
        self.timeout = timeout
        
    # Checksum REFERENCE: http://blog.xiyoulinux.org/?p=3338
    def do_checksum(self, source_string):
        sum1 = 0
        
        max_count = (len(source_string) / 2) * 2
        count = 0
        # Loop to calc the sum of all ascii
        # Every 16 Bits will be combined to a group
        while count < max_count:
            # Function ord() return a demical number of ascii.
            val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
            sum1 = sum1 + val
            sum1 = sum1 & 0xffffffff
            count = count + 2
        # Because max_count was devided two part then multipy by two
        # We still consider the length is odd 
        # So, if the length is odd, we need to calc the last bytes
        if max_count < len(source_string):
            sum1 = sum1 + ord(source_string[len(source_string) - 1])
            sum1 = sum1 & 0xffffffff
            
        # To get the higher 16 bit of sum1 equal zero, you need to add higher 16 bit
        # to the lower 16 bits
        sum1 = (sum1 >> 16) + (sum1 & 0xffff)
        # do it again for some exception. Ensure to get the correct sum1
        sum1 = sum1 + (sum1 >> 16)
        
        # Invert the sum1 
        answer = ~sum1
        
        # Convert HEX to DEC
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        # Now it is demical
        return answer 
    
    def receive_pong(self, sock, ID, timeout):
        # Receive ping from the socket
        # It seems like that it lack of checksum check from the server?
        time_remaining = timeout
        while True:
            start_time = time.time()
            readable = select.select([sock], [], [], time_remaining)
            time_spent = (time.time() - start_time)
            # If Time is out
            if readable[0] == []:
                return 
            time_received = time.time()
            # socket.recvfrom() return a srtring and its address
            recv_packet, addr = sock.recvfrom(1024)
            icmp_header = recv_packet[20:28]
            # 待会这里要打印一下是什么内容
            type, code, checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)
            # If the packet is ICMP:
            if packet_ID == ID:
                bytes_In_Double = struct.calcsize("d")
                time_sent = struct.unpack("d", recv_packet[28:28 + bytes_In_Double])[0]
                return time_received - time_sent
            time_remaining = time_remaining - time_spent
            if time_remaining <= 0:
                return 
    
    def send_ping(self, sock, ID):
        # Send ping to host
        target_addr = socket.gethostbyname(self.target_host)
        my_checksum = 0
        # Create a dummy header with a zero checksum
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        # Pack the time stamp with a dummy "Q"-end to 192 bytes
        # time.time() returns a float number from the year of 1970
        bytes_In_Double = struct.calcsize("d")
        data = (192 - bytes_In_Double) * "Q"
        data = struct.pack("d", time.time()) + data
        # Get the checksum on the data and the dummy header
        my_checksum = self.do_checksum(header + data)
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
        packet = header + data
        sock.sendto(packet, (target_addr, 1))
                    
    def ping_once(self):
        # Return the delay
        icmp = socket.getprotobyname("icmp")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error, (errno, msg):
            if errno == 1:
                # Not superuser,so operation is not permitted
                msg += "ICMP messages can only be sent from rootuser process"
                raise socket.error(msg)
        except Exception, e:
            print "Exception:", e
        my_ID = os.getpid() & 0xffff
        self.send_ping(sock, my_ID)
        delay = self.receive_pong(sock, my_ID, self.timeout)
        sock.close()
        return delay
    
    def ping(self):
        # run the ping process
        for i in xrange(self.count):
            print "Ping to %s..." % self.target_host
            try:
                delay = self.ping_once()
            except socket.gaierror, e:
                print "ping failed.(socket error: '%s')" % e[1]
                break
            if delay == None:
                print "ping failed.(timeout within %ssec.)" % self.timeout
            else:
                delay = delay * 1000
                print "Get pong in %0.4fms" % delay
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "python ping ")
    parser.add_argument('--target-host', action = "store", dest = "target_host", required = True)
    given_args = parser.parse_args()
    target_host = given_args.target_host
    pinger = Pinger(target_host = target_host)
    pinger.ping()
            
