    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月16日 下午10:01:27
# 说明：网页填表

import urllib2
import urllib
import requests

ID_USERNAME = 'signup-user-name' 
ID_EMAIL = 'fsignup-user-email'
ID_PASSWORD = 'signup-user-password'
USERNAME = 'username2'
EMAIL = 'youremail@qq.com'
PASSWORD = '123'
SIGNUP_URL = 'https://twitter.com/account/create'

def submit_form():
    # Submit a form
    payload = {
             ID_USERNAME:USERNAME,
             }
