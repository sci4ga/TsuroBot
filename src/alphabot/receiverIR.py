import RPi.GPIO as GPIO
import time
import logging
from typing import List, Tuple
import atexit


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up for {0}".format(__name__))


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Receiver_IR():
    def __init__(self):
        self.IR = 17
        self.keys = {0x45: "CH-",
                     0x47: "CH+",
                     0x46: "CH",
                     0x44: "<<",
                     0x40: ">>",
                     0x43: ">|",
                     0x07: "-",
                     0x15: "+",
                     0x09: "EQ",
                     0x16: "0",
                     0x19: "100+",
                     0x0d: "200+",
                     0x0c: "1",
                     0x18: "2",
                     0x5e: "3",
                     0x08: "4",
                     0x1c: "5",
                     0x5a: "6",
                     0x42: "7",
                     0x52: "8",
                     0x4a: "9"}

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IR, GPIO.IN)

    def read_IR(self) -> List[int]:
        """
        Read raw IR signal from receiver
        """
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

    def await_key(self) -> Tuple[str, int]:
        """
        Reads IR signals until a valid signal is received
        """
        key = None
        while key is None:
            data = self.read_IR()
            if data is not None:  # then validate the data, ignore if invalid
                if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
                    key = data[2]
        key_press = self.keys.get(key, "unkown")
        logger.info("Key press is {0}, signal hex({1})".format(key_press, hex(key)))
        return key_press, key


if __name__ == '__main__':
    """
    Awaits remote key presses and prints the key with signal received in hex
    """
    receiver = Receiver_IR()

    while True:
        key_press, key = receiver.await_key()
        print("Key press is {0}, signal hex({1})".format(key_press, hex(key)))
