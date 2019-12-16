#!/usr/bin/env python
'''
A module to pan/tilt the camera and access the camera sensor
'''

from driver_camera.vision import Vision
from driver_servo_motor.servo import Servo
import time
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
        # TODO: adapt the servos to alphabot 
        # self.pan_servo = Servo(self.config["cam_servo_pan_channel"], bus_number=bus_number, offset=self.config['pan_offset'])
        # self.tilt_servo = Servo(self.config["cam_servo_tilt_channel"], bus_number=bus_number, offset=self.config['tilt_offset'])
        self.servos = Servo()
        self.servos.tilt_absolute(0)
        self.servos.pan_absolute(0)
        self.vision = Vision(config_file=config_file)

        """logger.debug('Pan servo channel: {0}'.format(str(self.config["cam_servo_pan_channel"])))
        logger.debug('Tilt servo channel: {0}'.format(str(self.config["cam_servo_tilt_channel"])))
        logger.debug('Pan offset value: {0}'.format(str(self.config['pan_offset'])))
        logger.debug('Tilt offset value: {0}'.format(str(self.config['tilt_offset'])))"""

        #self.pan_servo.offset = self.config['pan_offset']
        #self.tilt_servo.offset = self.config['tilt_offset']



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

