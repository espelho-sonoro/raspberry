from services import *
from controllers import *

import logging
import aiocoap
import aiocoap.resource as resource
import asyncio

logging.basicConfig(level=logging.DEBUG)

SERVER_ADDRESS='http://localhost:5000'

def main():
    motor = Motor()
    espelhos = Espelhos(SERVER_ADDRESS)

    espelhos.register()

    root = aiocoap.resource.Site()
    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('motor',), coap.MotorResource(motor))

    loop = asyncio.get_event_loop()
    asyncio.async(aiocoap.Context.create_server_context(root))

    loop.run_forever()

if __name__ == "__main__":
    main()
