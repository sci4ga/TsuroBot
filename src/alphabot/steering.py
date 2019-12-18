'''
A module to steer the alphabot
'''
import time
from alphabot.wheel import Wheel
import logging

logger = logging.getLogger(__name__)


class Steering(object):
    '''Wheel movement control class'''
    def __init__(self):     
        self.right_wheel = Wheel(fwd_pin=13, rev_pin=12, pwm_pin=6)
        self.left_wheel = Wheel(fwd_pin=21, rev_pin=20, pwm_pin=26)

    def test(self):
        for i in range(100):
            # rotate counterclockwise
            self.right_wheel.pw = i
            self.left_wheel.pw = -1 * i
            time.sleep(0.01)
        for i in range(100):
            # rotate clockwise
            self.right_wheel.pw = -1 * i
            self.left_wheel.pw = i
            time.sleep(0.01)
        for i in range(100):
            # move forward
            self.right_wheel.pw = i
            self.left_wheel.pw = i
            time.sleep(0.01)
        for i in range(100):
            # move backward
            self.right_wheel.pw = -1 * i
            self.left_wheel.pw = -1 * i
            time.sleep(0.01)
        self.right_wheel.pw = 0
        self.left_wheel.pw = 0