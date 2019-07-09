import camera_calibration
import time
import config as cfg
from MarkerService import MarkerService
from vest_device import VestDevice
from actuator_controller import ActuatorController
from CameraService import CameraService
from MarkerDetectionSystem import MarkerDetectionSystem
from CameraRenderingSystem import CameraRenderingSystem
from LoggingSystem import LoggingSystem
from VibrationNavigationSystem import VibrationNavigationSystem

# create services
marker_service = MarkerService()

game_duration = cfg.gameDuration
delta = 0.0
sleep_time = cfg.timeStep
starting_time = time.time()
game_running = True

# Initialize the bluetooth connection to the vest
vest = VestDevice(cfg.device)

# make sure camera is released
with CameraService() as camera_service, \
     LoggingSystem(marker_service) as logging_system, \
     CameraRenderingSystem(camera_service) as camera_rendering_system:

    # create systems
    marker_detection_system = MarkerDetectionSystem(marker_service, camera_service)
    vibration_navigation_system = VibrationNavigationSystem(vest, marker_service)

    try:        
        print("Game running...")
        # GAME LOOP
        while (game_running):

            delta += 0.01

            # detect marker
            if(delta > sleep_time):
                marker_detection_system.update()
                camera_rendering_system.update()
                vibration_navigation_system.update()
                logging_system.update()

                #if dist != -1.0 and dist != 0.0:
                #    if dist < 50:
                #        print("Tell actuator detective is too clos to target")
                #    elif dist > 150:
                #        print("Tell actuator detective is too far away from target")
                    
                #actuator_controller.update(angle)

                # reset timer
                delta = 0.0


                # GAME END
            time_played = time.time() - starting_time
            if time_played > game_duration:
                time_played = 0.0
                delta = 0.0
                game_running = False
                vest.mute()
    finally:
        vest.mute()