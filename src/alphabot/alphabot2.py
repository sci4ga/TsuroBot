# import native modules
import logging
# local imports
from alphabot import steering, camera, led, buzzer, button, frontIR

logger = logging.getLogger(__name__)
logger.info("logging from alphabot2: {0}".format(__name__))

class AlphaBot2:
    def __init__(self):
        logger.info("Initializing AlphaBot2")

        #self.steering = steering.Steering()
        #self.camera = camera.Camera()
        #self.light = led.LED()
        #self.sound = buzzer.Buzzer()
        #self.button = button.Button()
        logger.info("Add front IR to alphabot")
        self.front_ir = frontIR.Front_IR()
        # TODO: add bottom ir
        # TODO: add front ir


"""    def get_state(self):
        return {
            # TODO: update these to use the getters?
            "pan": self.camera.pan,
            "tilt": self.camera.tilt
        }"""
