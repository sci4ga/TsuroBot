import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class Front_IR():
    def __init__(self):
        self.right_channel = 16
        self.left_channel = 19
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.right_channel,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.left_channel,GPIO.IN,GPIO.PUD_UP)
        logger.info("Left GPIO setup: {0}".format(str(self.left_channel)))
        logger.info("Right GPIO setup: {0}".format(str(self.right_channel)))

    def get_front_ir(self):
        signal = {}
        print("get_front_ir")
        signal["left"] = GPIO.input(self.left_channel)
        signal["right"] = GPIO.input(self.right_channel)
        print("Left: {0}".format(str(signal["left"])))
        print("Right: {0}".format(str(signal["right"])))
        return signal


if __name__=='__main__':
    ir = Front_IR()
    signal = {}
    print(str(ir.get_signal()))
    while not any([signal[x] for x in signal]):
        signal = ir.get_signal()
    print(str(signal))
