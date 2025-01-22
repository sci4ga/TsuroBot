# RaspberryPi setup

Use the RapberryPi Imager to format a microSD card with Raspberry Pi OS Lite (64-bit) as given here: https://www.raspberrypi.com/documentation/computers/getting-started.html

Include a username and password, Enable SSH, and provide credentials to your WiFi in the image configuration.

Find the host IP of the Raspberry Pi from your router after you power up the system.

Use Remote SSH VS Code extension to create an SSH sesison to tsuro@[host IP]

Update packages:
sudo apt-get update
sudo apt-get upgrade

Install git:
sudo apt-get install git
sudo apt-get install github-cli

Authenticate with git using HTTPS:
gh auth login

Pull this code and create/activate a virtual environment:
gh repo clone sci4ga/TsuroBot
cd ./TsuroBot
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
apt install libcamera-dev

# enable the camera and the I2C interface and SPI
sudo raspi-config

pip install -r requirements.txt

# RobotTsuro
# Required packages:

# OpenCV...
# Easy setup...
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install scons
sudo apt-get install swig
sudo pip3 install opencv-contrib-python



# NOTES

when running sudo (needed for LED), use the path to python in the venv. e.g.:
sudo /home/tsuro/TsuroBot/venv/bin/python ./led.py

~ 2.5GB free space will be needed for install.
~1.5GB extra needed for 'opencv_contrib' extra modules

Clear space like this:
https://www.raspberrypi-spy.co.uk/2018/03/free-space-raspberry-pi-sd-card/

ISSUES:
swagger UI cache does not clear between executed calls, returning old data