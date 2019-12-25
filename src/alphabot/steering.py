'''
A module to steer the alphabot
'''
from alphabot.wheel import Wheel
import logging

logger = logging.getLogger(__name__)


class Steering:
    '''The Steering class coordinates wheel movement of the alphabot2'''
    def __init__(self):
        self.right_wheel = Wheel(fwd_pin=13, rev_pin=12, pwm_pin=6)
        self.left_wheel = Wheel(fwd_pin=21, rev_pin=20, pwm_pin=26)

    def turn(self, radius: int):
        """This method initiates a turn of a given radius"""
        # TODO: Map pwm to turn radius
        raise(NotImplementedError)


if __name__ == '__main__':
    """
    This example rotates the alphabot2 back and forth
    """
    # TODO: Implement an example of the Steering class
    steering = Steering()
