# import native modules
import logging
# local imports
from alphabot import steering
from alphabot import camera


logger = logging.getLogger(__name__)

class AlphaBot2:
    def __init__(self):
        logger.info("Initializing AlphaBot2")

        self.steering = steering.Steering()
        self.camera = camera.Camera()
        # TODO: add bottom ir
        # TODO: add front ir


"""    def get_state(self):
        return {
            # TODO: update these to use the getters?
            "pan": self.camera.pan,
            "tilt": self.camera.tilt
        }"""
