# Keep Your Distance
Keep Your Distance (previously Police Chase) was a game designed over the course of the [Suitceyes](http://www.suitceyes.eu) research project, funded by the EU, with the aim of teaching deafblind individuals to navigate with the HIPI (Haptic Intelligent Personalized Interface) safely. The game involves two players where one assumes the role of a secret agent (player wearing the HIPI) and the other acts as a suspect. The goal of the secret agent is to keep within an optimal distance to the suspect. While getting too close to the suspect will expose the secret agent's cover, staying too far from the suspect will enable him/her to escape. At the end of the game, we provide a cue that the agent can *catch* the suspect to win the game.

The application uses a wide-angle camera to track ArUco markers which represent the suspect. Through computer vision algorithms we are able to estimate the distance and the angle to the marker. Depending on these two parameters we can provide different cues to the wearer of the HIPI:
* Varying frequency levels of vibration (quicker pulses mean the agent is getting too close to the suspect, slower pulses mean the agent is too far from the suspect)
* Local vibrations on the tactile belt of the HIPI: These indicate the direction the wearer must move towards in order to follow the suspect. 

We use a Wizard of Oz style application to provide signals to the user, e.g., when the agent can *catch* the suspect.
This application can be found [here](https://github.com/AffectiveCognitiveInstitute/police-chase-unity-app).

## Prequisites
### Python Modules
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

### Raspberry Pi
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

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
James Gay - james.gay@hs-offenburg.de
