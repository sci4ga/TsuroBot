# Setup

## Needed

- Alphabot2 Pi kit
- A computer with VSCode installed
- Access to a router

## Install/setup the OS and connect

- Use the RapberryPi Imager to format a microSD card with Raspberry Pi OS Lite (64-bit) as given here: https://www.raspberrypi.com/documentation/computers/getting-started.html 
Include a username and password, Enable SSH, and provide credentials to your WiFi in the image configuration.

- Find the host IP of the Raspberry Pi from your router after you power up the system (first startup takes several minutes).
- Use Remote SSH VS Code extension to create an SSH session to tsuro@[host IP]

## Update packages

From your ssh session, run the following.

```bash
sudo apt-get update -y
sudo apt-get upgrade -y
```

## Install git, authenticate with git using HTTPS, and pull repo

```bash
sudo apt-get install git gh -y
gh auth login
```

Use these login options:

- Github.com
- HTTPS
- Authenticate with GitHub credentials
- Paste an authentication token

```gh
gh repo clone sci4ga/TsuroBot
```

## enable the camera and the I2C interface and SPI

```bash
sudo raspi-config
```

- Choose Interfacing Options -> SPI -> Yes  to enable the SPI interface
- Choose Interfacing Options -> I2C -> Yes.
- Select Interfacing Options -> Serial, disable shell access, and enable the hardware serial port
- Finish
- Reboot

Create new ssh session with tsuro@[host IP]

## Install pip and pip install requirements

```bash
sudo apt install python3-pip -y
cd ./TsuroBot
mkdir logs
cd ./src
pip install --upgrade pip --break-system-packages
sudo pip install -r requirements.txt --break-system-packages
```

## Run the app

```bash
sudo python app.py
```

## NOTES

When re-imaging your rpi, you may need to clear .ssh/known_hosts if you're going to ssh back into the same IP

~ 2.5GB free space will be needed for install.
~1.5GB extra needed for 'opencv_contrib' extra modules

Clear space like this:
https://www.raspberrypi-spy.co.uk/2018/03/free-space-raspberry-pi-sd-card/

## ISSUES

We're unable to update Flask and Werkzeug to the latest versions because flask 2.3.0 depends on Werkzeug>=2.3.0 and connexion 2.14.2 depends on werkzeug<2.3 and >=1.0 This project needs to migrate from connexion 2.14.2 to 3.x.x to allow updates to Flask and Werkzeug.

When app.py is run, api.py reloads and therefore throws:

>RuntimeError: A PWM object already exists for this GPIO channel

The reload of api.py is likely caused by:

>ERROR 2025-01-24 09:59:14,576 connexion.apis.abstract abstract.py - Failed to add operation for GET /api/ack

From 2020: swagger UI cache does not clear between executed calls, returning old data
