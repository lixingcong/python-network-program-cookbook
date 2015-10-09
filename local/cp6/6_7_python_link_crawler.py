    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月9日 下午8:00:55
# 说明：简单的抓取网页上的链接，对https失效了
# usage: python xx.py --url='tieba.baidu.com' --query='tieba' --depth=1

import argparse
import sys
import httplib
import re

processed = []

def search_links(url, depth, search):
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

		# find the links 
		contents = result.read()
		all_links = re.findall('href="(.*?)"', contents)

		if (search in contents):
			print "found " + search + "at" + url

		print "==> %s processing %s links" % (str(depth), str(len(all_links)))
		for href in all_links:
			# find relative urls
			
			if (href.startswith("/")):
				href = "http://" + host + href
			print href
			# recurses links
			if (depth > 0):
				search_links(href, depth - 1, search)
	else:
		print "Skipping link: %s" % url
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Webpage link crwaler")
	parser.add_argument('--url', action = "store", dest = "url", required = True)
	parser.add_argument('--query', action = "store", dest = "query", required = True)
	parser.add_argument('--depth', action = "store", dest = "depth", type = int, default = 2)
	given_args = parser.parse_args()

	try:
		search_links(given_args.url, given_args.depth, given_args.query)
	except KeyboardInterrupt:
		print "Aborting search by user request"
	
