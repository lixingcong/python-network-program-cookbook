    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月16日 下午8:03:54
# 说明：访问后提取cookies信息，成功后，提示first cookie和second cookie

import cookielib
import urllib
import urllib2

# Press F12 on Chrome and find the text input frame and find out the label name
# It depend on the page source code.
ID_PASSWORD = 'password'
ID_USERNAME = 'userName'
# Your account name and password
USERNAME = 'pro'
PASSWORD = 'xxx'
LOGIN_URL = 'http://tieba.baidu.com/#'
NORMAL_URL = 'http://tieba.baidu.com/#'

def extract_cookie_info():
    # Fake login to a site with cookie
    # Convert to password and username to the url data
    login_data = urllib.urlencode({ID_USERNAME:USERNAME, ID_PASSWORD:PASSWORD})
    # Create a cookiejar
    cj = cookielib.CookieJar()
    # Create a url opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # In order to initiate a login session, you have to send the username and password POST parameters to the page. 
    # If the POST parameters are correct, the server internally maintains a login session.
    resp = opener.open(LOGIN_URL, login_data)
    
    # Send login info 
    for cookie in cj:
        print "-- First time cookie: %s --> %s" % (cookie.name, cookie.value)
        
    # Print the response and view the output.
    # print resp.read()
    
    # Print the headers
    print "Headers: %s" % resp.headers
    
    # Now access without any login info
    resp = opener.open(NORMAL_URL)
    for cookie in cj:
        print "++ second time cookie %s --> %s" % (cookie.name, cookie.value)
        
    print "Headers: %s" % resp.headers
    
if __name__ == "__main__":
    extract_cookie_info() 
