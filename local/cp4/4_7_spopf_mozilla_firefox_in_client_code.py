    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午9:51:14
# 说明：伪装成火狐的agent代码

import urllib2

BROWSER = 'Mozilla/5.0 (Windows NT 5.1; rv:20.0) Gecko/20100101 Firefox/20.0'
URL = 'http://www.cumt.edu.cn'

def spoof_firefox():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', BROWSER)]
    result = opener.open(URL)
    print "Response headers:"
    for head in result.headers.headers:
        print "\t", head
        
if __name__ == "__main__":
    spoof_firefox()        
