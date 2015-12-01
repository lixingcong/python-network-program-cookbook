    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月26日 下午4:32:23
# 说明：检查当前是否支持ipv6
# 需要第三方的库 sudo pip install netifaces
# 问题：AF_PACKET这个family是什么家族呢？

import socket
import netifaces as ni

def inspect_ipv6_support():
    # to find the ipv6 address
    print "IPV6 support built into python: %s" % socket.has_ipv6
    ipv6_addr = {} 
    for interface in ni.interfaces():
        all_addresses = ni.ifaddresses(interface)
        print "\nInterface %s:" % interface
        for family, addrs in all_addresses.iteritems():
            fam_name = ni.address_families[family]
            print "Address family: %s" % fam_name
            for addr in addrs:
                if fam_name == 'AF_INET6':
                    ipv6_addr[interface] = addr['addr']
                print "---address: %s " % addr['addr']
                nmask = addr.get('netmask', None)
                if nmask:
                    print "---Netmask: %s" % nmask
                bcast = addr.get('broadcast', None)
                if bcast:
                    print "---Broadcast: %s" % bcast
    if ipv6_addr:
        print "Found ipv6 address %s" % ipv6_addr
    else:
        print "No ipv6 address found"
        
if __name__ == "__main__":
    inspect_ipv6_support()        
        
