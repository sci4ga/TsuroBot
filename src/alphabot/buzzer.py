import RPi.GPIO as GPIO
import time
import logging
from typing import Optional
import atexit


def cleanup():
    GPIO.cleanup()
    print(f"GPIO cleaned up for {__name__}")


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Buzzer:
    """The Buzzer class actuates the buzzer on the Alphabot2."""
    def __init__(self, channel: Optional[int] = 4):
        self._channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._channel, GPIO.OUT)
        self.on = False

    @property
    def on(self):
        return self.__on

    @on.setter
    def on(self, val: bool):
        if val:
            self.__on = True
            GPIO.output(self._channel, GPIO.HIGH)
        else:
            self.__on = False
            GPIO.output(self._channel, GPIO.LOW)

    def beep(self, seconds: Optional[int] = 0.1):
        self.on = True
        time.sleep(seconds)
        self.on = False


if __name__ == '__main__':
    buzzer = Buzzer()
    buzzer.beep(0.05)
    print("The buzzer has beeped.")
