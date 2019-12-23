import RPi.GPIO as GPIO
import logging
from typing import Optional
import atexit


def cleanup():
    GPIO.cleanup()
    print(f"GPIO cleaned up for {__name__}")


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Front_IR:
    """The Front_IR class takes readings from the Alphabot2 front IR sensors"""
    def __init__(self, right_ch: Optional[int] = 16, left_ch: Optional[int] = 19):
        logger.info("Initializing front IR")
        self._right_channel = right_ch
        self._left_channel = left_ch
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._right_channel, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._left_channel, GPIO.IN, GPIO.PUD_UP)
        logger.info(f"Left GPIO setup: {self._left_channel}")
        logger.info(f"Right GPIO setup: {self._right_channel}")

    def read_sensors(self):
        signal = {}
        signal["left"] = GPIO.input(self._left_channel)
        signal["right"] = GPIO.input(self._right_channel)
        logger.debug(f"Front IR reading: {signal}")
        return signal


if __name__ == '__main__':
    import time
    ir = Front_IR()

    while True:
        signal = ir.read_sensors()
        print(f"Front IR reading: {signal}")
        time.sleep(0.05)
