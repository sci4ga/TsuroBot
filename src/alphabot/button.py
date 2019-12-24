import RPi.GPIO as GPIO
import logging
import atexit


def cleanup():
    GPIO.cleanup()
    print(f"GPIO cleaned up for {__name__}")


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Button:
    """The Button class reads from the alphabot2 joystick."""
    def __init__(self):
        self._buttons = {"CTR": 7,
                         "A": 8,
                         "B": 9,
                         "C": 10,
                         "D": 11}
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for x in self._buttons:
            GPIO.setup(self._buttons[x], GPIO.IN, GPIO.PUD_UP)

    def read_input(self) -> dict:
        """Read button input"""
        signal = {}
        for x in self._buttons:
            signal[x] = not bool(GPIO.input(self._buttons[x]))
        return signal

    def await_input(self) -> str:
        """Wait for button press and return the name of the button."""
        signal = {}
        while not any([signal[x] for x in signal]):
            signal = self.read_input()
        button_press = [x for x in signal if signal[x]][0]
        return button_press


if __name__ == '__main__':
    button = Button()
    import time
    print("Waiting for a button press.")
    while True:
        button_press = button.await_input()
        print(f"Button press: {button_press}")
        time.sleep(0.5)
