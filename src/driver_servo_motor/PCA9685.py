#!/usr/bin/python
'''
This driver module is for SunFounder PCA9685 the PCB board, a 16-channel 12-bit I2C Bus PWM Driver.
'''

import smbus
import time
import math
import logging

logger = logging.getLogger(__name__)

class PWM(object):
    """A PWM control class for PCA9685."""
    _MODE1 = 0x00
    _MODE2 = 0x01
    _SUBADR1 = 0x02
    _SUBADR2 = 0x03
    _SUBADR3 = 0x04
    _PRESCALE = 0xFE
    _LED0_ON_L = 0x06
    _LED0_ON_H = 0x07
    _LED0_OFF_L = 0x08
    _LED0_OFF_H = 0x09
    _ALL_LED_ON_L = 0xFA
    _ALL_LED_ON_H = 0xFB
    _ALL_LED_OFF_L = 0xFC
    _ALL_LED_OFF_H = 0xFD

    _RESTART = 0x80
    _SLEEP = 0x10
    _ALLCALL = 0x01
    _INVRT = 0x10
    _OUTDRV = 0x04


    def __init__(self, bus_number=None, address=0x40):
        logger.info("Initializing PWM with bus_number: {0}, address: {1}".format(bus_number, address))
        self.address = address
        if bus_number is None:
            self.bus_number = 1
        else:
            self.bus_number = bus_number
        self.bus = smbus.SMBus(self.bus_number)


    def setup(self):
        '''Init the class with bus_number and address'''
        logger.debug('Reseting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.write_all_value(0, 0)
        self._write_byte_data(self._MODE2, self._OUTDRV)
        self._write_byte_data(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self._read_byte_data(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self._write_byte_data(self._MODE1, mode1)
        time.sleep(0.005)
        self._frequency = 60


    def _write_byte_data(self, reg, value):
        '''Write data to I2C with self.address'''
        logger.debug('Writing value %2X to %2X' % (value, reg))
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as i:
            logger.info(i)
            self._check_i2c()


    def _read_byte_data(self, reg):
        '''Read data from I2C with self.address'''
        logger.debug('Reading value from %2X' % reg)
        try:
            results = self.bus.read_byte_data(self.address, reg)
            return results
        except Exception as i:
            logger.info(i)
            self._check_i2c()


    def _check_i2c(self):
        import commands
        bus_number = 1
        logger.info("I2C bus number is: %s" % bus_number)
        logger.info("Checking I2C device:")
        cmd = "ls /dev/i2c-%d" % bus_number
        output = commands.getoutput(cmd)
        logger.info('Commands "%s" output:' % cmd)
        logger.info(output)
        if '/dev/i2c-%d' % bus_number in output.split(' '):
            logger.info("I2C device setup OK")
        else:
            logger.warning("Seems like I2C have not been set, Use 'sudo raspi-config' to set I2C")
        cmd = "i2cdetect -y %s" % self.bus_number
        output = commands.getoutput(cmd)
        logger.info("Your PCA9685 address is set to 0x%02X" % self.address)
        logger.info("i2cdetect output:")
        logger.info(output)
        outputs = output.split('\n')[1:]
        addresses = []
        for tmp_addresses in outputs:
            tmp_addresses = tmp_addresses.split(':')[1]
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(address)
        logger.info("Conneceted i2c device:")
        if addresses == []:
            logger.info("None")
        else:
            for address in addresses:
                logger.info("  0x%s" % address)
        if "%02X" % self.address in addresses:
            logger.info("I2C device is connected. Try running the program again or email info@Sci4GA.org.")
        else:
            logger.warning("Device is missing.")
            logger.warning("Check the address & wiring of PCA9685 Servo driver. Email info@Sci4GA.org if issue remains.")
        raise IOError('IO error')


    @property
    def frequency(self):
        return self._frequency


    @frequency.setter
    def frequency(self, freq):
        '''Set PWM frequency'''
        logger.debug('Set frequency to %d' % freq)
        self._frequency = freq
        prescale_value = 25000000.0
        prescale_value /= 4096.0
        prescale_value /= float(freq)
        prescale_value -= 1.0
        logger.debug('Setting PWM frequency to %d Hz' % freq)
        logger.debug('Estimated pre-scale: %d' % prescale_value)
        prescale = math.floor(prescale_value + 0.5)
        logger.debug('Final pre-scale: %d' % prescale)

        old_mode = self._read_byte_data(self._MODE1)
        new_mode = (old_mode & 0x7F) | 0x10
        self._write_byte_data(self._MODE1, new_mode)
        self._write_byte_data(self._PRESCALE, int(math.floor(prescale)))
        self._write_byte_data(self._MODE1, old_mode)
        time.sleep(0.005)
        self._write_byte_data(self._MODE1, old_mode | 0x80)


    def write(self, channel, on, off):
        '''Set on and off value on specific channel'''
        logger.debug('Set channel "%d" to value "%d"' % (channel, off))
        self._write_byte_data(self._LED0_ON_L+4*channel, on & 0xFF)
        self._write_byte_data(self._LED0_ON_H+4*channel, on >> 8)
        self._write_byte_data(self._LED0_OFF_L+4*channel, off & 0xFF)
        self._write_byte_data(self._LED0_OFF_H+4*channel, off >> 8)


    def write_all_value(self, on, off):
        '''Set on and off value on all channel'''
        logger.debug('Set all channel to value "%d"' % (off))
        self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
        self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
        self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
        self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)


    def map(self, x, in_min, in_max, out_min, out_max):
        '''To map the value from arange to another'''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == '__main__':
    pwm = PWM()
    pwm.frequency = 60
    for i in range(16):
        time.sleep(0.5)
        logger.info('\nChannel %d\n' % i)
        time.sleep(0.5)
        for j in range(4096):
            pwm.write(i, 0, j)
            logger.info('PWM value: %d' % j)
            time.sleep(0.0003)
