#!/usr/bin/python3

import http.client
import codecs
import json
from pprint import pprint


class HTTPClient(object):
    """HTTP Client like a curl.

curl 'http://dev.idwell.ru/api/system/init/'
    -H 'Host: dev.idwell.ru'
    -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    -H 'Accept-Language: en-US,en;q=0.5'
    -H 'Accept-Encoding: gzip, deflate'
    -H 'Authorization: Basic YWRtaW46MTIzNDU2N0Fz'
    -H 'Cookie: csrftoken=Dq70lhcHNA1RplfAGsxp6vgvKTYPlzpEFMALMtBLq4INjAoP3wJX2Mrjx8UHNwRq'
    -H 'Connection: keep-alive"""

    def __init__(self, url, port=None, pre=None, verbose=False):
        if url.startswith('http'):
            self.url = url[5:].strip('/')
        else:
            self.url = url
        self.port = port
        self.pre = pre.strip('/')
        self.verbose = verbose

    def get(self, api, **kwargs):
        _method = 'GET'
        _api = api.strip('/')
        _args = ['{}={}'.format(k,v) for k, v in kwargs.items()]

        conn = http.client.HTTPConnection(self.url, self.port, timeout=30)
        headers = {
            'Host': self.url,
            'Authorization': 'Basic YWRtaW46MTIzNDU2N0Fz',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        _fullapi = '/{}/{}/'.format(self.pre, _api)
        _api_with_args = '{}?{}'.format(_fullapi, '&'.join(_args))
        print('{}: {}'.format(_method, _api_with_args))
        conn.request(_method, _api_with_args, headers=headers)
        r1 = conn.getresponse()

        if self.verbose:
            print(r1.status, r1.reason)

        data = r1.read()
        response_str = codecs.decode(data)
        return json.loads(response_str)


if __name__ == '__main__':
    cli = HTTPClient('http://dev.idwell.ru/', pre='/api/')

    # response = cli.get('/system/init/')
    # pprint(response)

    response = cli.get('/profile/', count=1)
    pprint(response)


