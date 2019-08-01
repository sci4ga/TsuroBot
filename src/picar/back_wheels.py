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
    # Direction channels
    Motor_A = 17
    Motor_B = 27

    # PWM channels
    PWM_A = 4
    PWM_B = 5

    def __init__(self, config_file, bus_number=1):
        ''' Init the direction channel and pwm channel '''

        logger.info("Initializing back wheels with bus number: {0}, config_file: {1}".format( 
                    str(bus_number), str(config_file)))
        
        with open(config_file) as f:
            self.config = json.load(f)

        self.left_wheel = TB6612.Motor(self.Motor_A, offset=self.config["left_polarity_correction"])
        self.right_wheel = TB6612.Motor(self.Motor_B, offset=self.config["right_polarity_correction"])
        self.pwm = PCA9685.PWM(bus_number=bus_number)
        self.pwm.setup()

        def _set_a_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_A, 0, pulse_wide)

        def _set_b_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_B, 0, pulse_wide)

        self.left_wheel.pwm = _set_a_pwm
        self.right_wheel.pwm = _set_b_pwm

        self._speed = 0

    def forward(self):
        ''' Move both wheels forward '''
        self.left_wheel.forward()
        self.right_wheel.forward()
        logger.debug('Run dc motors forward')

    def backward(self):
        ''' Move both wheels backward '''
        self.left_wheel.backward()
        self.right_wheel.backward()
        logger.debug('Run dc motors backward')

    def stop(self):
        ''' Stop both wheels '''
        self.left_wheel.stop()
        self.right_wheel.stop()
        logger.debug('Stop')

    @property
    def speed(self, speed):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        ''' Set moving speeds '''
        self.left_wheel.speed = self._speed
        self.right_wheel.speed = self._speed
        logger.debug('Set speed to %s' % self._speed)

    def calibrate_left_polarity(self):
        ''' Reverse the left wheels forward direction in calibration '''
        
        self.config["left_polarity_correction"] = not self.config["left_polarity_correction"]
        self.left_wheel.offset = self.config["left_polarity_correction"]
        self.save_config()
        logger.info("Left wheel polarity correction set to {0}".format(self.config["left_polarity_correction"]))

    def calibrate_right_polarity(self):
        ''' Reverse the right wheels forward direction in calibration '''
        self.config["right_polarity_correction"] = not self.config["right_polarity_correction"]
        self.right_wheel.offset = self.config["right_polarity_correction"]
        self.save_config()
        logger.info("Right wheel polarity correction set to {0}".format(self.config["right_polarity_correction"]))
    
    def save_config(self):
        with open(config, 'w') as outfile:
            json.dump(self.config, outfile)


if __name__ == '__main__':
    test()
