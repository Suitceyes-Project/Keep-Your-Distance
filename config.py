import json

with open("config.json", "r") as json_file:
    data = json.load(json_file)

def is_log_enabled():
    return data["log_enabled"] == True

def get_marker_id(side):
    return data["markers"][side]

def get_actuators():
    return data["actuators"]

