import json
import cv2.aruco as aruco
import numpy as np

with open("config.json", "r") as json_file:
    data = json.load(json_file)
    arucoDictionary = aruco.Dictionary_get(data["arucoDictionary"])
    timeStep = data["timeStep"]
    isLogEnabled = bool(data["logEnabled"])
    markerWidth = data["markerWidth"]
    camera = int(data["camera"])
    actuators = data["actuators"]
    gameDuration = data["gameDuration"]
    device = data["device"]
    minDistance = data["minDistance"]
    maxDistance = data["maxDistance"]
    frequencyClose = data["frequencyClose"]
    frequencyOptimal = data["frequencyOptimal"]
    frequencyFar = data["frequencyFar"]
    actuatorRanges = data["actuatorRanges"]
    targetLookAtThreshold = data["targetLookAtThreshold"]
    dangerTime = data["dangerTime"]
    shoulderMotors = data["shoulderMotors"]
    motorInterval = data["motorInterval"]
    resolutionX = data["resolutionX"]
    resolutionY = data["resolutionY"]
    distortCoeffs = np.array(data["distortCoeffs"])
    focalLength = data["focalLength"]
    camMatrix = np.array(data["camMatrix"])
    camCenter = data["camCenter"]
    calibrate = data["calibrate"]
    useFisheye = data["useFisheye"]
    deviceMode = int(data["deviceMode"])
    usbPort = data["usbPort"]
    catchThiefAfterTime = data["catchThiefAfterTime"]
    buttonGpioPort= int(data["button_gpio_pin"])
    

def get_marker_id(side):
    return data["markers"][side]