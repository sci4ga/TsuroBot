#!/usr/bin/python
# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================
import time
import math
import smbus
import logging

logger = logging.getLogger(__name__)


class PCA9685:
    # Registers/etc.
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09

    def __init__(self, address=0x40):
        self._bus = smbus.SMBus(1)
        self._address = address
        self.setPWMFreq(60)
        logger.debug("Reseting PCA9685")
        self.reset()

    def __del__(self):
        self.reset()

    def write(self, reg, value):
        "Writes an 8-bit value to the specified register/address"
        self._bus.write_byte_data(self._address, reg, value)
        logger.debug("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

    def read(self, reg):
        "Read an unsigned byte from the I2C device"
        result = self._bus.read_byte_data(self._address, reg)
        logger.debug("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self._address, result & 0xFF, reg))
        return result

    def reset(self):
        logger.info("Reseting PCA9685")
        self.write(self.__MODE1, 0x00)

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        logger.debug("Setting PWM frequency to %d Hz" % freq)
        logger.debug("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        logger.debug("Final pre-scale: %d" % prescale)

        oldmode = self.read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.write(self.__LED0_ON_H+4*channel, on >> 8)
        self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.write(self.__LED0_OFF_H+4*channel, off >> 8)
        logger.debug("channel: %d  LED_ON: %d LED_OFF: %d" % (channel, on, off))

    def setServoPulse(self, channel, pulse):
        "Sets the Servo Pulse,The PWM frequency must be 50HZ"
        pulse = int(pulse*4096/20000)       # PWM frequency is 50HZ,the period is 20000us
        self.setPWM(int(channel), 0, pulse)


if __name__ == '__main__':
    pwm = PCA9685(0x40, debug=True)
    pwm.setPWMFreq(60)
    while True:
        # setServoPulse(2,2500)
        for i in range(500, 2500, 10):
            pwm.setServoPulse(1, i)
            time.sleep(0.02)

        for i in range(2500, 500, -10):
            pwm.setServoPulse(1, i)
            time.sleep(0.02)
