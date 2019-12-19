import RPi.GPIO as GPIO
import time
import logging

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

    def beep(self, seconds=0.1):
        self.on()
        time.sleep(seconds)
        self.off()
