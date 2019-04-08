# police-chase

## Setup

1. install python
2. install via pip
	- numpy
	- opencv-python
	- opencv.aruco
	- opencv-contrib-python
	- matplotlib
    - matplotlib.pyplot
    - imageio
    - PIL.Image
    - os
    - os.path

3. run / build the app:
    - initiate game:
      * use "camera_calibration.fast_calibrate()", if calibration images with respective cam are already saved in "_calibration" folder
      * use "camera_calibration.calibrate()", if calibration needs to be done completely (i.e., new camera, no images saved in "_calibration" folder)
      * choose your own game_duration (length of pursuit)

    - game loop
