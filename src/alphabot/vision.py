# import native modules
import json
import logging
from typing import Optional
# import 3rd party modules
import cv2

logger = logging.getLogger(__name__)


class Vision:
    '''The Vision class gets input from the camera'''
    def __init__(self, config_file: str):
        logger.info(f"Initializing vision with config_file: {config_file}")
        with open(config_file) as f:
            self.config = json.load(f)

    def grab_still(self, file_name: Optional[str] = ".././temp/capture.jpg"):
        """Writes captured image to file"""
        try:
            img = cv2.VideoCapture(-1)
            _, bgr_image = img.read()
            cv2.imwrite(file_name, bgr_image)
        finally:
            img.release()

    def grab_still_mem(self):
        """Returns BGR image"""
        try:
            img = cv2.VideoCapture(-1)
            _, bgr_image = img.read()
        finally:
            img.release()
        return bgr_image


if __name__ == '__main__':
    vision = Vision()
    vision.grab_still(".././temp/test.jpg")
    print("File saved at .././temp/test.jpg")
