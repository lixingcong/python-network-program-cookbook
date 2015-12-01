    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午8:32:04
# 说明： 带cookies和自动解析lt进行模拟登陆,实测成功，需要安装bs库: sudo pip install beautifulsoup4
# 原文链接： http://jackroyal.github.io/2015/05/23/python-requests-login-csdn-blog/
# 知识点：未明白：lt是什么序列号，tojson是什么原理，
# TODO: 模拟登陆v2ex还有某些https的网站，带验证码的识别库，集成多线程爬虫下载附件

import requests
import os
from bs4 import BeautifulSoup as bs
from cookielib import LWPCookieJar

URL = 'http://ids.cumt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cumt.edu.cn%2Findex.portal'
REFER_URL = URL
URL_AFTER_LOGIN = 'http://my.cumt.edu.cn/index.portal'

USERNAME = '04131434'
PASSWORD = '12345678'

# 提取lt流水号，将数据化为一个字典
def toJson(str_):
    soup = bs(str_)
    tt = {}
    for inp in soup.form.find_all('input'):
        if inp.get('name') != None:
            tt[inp.get('name')] = inp.get('value')
    return tt


# cookie setting
s = requests.Session()
s.cookies = LWPCookieJar('cookiejar')
header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
          'Referer':REFER_URL
          }

# if cookies existed, or not expried
if os.path.exists('cookiejar'):
    ask = raw_input('Cookies existed. Clear them and login again?\n(y/n): ')
else:
    ask = 'n'
    
if ask == 'y':
    print "Setting Cookies Now..."
    response = s.get(URL)
    soup = toJson(response.text)
    payload = {'username':USERNAME,
               'password':PASSWORD,
               'lt': soup["lt"],
               'execution':'e1s1',
               '_eventId':'submit'
               }
    response = s.post(URL, data = payload, headers = header)
    s.cookies.save(ignore_discard = True)

    print response.text
else:
    print "Restoring cookie..."
    s.cookies.load(ignore_discard = True)

# After login sucessfully, what website you want to visit now?
# r = s.get(URL_AFTER_LOGIN, headers = header)
# print r.text
