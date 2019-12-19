"""
Before we install the Raspberry Pi library for the WS2812 LEDs, some preparations have to be made:

The package sources are updated:
sudo apt-get update
We install the required packages (confirm with Y):
sudo apt-get install gcc make build-essential python-dev git scons swig
The audio output must be deactivated. For this we edit the file
sudo nano /etc/modprobe.d/snd-blacklist.conf
Here we add the following line:

blacklist snd_bcm2835
Then the file is saved by pressing CTRL + O and CTRL + X closes the editor.

We also need to edit the configuration file:
sudo nano /boot/config.txt
Below are lines with the following content (with Ctrl + W you can search):

# Enable audio (loads snd_bcm2835)
dtparam=audio=on
This bottom line is commented out with a hashtag # at the beginning of the line: #dtparam=audio=on

We restart the system
sudo reboot
"""
