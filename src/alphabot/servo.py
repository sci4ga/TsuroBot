#!/usr/bin/env python
'''
Driver module for servo, with PCA9685
'''

from alphabot.PCA9685 import PCA9685
import logging
import time

logger = logging.getLogger(__name__)


class Servo(object):
    def __init__(self):
        self.pwm = PCA9685(0x40)
        self.pwm.setPWMFreq(50)
        #Set servo parameters
        self.pulse_min = 500
        self.pulse_max = 2500
        self.v_offset = 0
        self.h_offset = 0
        self.HPulse = 1500  #Sets the initial Pulse
        self.HStep = 5      #Sets the initial step length
        self.VPulse = 1500  #Sets the initial Pulse
        self.VStep = 5      #Sets the initial step length
        self.pwm.setServoPulse(1, int(self.VPulse))
        self.pwm.setServoPulse(0, int(self.HPulse))

    def tilt_absolute(self, tilt):
        "tilt from -100 to 100"
        target_pulse = (self.pulse_max - self.pulse_min)/200 * (tilt + 100) + 500
        if target_pulse > self.pulse_max: 
            target_pulse = self.pulse_max
        if target_pulse < self.pulse_min: 
            target_pulse = self.pulse_min
        while(self.VPulse != target_pulse):
            if self.VPulse < target_pulse:
                self.VPulse += self.VStep
            elif self.VPulse > target_pulse:
                self.VPulse -= self.VStep            
            if self.VStep >= (self.VPulse - target_pulse) >= (-1 * self.VStep):
                self.VPulse = target_pulse
            self.pwm.setServoPulse(1, int(self.VPulse))
            time.sleep(0.01)
        return None

    def pan_absolute(self, pan):
        "pan from -100 to 100"
        if -100 > pan > 100:
            return None
        target_pulse = (self.pulse_max - self.pulse_min)/200 * (pan + 100) + 500
        if target_pulse > self.pulse_max: 
            target_pulse = self.pulse_max
        if target_pulse < self.pulse_min: 
            target_pulse = self.pulse_min
        while(self.HPulse != target_pulse):
            if self.HPulse < target_pulse:
                self.HPulse += self.HStep
            elif self.HPulse > target_pulse:
                self.HPulse -= self.HStep
            if self.HStep >= (self.HPulse - target_pulse) >= (-1 * self.HStep):
                self.HPulse = target_pulse
            self.pwm.setServoPulse(0, int(self.HPulse))
            time.sleep(0.01)
        return None

    def set_tilt_center(self, tilt_center):
        "offset tilt center from -50 to 50"
        if -50 > tilt_center > 50:
            return None
        self.v_offset = tilt_center
        return None

    def set_pan_center(self, pan_center):
        "offset pan center from -50 to 50"
        if -50 > pan_center > 50:
            return None
        self.h_offset = pan_center
        return None

    def tilt_relative(self, tilt):
        "tilt from -100 to 100 with offset"
        if -100 > tilt > 100:
            return None
        target_pulse = (self.pulse_max - self.pulse_min )/200 * (pan + 100) + 500
        offset_pulse = (self.pulse_max - self.pulse_min )/200 * (self.v_offset ) + 500
        target_pulse = target_pulse + offset_pulse
        if target_pulse > self.pulse_max:
            target_pulse = self.pulse_max
        if target_pulse < self.pulse_min:
            target_pulse = self.pulse_min
        while(self.VPulse != target_pulse):
            if self.VPulse < target_pulse:
                self.VPulse += self.VStep
            elif self.VPulse > target_pulse:
                self.VPulse -= self.VStep          
            if self.VStep >= (self.VPulse - target_pulse) >= (-1 * self.VStep):
                self.VPulse = target_pulse
            self.pwm.setServoPulse(0, int(self.VPulse))
            time.sleep(0.01)
        return None

    def pan_relative(self, pan):
        "pan from -100 to 100 with offset"
        if -100 > pan > 100:
            return None
        target_pulse = (self.pulse_max - self.pulse_min)/200 * (pan + 100) + 500
        offset_pulse = (self.pulse_max - self.pulse_min)/200 * (self.h_offset) + 500
        target_pulse = target_pulse + offset_pulse
        if target_pulse > self.pulse_max:
            target_pulse = self.pulse_max
        if target_pulse < self.pulse_min: 
            target_pulse = self.pulse_min
        while(self.HPulse != target_pulse):
            if self.HPulse < target_pulse:
                self.HPulse += self.HStep
            elif self.HPulse > target_pulse:
                self.HPulse -= self.HStep
            if self.HStep >= (self.HPulse - target_pulse) >= (-1 * self.HStep):
                self.HPulse = target_pulse
            self.pwm.setServoPulse(0, int(self.HPulse))
            time.sleep(0.01)
        return None
