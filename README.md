# police-chase

## Setup

1. install python
2. install via pip3
	- numpy
	- opencv-python
	- opencv.aruco
	- opencv-contrib-python
	- matplotlib
    - matplotlib.pyplot
    - PIL.Image
    - os
    - os.path
    - time
    - csv
    - bluepy ("https://github.com/IanHarvey/bluepy")

3. run / build the app:
    - if you want to use webcam of laptop (NO external device)
      * change argument 1 to 0 in:
            - camera_calibration.62
            - arucreate.58

    - initiate game:
      * use "camera_calibration.fast_calibrate()", if calibration images with respective cam are already saved in "_calibration" folder (Intel RealSense)
      * use "camera_calibration.calibrate()", if calibration needs to be done completely (i.e., new camera, no images saved in "_calibration" folder)
      * change value set_marker_width, if you choose a different charuco board (width of printed aruco markers on chessboard)
      * choose your own game_duration (length of pursuit)
      * choose your own sleep_time: waiting intervall until next aruco marker detection
      
## Raspberry Pi
Since we're using a virtual environment you have to enter the following commands before running any python files, otherwise it won't find the required modules:
~~~
source ~/.profile
workon cv
~~~

You should then see:
~~~
(cv) pi@raspberrypi: ~/
~~~

For bluepy to work correctly the following commands maybe also have to be executed:
~~~
sudo hciconfig hci0 down
sudo hciconfig hci0 up
~~~


