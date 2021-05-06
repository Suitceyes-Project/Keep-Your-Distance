---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started
## Python Modules
The game is written in Python and requires a number of Python packages which can be installed via the `pip` command in a terminal of your choosing:
* [numpy](https://pypi.org/project/numpy/)
* [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [adafruit_pca9685](https://pypi.org/project/adafruit-circuitpython-pca9685/)
* [board](https://pypi.org/project/board/)
* [websocket-client](https://pypi.org/project/websocket-client/)
* OpenCV (v3.4.13): Python Binding is required. Follow [this](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) guide on how to build OpenCV Python binding for Raspberry Pi
* [picamera](https://pypi.org/project/picamera/): should be installed via `pip install picamera[array]` to be utilized with OpenCV. 
* [blinker](https://pypi.org/project/blinker/)
* [PyCmdMessenger](https://pypi.org/project/PyCmdMessenger/)
* [bluepy](https://pypi.org/project/bluepy/)

## Raspberry Pi
Raspberry Pi OS must be configured in order for the used interfaces to work correctly. To do this, open a terminal and enter:

`sudo raspi-config`

Next use the arrow keys to navigate to Interfacing Options and hit Enter. Here, the following two interfaces must be enabled:
1. I2C
2. Camera

## Usage
* If using a virtual Python environment, make sure to switch to that beforehand. Useful commands are:

```
source ~/.profile
workon your_environment
```
* To run in debug mode, use the following command:
```
python police-chase.py
```` 
* To run in a headless mode, use the following command:
```
python police-chase.py headless
```