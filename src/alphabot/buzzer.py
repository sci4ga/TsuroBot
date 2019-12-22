import RPi.GPIO as GPIO
import time
import logging
from typing import Optional
import atexit


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up for {0}".format(__name__))


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Buzzer():
    def __init__(self):
        self.channel = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

    def on(self):
        GPIO.output(self.channel, GPIO.HIGH)

    def off(self):
        GPIO.output(self.channel, GPIO.LOW)

    def beep(self, seconds: Optional[int] = 0.1):
        self.on()
        time.sleep(seconds)
        self.off()


if __name__ == '__main__':
    buzzer = Buzzer()
    buzzer.beep(0.05)
    print("The buzzer has beeped.")
