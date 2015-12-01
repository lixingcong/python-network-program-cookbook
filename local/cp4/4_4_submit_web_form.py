    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月16日 下午10:01:27
# 说明：网页填表
# 搞不清楚post和get的区别

import urllib2
import urllib
import requests

ID_USERNAME = 'username' 
ID_PASSWORD = 'password'
USERNAME = 'llllll'
PASSWORD = '111111'
SIGNUP_URL = 'http://ids.cumt.edu.cn/authserver/login'

def submit_form():
    # Submit a form
    payload = {
             ID_USERNAME:USERNAME,
             ID_PASSWORD:PASSWORD
             }
    # make a get request
    resp = requests.get(SIGNUP_URL)
    print "Response to GET request: %s" % resp.content
    
    # send post request
    resp = requests.post(SIGNUP_URL, payload)
    print "Headers from a POST request response: %s" % resp.headers
    
    
if __name__ == "__main__":
    submit_form()
