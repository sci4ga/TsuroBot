#!/usr/bin/python

# sudo pip install rpi_ws281x
from rpi_ws281x import Adafruit_NeoPixel, Color
import logging
import _rpi_ws281x as ws
logger = logging.getLogger(__name__)


class LED:
    """Control LED's 1-4"""
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
        [self.set_led(x, 0, 0, 0) for x in range(4)]

    def set_led(self, led_num: int, red: int, green: int, blue: int):
        """Set LED color using 0-255 RGB values"""
        logger.debug(f"led_num {led_num} color set to red={red}, green={green}, blue={blue}")
        self.strip.setPixelColor(led_num, Color(red, green, blue))
        logger.debug("show color")
        self.strip.show()
        return None


if __name__ == '__main__':
    led = LED()
    blink = True
    import time
    while True:
        if blink:
            led.set_led(0, 255, 0, 0)  # red
            led.set_led(1, 0, 255, 0)  # green
            led.set_led(2, 0, 0, 255)  # blue
            led.set_led(3, 0, 255, 255)  # yellow
            print("LED's ON.")
            blink = False
            time.sleep(1)
        else:
            led.set_led(0, 0, 0, 0)  # red
            led.set_led(1, 0, 0, 0)  # green
            led.set_led(2, 0, 0, 0)  # blue
            led.set_led(3, 0, 0, 0)  # yellow
            print("LED's OFF.")
            blink = True
            time.sleep(1)
