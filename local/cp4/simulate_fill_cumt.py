    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午7:48:51
# 说明：模拟填表，先使用chrome-F12-Network抓包再分析是get还是post
  
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import requests
from bs4 import BeautifulSoup as bs

def toJson(str):
    '''
    提取lt流水号，将数据化为一个字典
    '''
    soup = bs(str)
    tt = {}
    for inp in soup.form.find_all('input'):
        if inp.get('name') != None:
            tt[inp.get('name')] = inp.get('value')
    return tt
  
# 登录的主页面  
hosturl = 'http://ids.cumt.edu.cn/authserver/login' 
# post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
posturl = 'http://ids.cumt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cumt.edu.cn%2Findex.portal' 
  
# 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
  
# 打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
h = urllib2.urlopen(hosturl)  
# print h.read()
soup = toJson(h)

  
# 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
           'Referer' : 'http://ids.cumt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cumt.edu.cn%2Findex.portal'}  
# 构造Post数据，他也是从抓大的包里分析得出的。  
postData = {'username' : '04131434',
            'password' : '12345678',
            'lt': soup['lt'],
            'execution':'e1s1',
            '_eventId':'submit'
            }  
  
# 需要给Post数据编码  
postData = urllib.urlencode(postData)  
  
# 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
request = urllib2.Request(posturl, postData, headers)  
# print request.headers
response = urllib2.urlopen(request)  
text = response.read()  
print text  

s = requests.Session()
r = s.get('http://my.cumt.edu.cn/index.portal')
print r.text
