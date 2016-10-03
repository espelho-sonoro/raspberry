from urllib import request
from random import randint

import logging
import collections
import simplejson as json

INTERFACE = 'eth0'
NAME = 'espelhos-' + str(randint(100000, 999999))

class Espelhos(object):

    logger = logging.getLogger(__name__)

    def __init__(self, server_address):
        self.server_address = server_address

    def register(self):
        req = self.register_request()
        self.logger.info('Register created made: %s', str(req))

        with request.urlopen(req) as response:
            pass

    def register_request(self):
        data = str.encode(json.dumps({'name': NAME}))
        url = self.server_address + '/box'
        req = request.Request(url=url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        return req
