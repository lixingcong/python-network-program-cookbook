    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午8:32:04
# 说明： 带cookies和自动解析lt进行模拟登陆,实测成功，需要安装bs库: sudo pip install beautifulsoup4
# 原文链接： http://jackroyal.github.io/2015/05/23/python-requests-login-csdn-blog/
# 知识点：未明白：lt是什么序列号，tojson是什么原理，
# TODO: 模拟登陆v2ex还有某些https的网站，带验证码的识别库，集成多线程爬虫下载附件

import requests
import re
import os

from cookielib import LWPCookieJar

URL = 'http://ids.cumt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cumt.edu.cn%2Findex.portal'
REFER_URL = URL
URL_AFTER_LOGIN = 'http://my.cumt.edu.cn/index.portal'

USERNAME = '041314xx'
PASSWORD = 'xxxxxxxx'

# 这个完全可以不用bs库，直接从网页源代码提取
def get_lt(str_):
    f = re.compile(r"name=\"lt\"\svalue=\"(.*)\"\s/>", flags = 0)
    return f.findall(str_)[0]


# cookie setting
s = requests.Session()
s.cookies = LWPCookieJar('cookiejar')
header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
          'Referer':REFER_URL
          }

payload = {'username':USERNAME,
       'password':PASSWORD,
       'execution':'e1s1',
       'lt':None,
       '_eventId':'submit'
       }


# if cookies existed, or not expried
if os.path.exists('cookiejar'):
    ask = raw_input('Cookies existed. Clear them and login again?\n(y/n): ')
else:
    ask = 'y'

if ask == 'y':
    print "Setting Cookies Now..."
    response = s.get(URL)
    payload['lt'] = get_lt(response.text)
    response = s.post(URL, data = payload, headers = header)
    s.cookies.save(ignore_discard = True)
    print response.text
else:
    print "Restoring cookie..."
    s.cookies.load(ignore_discard = True)
    response = s.get(URL_AFTER_LOGIN, headers = header)
    print response.text

