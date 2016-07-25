import aiocoap
import aiocoap.resource as resource

import flask

import os
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
app = flask.Flask(__name__)

motor = None

class RegisterResource(resource.Resource):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super(RegisterResource, self).__init__()
        self.content = "This is register resource".encode('ascii')
        self.logger.info("Created a register resource")

    @asyncio.coroutine
    def render_get(self, request):
        self.logger.info("Received a get request: %s", request)
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=motor)
        self.logger.info("Sending get response: %s", response)
        return response

    @asyncio.coroutine
    def render_put(self, request):
        self.logger.info("Received a put request: %s", request)
        motor = request.get_request_uri()
        payload = "Changed content to: %s" % motor
        response = aiocoap.Message(code=aiocoap.CHANGED, payload=payload.encode("ascii"))
        self.logger.info("Sending put response: %s", response)
        return response

def coap_server():
    root = aiocoap.resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('register',), RegisterResource())

    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

@app.route('/')
def index():
    return "No motor registered" if motor else motor

def flask_server():
    app.run()

def main():
    pid = os.fork()
    if pid == 0:
        coap_server()
    else:
        flask_server()

if __name__ == "__main__":
    main()
