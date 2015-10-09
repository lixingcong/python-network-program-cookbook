    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月2日 下午4:30:46
# 说明：测试checksum算法

import struct

def book_checksum(source_string):
        sum1 = 0
        max_count = (len(source_string)) * 2
        count = 0
        # Loop to calc the sum of all ascii
        while count < max_count:
            # Function ord() return a demical number of ascii.
            val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
            sum1 += val
            sum1 = sum1 & 0xffffffff
            count += 2
        # I don't know what the following operation means.
        if max_count < len(source_string):
            sum1 += ord(source_string[len(source_string) - 1])
            sum1 = sum1 & 0xffffffff
            
        sum1 = (sum1 >> 16) + (sum & 0xffff)
        sum1 += (sum1 >> 16)
        answer = ~sum1
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

if __name__ == "__main__":
    a = input("input a string:")
    data = struct.pack("2i", a)
    print "original:" , repr(a)
    print "converted:", repr(data)
    #print book_checksum(data)
