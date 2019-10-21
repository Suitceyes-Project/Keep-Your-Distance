import VibrationController
import VibrationPatterns
import json
import vest_device
import time

device = vest_device.UsbVestDevice("/dev/ttyACM0")
clip = json.load("vibration_patterns/heartbeat.json")
vest_controller = VibrationController.VestController(device)
player = VibrationPatterns.VibrationPatternPlayer(vest_controller)
player.play_clip(clip)

deltaTime = 0
time_prev_frame = time.time()

while(True):
    current_time = time.time()
    deltaTime = current_time - time_prev_frame
    player.update(deltaTime)