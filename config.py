import json
import cv2.aruco as aruco

with open("config.json", "r") as json_file:
    data = json.load(json_file)
    arucoDictionary = aruco.Dictionary_get(data["arucoDictionary"])
    timeStep = data["timeStep"]
    isLogEnabled = bool(data["log_enabled"])
    markerWidth = data["markerWidth"]
    camera = int(data["camera"])
    actuators = data["actuators"]
    gameDuration = data["gameDuration"]

def get_marker_id(side):
    return data["markers"][side]