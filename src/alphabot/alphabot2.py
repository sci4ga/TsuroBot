# import native modules
# local imports
from alphabot import camera
from alphabot import steering
import RPi.GPIO as GPIO
# from alphabot import front_wheels, back_wheels, camera
import logging

logger = logging.getLogger(__name__)

class AlphaBot2:
    def __init__(self):
        logger.info("Initializing AlphaBot2")
        GPIO.cleanup()
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
