import aiocoap
import aiocoap.resource as resource

import logging
import asyncio
import json

logging.basicConfig(level=logging.DEBUG)

class RegisterResource(resource.Resource):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super(RegisterResource, self).__init__()
        self.content = "This is register resource".encode('ascii')
        self.logger.info("Created a register resource")

    def write_motor(self, motor_info):
        with open('motor', 'w') as f:
            f.write(motor_info)

    def read_motor(self):
        with open('motor', 'r') as f:
            return f.read()


    @asyncio.coroutine
    def render_get(self, request):
        self.logger.info("Received a get request: %s", request)
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=self.read_motor().encode('ascii'))
        self.logger.info("Sending get response: %s", response)
        return response

    @asyncio.coroutine
    def render_put(self, request):
        self.logger.info("Received a put request: %s", request)
        motor = request.payload.decode('ascii')
        self.write_motor(motor)
        payload = "Changed content to: %s" % motor
        response = aiocoap.Message(code=aiocoap.CHANGED, payload=payload.encode("ascii"))
        self.logger.info("Sending put response: %s", response)
        return response

class MotorControlResource(resource.Resource):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super(MotorControl, self).__init__()
        self.logger.info("Created a motor control resource")

    @asyncio.coroutine
    def render_get(self, request):
        pass

    @asyncio.coroutine
    def render_post(self, request):
        pass


def coap_server():
    root = aiocoap.resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('register',), RegisterResource())

    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    coap_server()
