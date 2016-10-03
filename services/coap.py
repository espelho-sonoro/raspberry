import aiocoap
import aiocoap.resource as resource
import asyncio
import simplejson as json

import collections
import logging

PositionMessage = collections.namedtuple('PositionMessage', ['degrees'])
MovementMessage = collections.namedtuple('MovementMessage', ['movement'])

class MotorResource(resource.Resource):

    logger = logging.getLogger(__name__)

    def __init__(self, motor):
        super(MotorResource, self).__init__()
        self.motor = motor
        self.logger.info("Created a motor resource")

    async def render_get(self, request):
        self.logger.info("Received a GET request: %s", request)

        position = self.motor.position()
        position_message = PositionMessage(degrees=position)
        response = self.build_response(position_message)

        return response

    async def render_put(self, request):
        self.logger.info("Received a PUT request: %s", request)

        movement_message = self.parse_payload(request.payload)
        new_position = self.rotate_motor(movement_message)
        position_message = PositionMessage(degrees=new_position)
        response = self.build_response(position_message, aiocoap.CHANGED)

        return response

    def parse_payload(self, payload):
        raw_movement_message = json.loads(payload)
        movement_message = MovementMessage(**raw_movement_message)
        self.logger.info("Parsed rotate message: %s", movement_message)
        return movement_message

    def rotate_motor(self, movement_message):
        new_position = self.motor.rotate(movement_message.movement)
        self.logger.info("New position motor position: %s.", new_position)
        return new_position

    def build_response(self, message, code=aiocoap.CONTENT):
        response_payload = json.dumps(message)
        response = aiocoap.Message(code=code, payload=response_payload.encode("ascii"))
        self.logger.info("Built response: %s", response)
        return response
