# import native modules
# local imports
#from alphabot import front_wheels, back_wheels, camera
from alphabot import camera
import logging

logger = logging.getLogger(__name__)

class AlphaBot2:
    def __init__(self):
        logger.info("Initializing AlphaBot2")
        #self.front_wheels = front_wheels.Front_Wheels()
        #self.back_wheels = back_wheels.Back_Wheels()
        self.camera = camera.Camera()
        # TODO: add vertical view (tilt)
        # TODO: add horizontal view (pan)

    def get_state(self):
        return {
            # TODO: update these to use the getters?
            "pan": self.camera.pan,
            "tilt": self.camera.tilt
        }
