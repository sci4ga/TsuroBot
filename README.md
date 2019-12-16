# RobotTsuro
# Required packages:

sudo apt-get install rpi.gpio

# OpenCV...
# Easy setup...
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install scons
sudo apt-get install swig
sudo pip3 install opencv-contrib-python

# enable the camera and the I2C interface and SPI
sudo raspi-config

# NOTES

~ 2.5GB free space will be needed for install.
~1.5GB extra needed for 'opencv_contrib' extra modules

Clear space like this:
https://www.raspberrypi-spy.co.uk/2018/03/free-space-raspberry-pi-sd-card/

ISSUES:
swagger UI cache does not clear between executed calls, returning old data