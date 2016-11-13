#!/usr/bin/python3

import http.client
import codecs
import json
from pprint import pprint

# class HTTPClient(object):




if __name__ == '__main__':

	# conn = http.client.HTTPSConnection("172.18.0.5", 8000, timeout=2)
	conn = http.client.HTTPConnection("dev.idwell.ru", timeout=30)

	analog = '''curl 'http://dev.idwell.ru/api/system/init/' 
					-H 'Host: dev.idwell.ru' 
					-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0' 
					-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' 
					-H 'Accept-Language: en-US,en;q=0.5' 
					-H 'Accept-Encoding: gzip, deflate' 
					-H 'Authorization: Basic YWRtaW46MTIzNDU2N0Fz' 
					-H 'Cookie: csrftoken=Dq70lhcHNA1RplfAGsxp6vgvKTYPlzpEFMALMtBLq4INjAoP3wJX2Mrjx8UHNwRq' 
					-H 'Connection: keep-alive'''
	
	headers = {
		'Authorization': 'Basic YWRtaW46MTIzNDU2N0Fz',
		'Host': 'dev.idwell.ru',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
		# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept': 'application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		# 'Accept-Language': 'en-US,en;q=0.5',
		# 'Accept-Encoding': 'gzip, deflate',
		'Authorization': 'Basic YWRtaW46MTIzNDU2N0Fz',
		'Cookie': 'csrftoken=Dq70lhcHNA1RplfAGsxp6vgvKTYPlzpEFMALMtBLq4INjAoP3wJX2Mrjx8UHNwRq',
		# 'Connection': 'keep-alive',
	}

	conn.request("GET", "/api/profile/30/", headers=headers)
	r1 = conn.getresponse()

	print(r1.status, r1.reason)

	data = r1.read()
	print('type: %s' % type(data))
	print(' len: %s' % len(data))
	response_str = codecs.decode(data)
	response = json.loads(response_str)
	pprint(response)
