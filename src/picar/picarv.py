# import native modules
# local imports
from picar import front_wheels, back_wheels, camera, vision
import logging

logger = logging.getLogger(__name__)

class PicarV:
    def __init__(self, config_json):
        logger.info("Initializing PicarV with config: {0}".format(str(config_json)))
        self.front_wheels = front_wheels.Front_Wheels(config_file=config_json)
        self.back_wheels = back_wheels.Back_Wheels(config_file=config_json)
        self.camera = camera.Camera(config_file=config_json)
        self.vision = vision.Vision(config_file=config_json)
        # TODO: add vertical view (tilt)
        # TODO: add horizontal view (pan)

    def get_state(self):
        return {
            "pan": self.camera.current_pan,
            "tilt": self.camera.current_tilt
        }
