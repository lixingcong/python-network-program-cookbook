    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午9:29:28
# 说明：使用代理服务器发送web请求

import urllib

URL = 'https://www.github.com'
PROXY_ADDR = '127.0.0.1:8000'

if __name__ == "__main__":
    resp = urllib.urlopen(URL, proxies = {'http':PROXY_ADDR})
    print "Proxy sever returns response headers %s" % resp.headers
