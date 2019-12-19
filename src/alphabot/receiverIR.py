import RPi.GPIO as GPIO
import time
import logging

logger = logging.getLogger(__name__)
logger.info("logging from IR receiver: {0}".format(__name__))


class Receiver_IR():
    def __init__(self):
        self.IR = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IR, GPIO.IN)

    def getkey(self):
        if GPIO.input(self.IR) == 0:
            count = 0
            while GPIO.input(self.IR) == 0 and count < 200:  # 9ms
                count += 1
                time.sleep(0.00006)
            if(count < 10):
                return
            count = 0
            while GPIO.input(self.IR) == 1 and count < 80:  # 4.5ms
                count += 1
                time.sleep(0.00006)

            idx = 0
            cnt = 0
            data = [0, 0, 0, 0]
            for i in range(0, 32):
                count = 0
                while GPIO.input(self.IR) == 0 and count < 15:    # 0.56ms
                    count += 1
                    time.sleep(0.00006)

                count = 0
                while GPIO.input(self.IR) == 1 and count < 40:   # 0: 0.56mx
                    count += 1                               # 1: 1.69ms
                    time.sleep(0.00006)

                if count > 7:
                    data[idx] |= 1 << cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            logger.debug("got: " + str(data))
            return data

    def await_key(self):
        key = None
        while key is None:
            data = self.getkey()
            if data is not None:
                if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  # check
                    key = data[2]
        if key == 0x18:
            logger.info("key is 2")
        if key == 0x08:
            logger.info("key is 4")
        if key == 0x1c:
            logger.info("key is 5")
        if key == 0x5a:
            logger.info("key is 6")
        if key == 0x52:
            logger.info("key is 8")
        if key == 0x15:
            logger.info("key is +")
        if key == 0x07:
            logger.info("key is -")
        else:
            logger.info("unknown key is val: " + str(key))
        return key
