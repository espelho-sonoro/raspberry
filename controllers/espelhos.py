from urllib import request
from random import randint

import logging
import collections
import simplejson as json

INTERFACE = 'eth0'
PORT = '5683'
NAME = 'espelhos-' + str(randint(100000, 999999))

RegisterMessage = collections.namedtuple('RegisterMessage', ['name', 'port'])

class Espelhos(object):

    logger = logging.getLogger(__name__)

    def __init__(self, server_address):
        self.server_address = server_address

    def register(self):
        message = RegisterMessage(name=NAME, port=PORT)
        req = self.register_request(message)
        self.logger.info('Register created made: %s', str(req))

        with request.urlopen(req) as response:
            pass

    def register_request(self, message):
        data = str.encode(json.dumps(message))
        url = self.server_address + '/box'
        req = request.Request(url=url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        return req
