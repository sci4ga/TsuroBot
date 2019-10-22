'''
A module to steer the alphabot
'''

from driver_servo_motor.wheel import Wheel
import logging

logger = logging.getLogger(__name__)


class Steering(object):
    '''Wheel movement control class'''
    def __init__(self):
        self.left_wheel = Wheel(fwd_pin=21, rev_pin=20, pwm_pin=26)
        self.right_wheel = Wheel(fwd_pin=13, rev_pin=12, pwm_pin=6)
