import json
import cv2.aruco as aruco

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
    motors = data["motors"]
    motorInterval = data["motorInterval"]

def get_marker_id(side):
    return data["markers"][side]