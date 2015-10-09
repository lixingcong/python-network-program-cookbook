    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月6日 下午4:24:31
# 说明：获取某个接口的ip 在linux下正常工作 形参为 lo wlan0 eth0等网络接口

import argparse
import socket
import fcntl
import struct


def get_interface_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
                            fcntl.ioctl(
                                        s.fileno(),
                                        0x8915,    # SIOCGIFADDR
                                        struct.pack('256s', ifname[:15]))
                            [20:24]
                            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "python network utils")
    parser.add_argument('--ifname', action = "store", dest = "ifname", required = True)
    given_args = parser.parse_args()
    ifname = given_args.ifname
    print "Interface [%s] --> IP: %s" % (ifname, get_interface_ip_addr(ifname))

