# RaspberryPi setup

Use the RapberryPi Imager to format a microSD card with Raspberry Pi OS Lite (64-bit) as given here: https://www.raspberrypi.com/documentation/computers/getting-started.html

Include a username and password, Enable SSH, and provide credentials to your WiFi in the image configuration.

Find the host IP of the Raspberry Pi from your router after you power up the system.

Use Remote SSH VS Code extension to create an SSH sesison to tsuro@[host IP]

# Update packages:
sudo apt-get update -y
sudo apt-get upgrade -y

# Install git:
sudo apt-get install git -y
sudo apt-get install gh -y

# Authenticate with git using HTTPS:
gh auth login

# enable the camera and the I2C interface and SPI
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes  to enable the SPI interface
Choose Interfacing Options -> I2C -> Yes.
Select Interfacing Options -> Serial, disable shell access, and enable the hardware serial port
*Choose Enable Camera -> Yes

sudo reboot
# Required packages:

#sudo apt install libcamera-dev -y
#sudo apt install python3-libcamera -y
#sudo apt install libcap-dev -y
#sudo apt install python3-pip -y
sudo apt install python3-Flask -y
sudo apt install python3-rpi.gpio -y

# Pull this code and create/activate a virtual environment:

gh repo clone sci4ga/TsuroBot
cd ./TsuroBot
#python -m venv --system-site-packages venv
#source venv/bin/activate
pip install --upgrade pip
#sudo apt install python3-prctl -y
sudo pip install -r requirements.txt --break-system-packages
#WARNING: The script connexion is installed in '/home/tsuro/.local/bin' which is not on PATH.
# RobotTsuro

# OpenCV...
# Easy setup...
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install scons
sudo apt-get install swig
pip install opencv-contrib-python



# NOTES

when running sudo (needed for LED) and in a venv, use the path to python in the venv. e.g.:
sudo /home/tsuro/TsuroBot/venv/bin/python ./led.py

After re-imaging your rpi, you may need to clear .ssh/known_hosts if you're going to ssh back into the same IP

~ 2.5GB free space will be needed for install.
~1.5GB extra needed for 'opencv_contrib' extra modules

Clear space like this:
https://www.raspberrypi-spy.co.uk/2018/03/free-space-raspberry-pi-sd-card/

ISSUES:
swagger UI cache does not clear between executed calls, returning old data