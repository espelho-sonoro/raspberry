import aiocoap
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)

@asyncio.coroutine
def main():
    logger = logging.getLogger(__name__)
    logger.info('Starting main')

    protocol = yield from aiocoap.Context.create_client_context()

    request = aiocoap.Message(code=aiocoap.PUT)
    request.set_request_uri('coap://localhost/register')
    request.payload = ''

    try:
        logger.info('Performing request: %s', request)
        response = yield from protocol.request(request).response
    except Exception as e:
        logger.error(e, 'Failed to perform request')
    else:
        logger.info('Request succesful: %s', response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
