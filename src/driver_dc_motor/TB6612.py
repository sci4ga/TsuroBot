#!/usr/bin/env python
'''
This module is for SunFounder TB6612 the PCB board, a 2 Channel Motor Driver.
'''
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class Motor(object):
    ''' Motor driver class
        Set direction_channel to the GPIO channel which connect to MA,
        Set motor_B to the GPIO channel which connect to MB,
        Both GPIO channel use BCM numbering;
        Set pwm_channel to the PWM channel which connect to PWMA,
        Set pwm_B to the PWM channel which connect to PWMB;
        PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
    '''

    def __init__(self, direction_channel, pwm=None, offset=True):
        '''Init a motor on giving dir. channel and PWM channel.'''
        logger.info("Initializing dc motor with direction channel: {0}, pwm: {1}, offset: {2}".format(
                    str(direction_channel), str(pwm), str(offset)))
        self.direction_channel = direction_channel
        self._pwm = pwm
        self._offset = offset
        self.forward_offset = self._offset

        self.backward_offset = not self.forward_offset
        self._speed = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        logger.debug('setup motor direction channel at %s' % direction_channel)
        logger.debug('setup motor pwm channel')
        GPIO.setup(self.direction_channel, GPIO.OUT)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        ''' Set Speed with giving value '''
        if speed not in range(0, 101):
            raise ValueError('speed ranges fron 0 to 100, not "{0}"'.format(speed))
        if not callable(self._pwm):
            raise ValueError('pwm is not callable. Set Motor.pwm to a pwm control function with only 1 veriable speed')
        logger.debug('Set speed to: %s' % speed)
        self._speed = speed
        self._pwm(self._speed)

    def forward(self):
        ''' Set the motor direction to forward '''
        GPIO.output(self.direction_channel, self.forward_offset)
        self.speed = self._speed
        logger.debug('Motor moving forward (%s)' % str(self.forward_offset))

    def backward(self):
        ''' Set the motor direction to backward '''
        GPIO.output(self.direction_channel, self.backward_offset)
        self.speed = self._speed
        logger.debug('Motor moving backward (%s)' % str(self.backward_offset))

    def stop(self):
        ''' Stop the motor by giving a 0 speed '''
        logger.debug('Motor stop')
        self.speed = 0

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        ''' Set offset for much user-friendly '''
        if value not in (True, False):
            raise ValueError('offset value must be Bool value, not"{0}"'.format(value))
        self.forward_offset = value
        self.backward_offset = not self.forward_offset
        logger.debug('Set offset to %d' % self._offset)

    @property
    def pwm(self):
        return self._pwm

    @pwm.setter
    def pwm(self, pwm):
        logger.debug('pwm set')
        self._pwm = pwm
