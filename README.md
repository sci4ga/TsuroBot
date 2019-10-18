# RobotTsuro
# Required packages:

sudo apt-get install rpi.gpio

# OpenCV...
# Easy setup...
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev

sudo pip3 install opencv-contrib-python

# enable the camera
sudo raspi-config

# Hard setup...
# Required packages:

sudo apt-get install rpi.gpio
sudo apt-get install ffmpeg
sudo apt-get install python3-opencv
sudo apt-get install libjpeg8-dev

# TODO: add explanatory information
To install opencv on raspberry pi, see:
https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/

~ 2.5GB free space will be needed for install.
~1.5GB extra needed for 'opencv_contrib' extra modules

Clear space like this:
https://www.raspberrypi-spy.co.uk/2018/03/free-space-raspberry-pi-sd-card/

These system packages may be needed:

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran

