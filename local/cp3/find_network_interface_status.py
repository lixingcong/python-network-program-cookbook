    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月7日 下午9:20:19
# 说明：使用前安装nmap插件，sudo pip install python-nmap

import argparse
import socket
import struct
import fcntl
import nmap

SAMPLE_PORT = '21-23'

def get_interface_status(ifname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(
                        fcntl.ioctl(
                                    sock.fileno(),
                                    0x8915,    # SIOCGIFADDR, C socket library sockios.h
                                    struct.pack('256s', ifname[:15])
                                    )[20:24]
                        )
    nm = nmap.PortScanner()
    # In fact here is the function useful
    nm.scan(ip_address, SAMPLE_PORT)
    return nm[ip_address].state()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "python network utils")
    parser.add_argument('--ifname', action = "store", dest = "ifname", required = True)
    given_args = parser.parse_args()
    ifname = given_args.ifname
    print "Interface %s is %s" % (ifname, get_interface_status(ifname))
    
