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
from MarkerTransformationSystem import MarkerTransformationSystem

# create services
marker_service = MarkerService()

game_duration = cfg.gameDuration
delta = 0.0
sleep_time = cfg.timeStep
starting_time = time.time()
game_running = True
time_prev_frame = time.time()

# Initialize the bluetooth connection to the vest
vest = VestDevice(cfg.device)

# make sure camera is released
with CameraService() as camera_service, \
     LoggingSystem(marker_service) as logging_system, \
     CameraRenderingSystem(camera_service) as camera_rendering_system:

    # create systems
    marker_detection_system = MarkerDetectionSystem(marker_service, camera_service)
    vibration_navigation_system = VibrationNavigationSystem(vest, marker_service)
    marker_transformation_system = MarkerTransformationSystem(marker_service, camera_service)
    
    try:        
        print("Game running...")
        # GAME LOOP
        while (game_running):
            
            # calculated time passed
            current_time = time.time()
            delta += current_time - time_prev_frame
            time_prev_frame = current_time

            # detect marker
            if(delta < sleep_time):
                continue
            
            marker_detection_system.update()
            marker_transformation_system.update()
            camera_rendering_system.update()
            vibration_navigation_system.update()

            # reset timer
            delta = 0.0

            # GAME END
            time_played = current_time - starting_time
            if time_played > game_duration:
                time_played = 0.0
                delta = 0.0
                game_running = False
                vest.mute()
    finally:
        print("Closed application")
        vest.mute()