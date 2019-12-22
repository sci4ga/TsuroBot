import RPi.GPIO as GPIO
import logging
import atexit


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up for {0}".format(__name__))


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Button():
    def __init__(self):
        self.CTR = 7
        self.A = 8
        self.B = 9
        self.C = 10
        self.D = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.CTR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.A, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.B, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.C, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.D, GPIO.IN, GPIO.PUD_UP)

    def get_input(self):
        signal = {}
        signal['center'] = not bool(GPIO.input(self.CTR))
        signal['a'] = not bool(GPIO.input(self.A))
        signal['b'] = not bool(GPIO.input(self.B))
        signal['c'] = not bool(GPIO.input(self.C))
        signal['d'] = not bool(GPIO.input(self.D))
        return signal

    def await_input(self):
        signal = {}
        while not any([signal[x] for x in signal]):
            signal = self.get_input()
        return signal
