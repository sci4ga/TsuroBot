#!/usr/bin/env python
'''
A module to control the back wheels of RPi Car
'''

from driver_dc_motor import TB6612
from driver_servo_motor import PCA9685
import json
import logging

logger = logging.getLogger(__name__)


class Back_Wheels(object):
    ''' Back wheels control class '''
    Motor_A = 17
    Motor_B = 27

    PWM_A = 4
    PWM_B = 5

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "back_wheels.py":'

    def __init__(self, config, debug=False, bus_number=1):
        ''' Init the direction channel and pwm channel '''
        with open(config) as f:
            self.config = json.load(f)

        self.debug = debug
        self.left_wheel = TB6612.Motor(self.Motor_A, offset=self.config["left_polarity_correction"])
        self.right_wheel = TB6612.Motor(self.Motor_B, offset=self.config["right_polarity_correction"])
        self.pwm = PCA9685.PWM(bus_number=bus_number)
        self.left_wheel.debug = debug
        self.right_wheel.debug = debug
        self.pwm.debug = debug

        def _set_a_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_A, 0, pulse_wide)

        def _set_b_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_B, 0, pulse_wide)

        self.left_wheel.pwm = _set_a_pwm
        self.right_wheel.pwm = _set_b_pwm

        self._speed = 0


    def _debug_(self, message):
        if self.debug:
            logger.info(message)

    def forward(self):
        ''' Move both wheels forward '''
        self.left_wheel.forward()
        self.right_wheel.forward()
        self._debug_('Running forward')

    def backward(self):
        ''' Move both wheels backward '''
        self.left_wheel.backward()
        self.right_wheel.backward()
        self._debug_('Running backward')

    def stop(self):
        ''' Stop both wheels '''
        self.left_wheel.stop()
        self.right_wheel.stop()
        self._debug_('Stop')

    @property
    def speed(self, speed):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        ''' Set moving speeds '''
        self.left_wheel.speed = self._speed
        self.right_wheel.speed = self._speed
        self._debug_('Set speed to %s' % self._speed)

    def calibrate_left_polarity(self):
        ''' Reverse the left wheels forward direction in calibration '''
        self.config["left_polarity_correction"] = not self.config["left_polarity_correction"]
        self.left_wheel.offset = self.config["left_polarity_correction"]
        with open(config, 'w') as outfile:
            json.dump(self.config, outfile)

    def calibrate_right_polarity(self):
        ''' Reverse the right wheels forward direction in calibration '''
        self.config["right_polarity_correction"] = not self.config["right_polarity_correction"]
        self.right_wheel.offset = self.config["right_polarity_correction"]
        with open(config, 'w') as outfile:
            json.dump(self.config, outfile)


if __name__ == '__main__':
    test()
