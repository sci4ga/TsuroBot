#!/usr/bin/env python
'''
**********************************************************************
* Filename    : camera.py
* Description : A module to move the camera's up, down, left, right.
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
**********************************************************************
'''

from picar.SunFounder_PCA9685 import Servo
import time
import json
import logging

logger = logging.getLogger(__name__)


class Camera(object):
    '''Camera movement control class'''
    pan_channel = 1            # Pan servo channel
    tilt_channel = 2        # Tilt servo channel

    READY_PAN = 90            # Ready position angle
    READY_TILT = 90            # Ready position angle
    CALI_PAN = 90            # Calibration position angle
    CALI_TILT = 90            # Calibration position angle

    CAMERA_DELAY = 0.005
    PAN_STEP = 15                # Pan step = 5 degree
    TILT_STEP = 10            # Tilt step = 5 degree

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "camera.py":'

    def __init__(self, bus_number=1, config="config.json"):
        ''' Init the servo channel '''
        logger.info("Initializing Camera with bus_number: {0}, config: {1}".format(str(bus_number), str(config)))
        with open(config) as f:
            self.config = json.load(f)
        self.pan_offset = self.config['pan_offset']
        self.tilt_offset = self.config['tilt_offset']

        self.pan_servo = Servo.Servo(self.pan_channel, bus_number=bus_number, offset=self.pan_offset)
        self.tilt_servo = Servo.Servo(self.tilt_channel, bus_number=bus_number, offset=self.tilt_offset)

        logger.debug('Pan servo channel: {0}'.format(str(self.pan_channel)))
        logger.debug('Tilt servo channel: {0}'.format(str(self.tilt_channel)))
        logger.debug('Pan offset value: {0}'.format(str(self.pan_offset)))
        logger.debug('Tilt offset value: {0}'.format(str(self.tilt_offset)))

        self.current_pan = 0
        self.current_tilt = 0
        self.ready()

    def safe_plus(self, variable, plus_value):
        ''' Plus angle safely with no over ranges '''
        variable += plus_value
        if variable > 180:
            variable = 180
        if variable < 0:
            variable = 0
        return variable

    def turn_left(self, step=PAN_STEP):
        ''' Control the pan servo to make the camera turning left '''
        logger.debug('Turn left at step: {0}'.format(str(step)))
        self.current_pan = self.safe_plus(self.current_pan, step)
        self.pan_servo.write(self.current_pan)

    def turn_right(self, step=PAN_STEP):
        ''' Control the pan servo to make the camera turning right '''
        logger.debug('Turn right at step: {0}'.format(str(step)))
        self.current_pan = self.safe_plus(self.current_pan, -step)
        self.pan_servo.write(self.current_pan)

    def turn_up(self, step=TILT_STEP):
        ''' Control the tilt servo to make the camera turning up '''
        logger.debug('Turn up at step: {0}'.format(str(step)))
        self.current_tilt = self.safe_plus(self.current_tilt, step)
        self.tilt_servo.write(self.current_tilt)

    def turn_down(self, step=TILT_STEP):
        '''Control the tilt servo to make the camera turning down'''
        logger.debug('Turn down at step: {0}'.format(str(step)))
        self.current_tilt = self.safe_plus(self.current_tilt, -step)
        self.tilt_servo.write(self.current_tilt)

    def to_position(self, expect_pan, expect_tilt, delay=CAMERA_DELAY):
        '''Control two servo to write the camera to ready position'''
        pan_diff = self.current_pan - expect_pan
        tilt_diff = self.current_tilt - expect_tilt
        logger.debug('Turn to posision [%s, %s] (pan, tilt)' % (expect_pan, expect_tilt))
        while True:
            if pan_diff != 0 or tilt_diff != 0:
                pan_diff = self.current_pan - expect_pan
                tilt_diff = self.current_tilt - expect_tilt
                if abs(pan_diff) > 1:
                    if pan_diff < 0:
                        self.current_pan = self.safe_plus(self.current_pan, 1)
                    elif pan_diff > 0:
                        self.current_pan = self.safe_plus(self.current_pan, -1)
                else:
                    self.current_pan = expect_pan
                if abs(tilt_diff) > 1:
                    if tilt_diff < 0:
                        self.current_tilt = self.safe_plus(self.current_tilt, 1)
                    elif tilt_diff > 0:
                        self.current_tilt = self.safe_plus(self.current_tilt, -1)
                else:
                    self.current_tilt = expect_tilt

                self.pan_servo.write(self.current_pan)
                self.tilt_servo.write(self.current_tilt)
                time.sleep(delay)
            else:
                break

    def ready(self):
        ''' Set the camera to ready position '''
        logger.debug('Turn to "Ready" position')
        self.pan_servo.offset = self.pan_offset
        self.tilt_servo.offset = self.tilt_offset
        self.current_pan = self.READY_PAN
        self.current_tilt = self.READY_TILT
        self.pan_servo.write(self.current_pan)
        self.tilt_servo.write(self.current_tilt)

    def calibration(self):
        ''' Control two servo to write the camera to calibration position '''
        logger.debug('Turn to "Calibration" position')
        self.pan_servo.write(self.CALI_PAN)
        self.tilt_servo.write(self.CALI_TILT)
        self.cali_pan_offset = self.pan_offset
        self.cali_tilt_offset = self.tilt_offset

    def cali_up(self):
        ''' Calibrate the camera to up '''
        self.cali_tilt_offset += 1
        self.tilt_servo.offset = self.cali_tilt_offset
        self.tilt_servo.write(self.CALI_TILT)

    def cali_down(self):
        ''' Calibrate the camera to down '''
        self.cali_tilt_offset -= 1
        self.tilt_servo.offset = self.cali_tilt_offset
        self.tilt_servo.write(self.CALI_TILT)

    def cali_left(self):
        ''' Calibrate the camera to left '''
        self.cali_pan_offset += 1
        self.pan_servo.offset = self.cali_pan_offset
        self.pan_servo.write(self.CALI_PAN)

    def cali_right(self):
        ''' Calibrate the camera to right '''
        self.cali_pan_offset -= 1
        self.pan_servo.offset = self.cali_pan_offset
        self.pan_servo.write(self.CALI_PAN)

    def cali_ok(self):
        ''' Save the calibration value '''
        self.pan_offset = self.cali_pan_offset
        self.tilt_offset = self.cali_tilt_offset
        self.config['pan_offset'] = self.pan_offset
        self.config['tilt_offset'] = self.tilt_offset
        with open(config, 'w') as outfile:
            json.dump(self.config, outfile)

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        ''' Set if debug information shows '''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            logger.info(self._DEBUG_INFO, "Set debug on")
            logger.info(self._DEBUG_INFO, "Set pan servo and tilt servo debug on")
            self.pan_servo.debug = True
            self.tilt_servo.debug = True
        else:
            logger.info(self._DEBUG_INFO, "Set debug off")
            logger.info(self._DEBUG_INFO, "Set pan servo and tilt servo debug off")
            self.pan_servo.debug = False
            self.tilt_servo.debug = False


if __name__ == '__main__':
    camera = Camera()
    try:
        for i in range(0, 36):
            logger.info("pan moving left     ", i)
            camera.pan_left()
            time.sleep(camera.CAMERA_DELAY*camera.PAN_STEP)
        for i in range(0, 36):
            logger.info("pan moving right    ", i)
            camera.pan_right()
            time.sleep(camera.CAMERA_DELAY*camera.PAN_STEP)
        for i in range(0, 36):
            logger.info("tilt moving up      ", i)
            camera.tilt_up()
            time.sleep(camera.CAMERA_DELAY*camera.TILT_STEP)
        for i in range(0, 36):
            logger.info("tilt moving right   ", i)
            camera.tilt_down()
            time.sleep(camera.CAMERA_DELAY*camera.TILT_STEP)

        logger.info("Camera move to ready position")
        camera.ready()

        logger.info("Camera move to position (0, 0)")
        camera.to_posision(0, 0)
        logger.info("Camera move to position (180, 180)")
        camera.to_posision(180, 180)

        logger.info("Camera move to ready position")
        camera.ready()
    except KeyboardInterrupt:
        camera.ready()
