#!/usr/bin/python3

import sys
import http.client
import urllib.parse
import codecs
from random import choice
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

    def __init__(self, url, port=None, pre=None, verbose=False, timeout=30):
        if url.startswith('http'):
            self.url = url[5:].strip('/')
        else:
            self.url = url

        _port = port
        if url == SERVERS['lh']:
            _port = 8000

        self.port = _port
        self.pre = pre.strip('/')
        self.verbose = verbose
        self.timeout = timeout

    def __send_request(self, method, api, data=None, print_response=False, print_full=False, print_meta=False, **kwargs):
        _method = method
        _api = api.strip('/')
        _args = ['{}={}'.format(k,v) for k, v in kwargs.items()]

        conn = http.client.HTTPConnection(self.url, self.port, timeout=self.timeout)
        headers = {
            'Host': self.url,
            'Authorization': 'Basic YWRtaW46MTIzNDU2N0Fz',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/json',
        }

        _fullapi = '/{}/{}/'.format(self.pre, _api)
        _api_with_args = _fullapi
        if len(_args) > 0:
            _api_with_args = '{}?{}'.format(_fullapi, '&'.join(_args))
        if print_full or print_meta or print_response:
            print('{}: {}'.format(_method, _api_with_args))
            if data is not None:
                print('data: {}'.format(data))
        conn.request(_method, _api_with_args, json.dumps(data), headers=headers)
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

    def get(self, api, data=None, print_response=False, print_full=False, print_meta=False, **kwargs):
        return self.__send_request('GET', api, data, print_response=print_response, print_full=print_full, print_meta=print_meta, **kwargs)

    def post(self, api, data=None, print_response=False, print_full=False, print_meta=False, **kwargs):
        return self.__send_request('POST', api, data, print_response=print_response, print_full=print_full, print_meta=print_meta, **kwargs)

    def patch(self, api, data=None, print_response=False, print_full=False, print_meta=False, **kwargs):
        return self.__send_request('PATCH', api, data, print_response=print_response, print_full=print_full, print_meta=print_meta, **kwargs)


def make_client():
    server = 'lh'
    try:
        _server = sys.argv[1]
        assert _server in SERVERS
        server = _server
    except:
        pass
    return HTTPClient(SERVERS[server], pre='/api/', timeout=60)


def get_string():
    with codecs.open('/tmp/base.txt', 'r', 'utf-8') as f:
        return choice(f.readlines()).strip('\n ')


def generate_posts(cli):
    measure = Measure()
    for i in range(50):
        response = cli.post('/newsband/', data={'text': get_string()}, print_full=False)
        measure.append(response['meta']['elapsed'])
    print(measure)


def measurement_of_profiles(cli):
    # response = cli.get('/profile/', count=1, print_full=True)
    # response = cli.get('/profile/53/', count=1, print_full=True)
    #
    # count = response['count']

    # response = cli.get('/profile/', group='Dweller', print_full=True)
    # for i in range(20):

    first_print_meta = True

    measure = Measure()
    for i in range(5):
        # response = cli.get('/system/init/', print_full=False)
        # response = cli.get('/profile/', count=1, print_full=False)
        response = cli.get('/profile/', group='Dweller', print_full=False, print_meta=first_print_meta)
        measure.append(response['meta']['elapsed'])
        first_print_meta = False
    print(measure)


if __name__ == '__main__':

    cli = make_client()

    generate_posts(cli)
