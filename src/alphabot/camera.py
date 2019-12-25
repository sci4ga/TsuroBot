#!/usr/bin/env python
'''
A module to pan/tilt the camera and access the camera sensor
'''

from alphabot.vision import Vision
from alphabot.servo import Servo
import json
import logging

logger = logging.getLogger(__name__)


class Camera(object):
    '''Camera movement control class'''
    def __init__(self, config_file='./config_camera.json', bus_number=1):
        ''' Init the servo channel '''
        logger.info("Initializing Camera with bus_number: {0}, config: {1}".format(str(bus_number), str(config_file)))
        with open(config_file) as f:
            self.config = json.load(f)
        self.servos = Servo()
        self.servos.tilt_absolute(0)
        self.servos.pan_absolute(0)
        self.vision = Vision(config_file=config_file)

        # self.pan_servo.offset = self.config['pan_offset']
        # self.tilt_servo.offset = self.config['tilt_offset']

        """def calibrate_tilt(self, tilt):
        ''' Calibrate the camera to up '''
        self.config['tilt_offset'] += tilt
        self.tilt_servo.offset = self.config['tilt_offset']
        self.tilt_servo.write(self.tilt)

    def calibrate_pan(self, pan):
        ''' Calibrate the camera to left '''
        self.config['pan_offset'] += pan
        self.pan_servo.offset = self.config['pan_offset']
        self.pan_servo.write(self.pan)"""

    def save_calibration(self):
        ''' Save the calibration value '''
        with open(self.config["config_file"], 'w') as outfile:
            json.dump(self.config, outfile)
