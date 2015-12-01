    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午9:40:52
# 说明：使用HTTPConnection()向服务器发起请求，判断网页返回代码

import argparse
import httplib
import urlparse


DEFAULT_URL = 'http://www.cumt.edu.cn'
HTTP_GOOD_CODES = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]

def get_server_status_code(url):
    # Download just the header of a URL and return status code
    host, path = urlparse.urlparse(url)[1:3]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Example HEAD Request')
    parser.add_argument('--url', action = 'store', dest = 'url', default = DEFAULT_URL)
    given_args = parser.parse_args()
    url = given_args.url
    if get_server_status_code(url) in HTTP_GOOD_CODES:
        print "Server %s status is OK!" % url
    else:
        print "Server %s status is NOT OK!" % url
