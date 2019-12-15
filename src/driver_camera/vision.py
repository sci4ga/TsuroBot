# import native modules
import json
import logging
# import 3rd party modules
import cv2

logger = logging.getLogger(__name__)

class Vision(object):
    '''Computer Vision / Camera vision class'''

    def __init__(self, config_file):
        ''' setup channels and basic stuff '''
        logger.info("Initializing front wheels with config_file: {0}".format(str(config_file)))
        with open(config_file) as f:
            self.config = json.load(f)

    def grab_still(self, file_name=".././temp/capture.jpg"):
        try:
            img = cv2.VideoCapture(-1)
            _, bgr_image = img.read()
            cv2.imwrite(file_name, bgr_image)
        finally:
            img.release()

    def grab_still_mem(self):
        try:
            img = cv2.VideoCapture(-1)
            _, bgr_image = img.read()
        finally:
            img.release()
