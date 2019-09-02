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
from ProximityConditionSystem import ProximityConditionSystem
from Game import Game
from TargetLookAtSystem import TargetLookAtSystem
from Feedback import FeedbackSystem

# create services
marker_service = MarkerService()

delta = 0.0
sleep_time = cfg.timeStep
time_prev_frame = time.time()
game = Game()



# make sure camera is released
with CameraService() as camera_service, \
     LoggingSystem(marker_service) as logging_system, \
     CameraRenderingSystem(camera_service) as camera_rendering_system:

    # Initialize the bluetooth connection to the vest
    vest = VestDevice(cfg.device)
    
    # create systems
    marker_detection_system = MarkerDetectionSystem(marker_service, camera_service)
    vibration_navigation_system = VibrationNavigationSystem(vest, marker_service)
    marker_transformation_system = MarkerTransformationSystem(marker_service, camera_service)
    proximity_condition_system = ProximityConditionSystem(game, marker_service)
    target_look_at_system = TargetLookAtSystem(marker_service)
    feedback_system = FeedbackSystem(vest)
    
    # start the game
    game.start()
    
    try:        
        print("Game running...")
        # GAME LOOP
        while (game.is_running):
            
            # calculated time passed
            current_time = time.time()
            delta += current_time - time_prev_frame
            time_prev_frame = current_time

            # wait for next frame
            if(delta < sleep_time):
                continue
            
            # update systems
            game.update(delta)
            marker_detection_system.update()
            marker_transformation_system.update()
            camera_rendering_system.update()
            vibration_navigation_system.update()
            target_look_at_system.update()
            feedback_system.update()
            #proximity_condition_system.update(delta)
            
            # reset timer
            delta = 0.0

            # GAME END
            if game.is_over:
                print("Game is over.")
                vest.mute()

    finally:
        print("Closed application")
        vest.mute()