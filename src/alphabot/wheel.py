'''
A module to actuate the wheel servo via TB6612FNG
'''
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class Wheel(object):
    def __init__(self, fwd_pin, rev_pin, pwm_pin):
        self.fwd_pin = fwd_pin
        self.rev_pin = rev_pin
        self.pwm_pin = pwm_pin
        self.freq = 500
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.fwd_pin, GPIO.OUT)
        GPIO.setup(self.rev_pin, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, 500)
        self.pwm.start(0)
        self.pw = 0

    @property
    def pw(self):
        return self._pw

    @pw.setter
    def pw(self, pw_val):
        self._pw = pw_val
        if((pw_val > 0) and (pw_val <= 100)):
            GPIO.output(self.fwd_pin, GPIO.HIGH)
            GPIO.output(self.rev_pin, GPIO.LOW)
            self.pwm.ChangeDutyCycle(pw_val)
        elif((pw_val < 0) and (pw_val >= -100)):
            GPIO.output(self.fwd_pin, GPIO.LOW)
            GPIO.output(self.rev_pin, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(0 - pw_val)
        elif(pw_val == 0):
            GPIO.output(self.fwd_pin, GPIO.LOW)
            GPIO.output(self.rev_pin, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
