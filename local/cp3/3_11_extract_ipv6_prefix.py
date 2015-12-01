    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月26日 下午5:01:11
# 说明：从ipv6中提取v6前缀
# 需要第三方的库 sudo pip install netaddr  (墙很厉害，dns污染)
# 按照RFC 3513的定义，前面的64位地址由全网路由和子网id组成，通常使用一个较短的前缀（例如/48），可以定义更长，更具体的前缀，比如/64。
# 原书中有错误，出现的%eth应该替换为interface因为不止一个eth接口，有的的电脑有无线接入openwrt也能获得v6地址

import socket
import netifaces as ni
import netaddr as na

def extract_ipv6_info():
    print "ipv6 support built into python: %s" % socket.has_ipv6
    for interface in ni.interfaces():
        all_addresses = ni.ifaddresses(interface)
        print "Interface %s:" % interface
        for family, addrs in all_addresses.iteritems():
            fam_name = ni.address_families[family]
            # print "Family:",fam_name
            for addr in addrs:
                if fam_name == 'AF_INET6':
                    addr = addr['addr']
                    # Error in sample code on the book
                    has_eth_string = addr.split('%' + interface)
                    if has_eth_string:
                        # Error in sample code on the book
                        addr = addr.split('%' + interface)[0]
                    print " -IP address: %s" % na.IPNetwork(addr)
                    print " -IP Version: %s" % na.IPAddress(addr).version
                    print " -IP Prefix length: %s" % na.IPNetwork(addr).prefixlen
                    print " -Network: %s" % na.IPNetwork(addr).network
                    print " -Broadcast: %s" % na.IPNetwork(addr).broadcast
                    print ""
                    
if __name__ == "__main__":
    extract_ipv6_info()                    
                    
                    
                    
        
