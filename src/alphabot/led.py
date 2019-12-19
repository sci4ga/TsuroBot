#!/usr/bin/python

# sudo pip install rpi_ws281x
from rpi_ws281x import Adafruit_NeoPixel, Color, ws
import logging

logger = logging.getLogger(__name__)


class LED:
    """Control LED's 0-4"""
    def __init__(self):
        # LED strip configuration:
        LED_COUNT = 4      # Number of LED pixels.
        LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 5       # DMA channel to use for generating signal (try 5)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0
        LED_STRIP = ws.WS2811_STRIP_RGB
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.strip.setPixelColor(0, Color(255, 0, 0))
        self.strip.setPixelColor(1, Color(0, 255, 0))
        self.strip.setPixelColor(2, Color(0, 0, 255))
        self.strip.setPixelColor(3, Color(0, 255, 255))
        self.strip.show()

    def set_led(self, led_num, red, green, blue):
        """Set LED color using 0-255 RGB values"""
        logger.debug("led_num {0} color set to red={1}, green={2}, blue={3}".format(led_num, red, green, blue))
        self.strip.setPixelColor(led_num, Color(red, green, blue))
        logger.debug("show color")
        self.strip.show()
        return None
