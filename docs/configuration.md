---
layout: default
title: Configuration
nav_order: 3
---

# Configuration
The `config.json` file contains a list of settings. The following table gives a description of each parameter.

|Parameter|Value type|Description|
|---------|:----------:|-----------|
|actuatorRanges|array|Determines which motors get activated when the angle between the marker and wearer gets calculated. These motors determine the direction the wearer of the haptic wearable should move towards.|
|arucoDictionary|int|Which set of aruco markers get detected. View OpenCV documentation for further details. |
|button_gpio_pin|int|Which gpio pin on the Raspberry Pi is used to receive push button events.|
|calibrate|boolean|When the game starts, should the calibration process for the camera be started?|
|camCenter|array|A value that gets calculated during the calibration process. Value is taken from camera intrinsic matrix.|
|camMatrix|array|Camera intrinsic matrix. A value that gets calculated during the calibration process that is used for undistorting images captured by the fisheye camera.|
|camera|integer|Determines whether a webcam camera(=0) or external camera(=1) is used.|
|catchThiefAfterTime|float|The amount of time since the start of the game that has elapsed until the agent can catch the thief.|
|dangerTime|float|The maximum amount of time the agent can be in a danger zone -that is when the agent is too close or too far away from the suspect. Surpassing this time results in a game over. |
|distortCoeffs|array|Input vector of distortion coefficients. Calculated during camera calibration and used during the frame undistortion process.|
|focalLength|float|Focal length of the camera. Taken from camera intrinsic matrix calculated during calibration process.|
|frequencyClose|float|The frequency of the vibrations in seconds when the user's distance to the average position of all markers is smaller than `minDistance`.|
|frequencyFar|float|The frequency of the vibrations in seconds when the user's distance to the average position of all markers is larger than `maxDistance`.|
|frequencyOptimal|float|The frequency of the vibrations in seconds when the user's distance to the average position of all markers is greater than `minDistance` and smaller than `maxDistance`.|
|gameDuration|float|The maximum duration of the game is seconds.|
|logEnabled|boolean|When enabled the `LoggingSystem` writes detected markers and the calculated distances and angles into a csv file. |
|markerWidth|float|The width of the markers in metres.|
|markers|dictionary|Maps the id of a marker to a side ("left", "front", "right", "back") that corresponds to the side of the suspect. |
|maxDistance|float|The maximum distance the agent can be away from the suspect in metres before the agent is determined to be too far away and thus in "danger".|
|minDistance|float|The minimum distance the agent can be away from the suspect in metres before the agent is determined to be too close and thus in "danger".|
|shoulderMotors|array|The index of the motors used to convey the "stop" and "start" signal.|
|resolutionX|float|Resolution of the camera in the X dimension.|
|resolutionY|float|Resolution of the camera in the Y dimension.|
|targetLookAtThreshold|float|A threshold that determines when the suspect is considered to be facing the agent.|
|timeStep|float|The rate at which the game is updated in seconds.|
|useFisheye|boolean|Is a wide-angle camera being used? |
|ServerUri|string|The endpoint of the MQTT online broker.|
|Port|int|The port of the endpoint of the MQTT online broker.|
|CleanSession|bool|When the clean session flag is set to true, the client does not want a persistent session. If the client disconnects for any reason, all information and messages that are queued from a previous persistent session are lost. |
|Username|string|Username for MQTT authentication.|
|Password|string|Password for MQTT authentication.|
|SSL_TLS|boolean|Enables or disables SSL/TLS support.|
|Topics|array|An array of topics the MQTT broker should subscribe to when connecting.|