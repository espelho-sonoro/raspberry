import logging

class Motor:

    logger = logging.getLogger(__name__)
    orientation = 0.0

    def __init__(self):
        self.logger.info("Create motor instance")

    def rotate(self, degrees):
        self.logger.info("Moving motor: %s degrees", degrees)
        self.orientation += degrees
        return self.orientation

    def position(self):
        return self.orientation
