#!/usr/bin/env python
'''
A module to control the front wheels of RPi Car
'''
from driver_servo_motor import Servo
import json
import logging

logger = logging.getLogger(__name__)

class Front_Wheels(object):
    ''' Front wheels control class '''

    def __init__(self, config_file="./config_wheels.json", bus_number=1, channel=0):
        ''' setup channels and basic stuff '''
        logger.info("Initializing front wheels with bus number: {0}, config_file: {1}, channel: {2}".format(
                    str(bus_number), str(config_file), str(channel)))
        with open(config_file) as f:
            self.config = json.load(f)
        logger.info(str(self.config))
        self._straight_angle = 90
        self.turning_max = 45
        self._turning_offset = self.config['turning_offset']

        self.steering = Servo.Servo(channel, bus_number=bus_number, offset=self.turning_offset)
        logger.debug('Front wheel PWM channel: %s' % channel)
        logger.debug('Front wheel offset value: %s ' % self.turning_offset)

        self._angle = {"left": self._min_angle, "straight": self._straight_angle, "right": self._max_angle}
        logger.debug('left angle: %s, straight angle: %s, right angle: %s' % (self._angle["left"], self._angle["straight"], self._angle["right"]))
        self.steering.setup()

    def turn_left(self):
        ''' Turn the front wheels left '''
        logger.debug("Turn left")
        self.steering.write(self._angle["left"])

    def turn_straight(self):
        ''' Turn the front wheels back straight '''
        logger.debug("Turn straight")
        self.steering.write(self._angle["straight"])

    def turn_right(self):
        ''' Turn the front wheels right '''
        logger.debug("Turn right")
        self.steering.write(self._angle["right"])

    def turn(self, angle):
        ''' Turn the front wheels to the giving angle '''
        logger.debug("Turn to %s " % angle)
        if angle < self._angle["left"]:
            angle = self._angle["left"]
        if angle > self._angle["right"]:
            angle = self._angle["right"]
        self.steering.write(angle)

    @property
    def turning_max(self):
        return self._turning_max

    @turning_max.setter
    def turning_max(self, angle):
        self._turning_max = angle
        self._min_angle = self._straight_angle - angle
        self._max_angle = self._straight_angle + angle
        self._angle = {"left": self._min_angle, "straight": self._straight_angle, "right": self._max_angle}

    @property
    def turning_offset(self):
        return self._turning_offset

    @turning_offset.setter
    def turning_offset(self, value):
        if not isinstance(value, int):
            raise TypeError('"turning_offset" must be "int"')
        self._turning_offset = value
        self.config["turning_offset"] = value
        self.steering.offset = value

    def calibrate_left(self):
        ''' Calibrate the wheels to left '''
        self.turning_offset -= 1
        self.turn_straight()

    def calibrate_right(self):
        ''' Calibrate the wheels to right '''
        self.turning_offset += 1
        self.turn_straight()

    def save_config(self):
        with open(self.config["config_file"], 'w') as outfile:
            json.dump(self.config, outfile)
