#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import logging
import atexit
from typing import Optional


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up for {0}".format(__name__))


atexit.register(cleanup)
logger = logging.getLogger(__name__)


class Bottom_IR:

    def __init__(self, numSensors: Optional[int] = 5):
        self._numSensors = numSensors
        self.calibratedMin = [0] * self._numSensors
        self.calibratedMax = [1023] * self._numSensors
        self.last_value = 0
        self._CS = 5
        self._Clock = 25
        self._Address = 24
        self._DataOut = 23
        self._historySize = 333
        self.history = [{}] * self._historySize
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._Clock, GPIO.OUT)
        GPIO.setup(self._Address, GPIO.OUT)
        GPIO.setup(self._CS, GPIO.OUT)
        GPIO.setup(self._DataOut, GPIO.IN, GPIO.PUD_UP)

    """
    Reads the sensor values into an array. There *MUST* be space
    for as many values as there were sensors specified in the constructor.
    Example usage:
    unsigned int sensor_values[8];
    sensors.read(sensor_values);
    The values returned are a measure of the reflectance in abstract units,
    with higher values corresponding to higher reflectance (e.g. a white
    surface or a bright light).
    """
    def get_analog_read(self) -> dict:
        #TODO: make this not garbage
        value = [0]*(self._numSensors+1)
        analog_read = {}
        # Read Channel0~channel6 AD value
        for j in range(0, self._numSensors+1):
            GPIO.output(self._CS, GPIO.LOW)  # turn on IR light
            #keep in mind: everything here does stuff bit by bit
            for i in range(0, 4):
                # sent 4-bit self._Address
                # Sends byte representation of sensor number to output channel
                # AKA tells output which sensor is sending it info
                # send bit x of the address
                if(((j) >> (3 - i)) & 0x01):
                    GPIO.output(self._Address, GPIO.HIGH)
                else:
                    GPIO.output(self._Address, GPIO.LOW)

                # read MSB 4-bit data
                # double the sensor number and store it into value
                # Check if there's any input from the data channel
                # if so, add one to the value
                # AKA store whether or not each sensor took an input or not
                # send bit x of the sensor data
                value[j] <<= 1
                if(GPIO.input(self._DataOut)):
                    value[j] |= 0x01

                #Tells the io clock to move forward in time
                GPIO.output(self._Clock, GPIO.HIGH)
                GPIO.output(self._Clock, GPIO.LOW)
            for i in range(0, 6):
                # read LSB 8-bit data
                # send bit x of the sensor data
                value[j] <<= 1
                if(GPIO.input(self._DataOut)):
                    value[j] |= 0x01
                GPIO.output(self._Clock, GPIO.HIGH)
                GPIO.output(self._Clock, GPIO.LOW)
            time.sleep(0.0001)
            GPIO.output(self._CS, GPIO.HIGH)  # turn off IR light

        for x in range(1, 6):
            analog_read[x] = value[x]
        logger.debug(str(analog_read))
        self.history.append(analog_read)
        self.history = self.history[1:self._historySize + 1]
        return analog_read

    """
    Reads the sensors 10 times and uses the results for
    calibration.  The sensor values are not returned; instead, the
    maximum and minimum values found over time are stored internally
    and used for the readCalibrated() method.
    """
    def calibrate(self):
        #TODO: change calibrate so we can set the time we are in calibration
        #TODO: or alternatively a "start calibration" and "stop calibration" function each
        max_sensor_values = [0]*self._numSensors
        min_sensor_values = [0]*self._numSensors
        for j in range(0, 10):

            sensor_values = self.get_analog_read()

            for i in range(0, self._numSensors):
                # set the max we found THIS time
                if((j == 0) or max_sensor_values[i] < sensor_values[i]):
                    max_sensor_values[i] = sensor_values[i]

                # set the min we found THIS time
                if((j == 0) or min_sensor_values[i] > sensor_values[i]):
                    min_sensor_values[i] = sensor_values[i]

        # record the min and max calibration values
        for i in range(0, self._numSensors):
            if(min_sensor_values[i] > self.calibratedMin[i]):
                self.calibratedMin[i] = min_sensor_values[i]
            if(max_sensor_values[i] < self.calibratedMax[i]):
                self.calibratedMax[i] = max_sensor_values[i]

    """
    Returns values calibrated to a value between 0 and 1000, where
    0 corresponds to the minimum value read by calibrate() and 1000
    corresponds to the maximum value.  Calibration values are
    stored separately for each sensor, so that differences in the
    sensors are accounted for automatically.
    """
    def readCalibrated(self):
        value = 0
        # read the needed values
        sensor_values = self.get_analog_read()

        for i in range(0, self._numSensors):

            #scales to min and max for a specific sensor;
            denominator = self.calibratedMax[i] - self.calibratedMin[i]

            if(denominator != 0):
                value = (sensor_values[i] - self.calibratedMin[i]) * 1000 / denominator

            if(value < 0):
                value = 0
            elif(value > 1000):
                value = 1000

            sensor_values[i] = value
        return sensor_values

    """
    Operates the same as read calibrated, but also returns an
    estimated position of the robot with respect to a line. The
    estimate is made using a weighted average of the sensor indices
    multiplied by 1000, so that a return value of 0 indicates that
    the line is directly below sensor 0, a return value of 1000
    indicates that the line is directly below sensor 1, 2000
    indicates that it's below sensor 2000, etc.  Intermediate
    values indicate that the line is between two sensors.  The
    formula is:

       0*value0 + 1000*value1 + 2000*value2 + ...
       --------------------------------------------
             value0  +  value1  +  value2 + ...

    By default, this function assumes a dark line (low values)
    surrounded by white (high values).  If your line is light on
    black, set the optional second argument white_line to false.  In
    this case, each sensor value will be replaced by (1000-value)
    before the averaging.
    """
    def readLine(self, white_line=0):
        # TODO: we probably don't need this
        # TODO: either here or a different class, steering should make sure the
        #   outside sensors are white and the center sensors are black,
        #   correcting as needed
        # TODO: if all white or all black, spin around and hope for the best
        sensor_values = self.readCalibrated()
        avg = 0
        sum = 0
        on_line = 0
        for i in range(0, self._numSensors):
            value = sensor_values[i]
            if(not white_line):
                value = 1000-value
            # keep track of whether we see the line at all
            if(value > 500):
                on_line = 1

            # only average in values that are above a noise threshold
            if(value > 50):
                avg += value * (i * 1000)  # this is for the weighted total,
                sum += value                 # this is for the denominator

        if(on_line != 1):
            # If it last read to the left of center, return 0.
            if(self.last_value < (self._numSensors - 1)*1000/2):
                # print("left")
                self.last_value = 0

            # If it last read to the right of center, return the max.
            else:
                # print("right")
                self.last_value = (self._numSensors - 1)*1000
        else:
            self.last_value = avg/sum

        return self.last_value, sensor_values


if __name__ == '__main__':
    """
    This example continuously returns measurements from the bottom IR sensors
    """
    TR = Bottom_IR()
    while True:
        print(f"Sensor values: {TR.get_analog_read()}")
        time.sleep(0.2)
