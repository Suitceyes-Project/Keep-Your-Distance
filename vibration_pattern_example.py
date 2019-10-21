import VibrationController
import VibrationPatterns
import json
import vest_device
import time
import atexit

def exit_handler():
    device.mute()
    
atexit.register(exit_handler)

device = vest_device.UsbVestDevice("/dev/ttyACM0")
with open("vibration_patterns/heartbeat.json") as json_file:
    clip = json.load(json_file)
vest_controller = VibrationController.VestController(device)
player = VibrationPatterns.VibrationPatternPlayer(vest_controller)
player.play_clip(clip)
#player.speed = 1.25
deltaTime = 0
time_prev_frame = time.time()

while(True):
    current_time = time.time()
    deltaTime = current_time - time_prev_frame    
    player.update(deltaTime)
    time_prev_frame = current_time
    time.sleep(0.016)