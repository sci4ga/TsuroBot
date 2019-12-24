'''
A module to actuate the wheel servo via TB6612FNG
'''
import RPi.GPIO as GPIO
import logging
import atexit


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up for {0}".format(__name__))


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Wheel:
    """The Wheel class actuates the servos at the wheels of the alphabot2"""
    def __init__(self, fwd_pin: int, rev_pin: int, pwm_pin: int):
        self._fwd_pin = fwd_pin
        self._rev_pin = rev_pin
        self._pwm_pin = pwm_pin
        self._freq = 500
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._fwd_pin, GPIO.OUT)
        GPIO.setup(self._rev_pin, GPIO.OUT)
        GPIO.setup(self._pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self._pwm_pin, self._freq)
        self.pwm.start(0)
        self.pw = 0

    @property
    def pw(self):
        return self.__pw

    @pw.setter
    def pw(self, pw_val: int):
        self.__pw = pw_val
        if((pw_val > 0) and (pw_val <= 100)):
            GPIO.output(self._fwd_pin, GPIO.HIGH)
            GPIO.output(self._rev_pin, GPIO.LOW)
            self.pwm.ChangeDutyCycle(pw_val)
        elif((pw_val < 0) and (pw_val >= -100)):
            GPIO.output(self._fwd_pin, GPIO.LOW)
            GPIO.output(self._rev_pin, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(0 - pw_val)
        elif(pw_val == 0):
            GPIO.output(self._fwd_pin, GPIO.LOW)
            GPIO.output(self._rev_pin, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)


if __name__ == '__main__':
    """
    This example rotates the alphabot2 back and forth
    """
    import time
    right_wheel = Wheel(fwd_pin=13, rev_pin=12, pwm_pin=6)
    left_wheel = Wheel(fwd_pin=21, rev_pin=20, pwm_pin=26)
    clockwise = True
    while True:
        if clockwise:
            print(f"Rotate clockwise")
            right_wheel.pw = 20
            left_wheel.pw = -20
            time.sleep(.5)
            clockwise = False
        else:
            print("Rotate counterclockwise")
            right_wheel.pw = -20
            left_wheel.pw = 20
            time.sleep(.5)
            clockwise = True
        print("stop")
        right_wheel.pw = 0
        left_wheel.pw = 0
        time.sleep(1)
