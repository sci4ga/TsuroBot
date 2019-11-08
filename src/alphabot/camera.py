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
        self.pan_servo = Servo(self.config["cam_servo_pan_channel"], bus_number=bus_number, offset=self.config['pan_offset'])
        self.tilt_servo = Servo(self.config["cam_servo_tilt_channel"], bus_number=bus_number, offset=self.config['tilt_offset'])
        self.vision = Vision(config_file = config_file)

        logger.debug('Pan servo channel: {0}'.format(str(self.config["cam_servo_pan_channel"])))
        logger.debug('Tilt servo channel: {0}'.format(str(self.config["cam_servo_tilt_channel"])))
        logger.debug('Pan offset value: {0}'.format(str(self.config['pan_offset'])))
        logger.debug('Tilt offset value: {0}'.format(str(self.config['tilt_offset'])))

        self.pan_servo.offset = self.config['pan_offset']
        self.tilt_servo.offset = self.config['tilt_offset']
        self.pan = self.config["center_pan"]
        self.tilt = self.config["center_tilt"]

    @property
    def pan(self):
        return self.__pan

    @pan.setter
    def pan(self, val):
        if val > 180:
            val = 180
        if val < 0:
            val = 0
        self.__pan = val

    @property
    def tilt(self):
        return self.__tilt

    @tilt.setter
    def tilt(self, val):
        if val > 180:
            val = 180
        if val < 0:
            val = 0
        self.__tilt = val

    def look_at(self, target_pan=None, target_tilt=None, servo_delay=None):
        '''Control two servo to write the camera to ready position'''
        # Pan step 15 ~= 5 degrees
        # Tilt step 10 ~= 5 degrees
        if target_pan is None:
            target_pan = self.pan
        if target_tilt is None:
            target_tilt = self.tilt
        if target_pan < 0 or target_pan > 180 or target_tilt < 0 or target_tilt > 180:
            raise ValueError("Pan and Tilt must be between 0 and 180. Found pan: {0}, tilt: {1}".format(target_pan, target_tilt))
        logger.debug('Move position from [{0}, {1}] (pan, tilt)'.format(self.pan, self.tilt))
        while self.pan != target_pan or self.tilt != target_tilt:
            if target_pan > self.pan:
                self.pan += 1
            if target_pan < self.pan:
                self.pan -= 1
            if target_tilt > self.tilt:
                self.tilt += 1
            if target_tilt < self.tilt:
                self.tilt -= 1
            self.pan_servo.write(self.pan)
            self.tilt_servo.write(self.tilt)
            if servo_delay is None:
                time.sleep(self.config["cam_servo_delay"])
            else:
                time.sleep(servo_delay)
        logger.debug('Position set to [{0}, {1}] (pan, tilt)'.format(target_pan, target_tilt))

    def look_center(self):
        ''' Set the camera to center position '''
        logger.debug('Turn to "Center" position')
        self.look_at(target_pan=self.config["center_pan"], target_tilt=self.config["center_tilt"])

    def calibrate_tilt(self, tilt):
        ''' Calibrate the camera to up '''
        self.config['tilt_offset'] += tilt
        self.tilt_servo.offset = self.config['tilt_offset']
        self.tilt_servo.write(self.tilt)

    def calibrate_pan(self, pan):
        ''' Calibrate the camera to left '''
        self.config['pan_offset'] += pan
        self.pan_servo.offset = self.config['pan_offset']
        self.pan_servo.write(self.pan)

    def save_calibration(self):
        ''' Save the calibration value '''
        with open(self.config["config_file"], 'w') as outfile:
            json.dump(self.config, outfile)

