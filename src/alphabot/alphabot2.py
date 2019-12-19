# import native modules
import logging
# local imports
from alphabot import steering, camera, led, buzzer, button, frontIR, bottomIR, receiverIR

logger = logging.getLogger(__name__)
logger.info("logging from alphabot2: {0}".format(__name__))


class AlphaBot2:
    def __init__(self):
        logger.info("Initializing AlphaBot2")
        logger.debug("Add steering to alphabot")
        self.steering = steering.Steering()
        logger.debug("Add camera to alphabot")
        self.camera = camera.Camera()
        logger.debug("Add LEDs to alphabot")
        self.light = led.LED()
        logger.debug("Add buzzer to alphabot")
        self.sound = buzzer.Buzzer()
        logger.debug("Add buttons to alphabot")
        self.button = button.Button()
        logger.debug("Add front IR to alphabot")
        self.front_ir = frontIR.Front_IR()
        logger.debug("Add bottom IR to alphabot")
        self.bottom_ir = bottomIR.Bottom_IR()
        logger.debug("Add IR receiver to alphabot")
        self.receiver_ir = receiverIR.Receiver_IR()


"""    def get_state(self):
        return {
            # TODO: update these to use the getters?
            "pan": self.camera.pan,
            "tilt": self.camera.tilt
        }"""
