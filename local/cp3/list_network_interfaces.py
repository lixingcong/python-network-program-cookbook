    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月5日 下午9:46:51
# 说明：通过socket获得当前系统的接口，不使用ifconfig

import sys
import socket
# using fcntl to lock a file
import fcntl
import struct
# using array for the same type data
import array

# The request code of getting all interfaces
SIOCGIFCONF = 0x8912
STUCT_SIZE_32 = 32
STUCT_SIZE_64 = 40
PLATFORM_32_MAX_NUMBER = 2 ** 32
DEFAULT_INTERFACES = 8

def list_interface():
    interfaces = []
    max_interfaces = DEFAULT_INTERFACES
    is_64bits = sys.maxsize > PLATFORM_32_MAX_NUMBER
    struct_size = STUCT_SIZE_64 if is_64bits else STUCT_SIZE_32
    # sock_dgram is a type of UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        bytes1 = max_interfaces * struct_size
        interface_names = array.array('B', '\0' * bytes1)
        sock_info = fcntl.ioctl(
            sock.fileno(),
            SIOCGIFCONF,
            struct.pack('iL', bytes1, interface_names.buffer_info()[0])
            )
        outbytes = struct.unpack('iL', sock_info)[0]
        if outbytes == bytes1:
            max_interfaces *= 2
        else:
            break
    namestr = interface_names.tostring()
    for i in range(0, outbytes, struct_size):
        # Attention to namestr(): the para is [a:a+16]
        interfaces.append((namestr[i: i + 16].split('\0', 1)[0]))
    return interfaces
    
if __name__ == "__main__":
    interfaces = list_interface()
    print "machine has %s interfaces :%s" % (len(interfaces), interfaces)
                    
        
