from motor import *
import logging
import aiocoap
import aiocoap.resource as resource
import asyncio

logging.basicConfig(level=logging.DEBUG)

SERVER_ADDRESS='coap://localhost'

def main():
    motor = Motor()

    root = aiocoap.resource.Site()
    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('motor',), coap.MotorResource(motor))

    loop = asyncio.get_event_loop()
    asyncio.async(aiocoap.Context.create_server_context(root))

    loop.run_forever()

if __name__ == "__main__":
    #print(dir(motor))
    main()
