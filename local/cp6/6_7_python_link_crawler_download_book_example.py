    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月9日 下午7:39:39
# 说明：执行 python 1.py --url='http://web.calstatela.edu/faculty/pthomas/CIS445/py/'
# 即可批量下载源代码py文件到/tmp/test_py/   自动递归目录
# 收获：配合chrome的F12开发人员工具进行表达式的调试，有利于网页的解析，总之不同的网页格式千变万化，此例为最简单的情况

import argparse
import httplib
import re
import os
import urllib2

processed = []
# create a folder to store files downloaded
try:
	os.mkdir("/tmp/test_py")
finally:
	pass

# A simple function to download file,url1 is the url,file_name is the original name on the server
def download_it(url1, file_name, location1):
	f = urllib2.urlopen(url1) 
	data = f.read() 
	with open((location1 + '/' + file_name), "wb") as code:     
		code.write(data)
		
# if download files,please add '/' as the tail of url
# dir_to_store is recusive dir to create
def search_links(url, depth, dir_to_store):
	url_is_processed = (url in processed)
	if (url.startswith("http://") and (not url_is_processed)):
		processed.append(url)
		url = host = url.replace("http://", "", 1)
		path = "/"
		
		urlparts = url.split("/")
		if (len(urlparts) > 1):
			host = urlparts[0]
			path = url.replace(host, "", 1)

		# start crawing 
		print "Crawing url: %s%s" % (host, path)
		conn = httplib.HTTPConnection(host)
		req = conn.request("GET", path)
		result = conn.getresponse()

		# find the links begin with "href"
		contents = result.read()
		all_links = re.findall('href="(.*?)"', contents)

		print "Depth %d is processing %s links that been found" % (depth, str(len(all_links)))
		for href in all_links:
			# find relative urls
			create_new_dir = ''
			# if it is 'chapter_', create a new folder
			if (href.startswith("c")):
				create_new_dir = "/tmp/test_py/" + href
				os.mkdir(create_new_dir)
				# Generate a new url more deeper
				href = "http://" + url + href
			# If it is a python code
			if (href.endswith(".py")):
				to_download = "http://" + url + href
				download_it(to_download, href, dir_to_store + '/')
			# Recusive	
			if (depth > 0):
				search_links(href, depth - 1, create_new_dir)			

	# else:
		# print "Skipping link: %s" % url
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Webpage link crwaler")
	parser.add_argument('--url', action = "store", dest = "url", required = True)
	parser.add_argument('--depth', action = "store", dest = "depth", type = int, default = 2)
	given_args = parser.parse_args()

	try:
		search_links(given_args.url, given_args.depth, '')
	except KeyboardInterrupt:
		print "Aborting search by user request"
	

