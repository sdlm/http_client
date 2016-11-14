#!/usr/bin/python3

import sys
import http.client
import codecs
import json
from pprint import pprint
from helpers import Timer, Measure


SERVERS = {
    'lh': 'http://172.18.0.5/',
    'dev': 'http://dev.idwell.ru/',
    'demo': 'http://demo.idwell.ru/',
}


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

    def get(self, api, print_response=False, print_full=False, print_meta=False, **kwargs):
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
        _api_with_args = _fullapi
        if len(_args) > 0:
            _api_with_args = '{}?{}'.format(_fullapi, '&'.join(_args))
        if print_full or print_meta or print_response:
            print('{}: {}'.format(_method, _api_with_args))
        conn.request(_method, _api_with_args, headers=headers)
        resp = None
        with Timer() as t:
            resp = conn.getresponse()

        if self.verbose:
            print(resp.status, resp.reason)

        data = resp.read()
        response_str = codecs.decode(data)
        result = {
            'data': json.loads(response_str),
            'meta': {
                'elapsed': t.msecs
            }
        }
        if print_response or print_full:
            pprint(result['data'])
        if print_meta or print_full:
            print('elapsed: {:.0f}'.format(result['meta']['elapsed']))

        return result


if __name__ == '__main__':

    server = 'lh'

    try:
        _server = sys.argv[1]
        assert _server in SERVERS
        server = _server
    except:
        pass

    _port = None
    if server == 'lh':
        _port = 8000

    cli = HTTPClient(SERVERS[server], port=_port, pre='/api/')

    measure = Measure()

    for i in range(10):
        # response = cli.get('/system/init/', print_full=False)
        response = cli.get('/profile/', count=1, print_full=False)
        measure.append(response['meta']['elapsed'])

    print(measure)
