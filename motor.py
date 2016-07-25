import aiocoap
import aiocoap.resource as resource

import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MotorResource(resource.Resource):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super(MotorResource, self).__init__()
        self.content = "This is a motor resource".encode('ascii')
        self.logger.info("Created a motor resource")

    @asyncio.coroutine
    def render_get(self, request):
        self.logger.info("Received a get request: %s", request)
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=self.content)
        self.logger.info("Sending get response: %s", response)
        return response

    @asyncio.coroutine
    def render_put(self, request):
        self.logger.info("Received a put request: %s", request)
        self.content = request.payload
        payload = "Changed content to: %s" % self.content
        response = aiocoap.Message(code=aiocoap.CHANGED, payload=payload.encode("ascii"))
        self.logger.info("Sending put response: %s", response)
        return response


@asyncio.coroutine
def register_with_server(local_server_address):
    protocol = yield from aiocoap.Context.create_client_context()

    request = aiocoap.Message(code=aiocoap.PUT)
    request.payload = local_server_address.encode('ascii')
    request.set_request_uri('coap://localhost/register')

    try:
        response = protocol.request(request).response
    except Exception as e:
        logger.error(e, 'Failed to make request')
    else:
        logger.info('Registered succesfully')


def main():
    root = aiocoap.resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('motor',), MotorResource())

    asyncio.async(aiocoap.Context.create_server_context(root, bind=('::', 5684)))
    asyncio.async(register_with_server('coap://127.0.0.1:5684'))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()

