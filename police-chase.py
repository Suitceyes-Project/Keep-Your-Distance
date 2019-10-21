import camera_calibration
import time
import config as cfg
import vest_device
from MarkerService import MarkerService
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

print("entered police-chase script", flush=True)

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

    # Initialize connection to the vest
    if cfg.deviceMode == 0:
        vest = vest_device.UsbVestDevice(cfg.usbPort)
    else:
        vest = vest_device.BleVestDevice(cfg.device)
    
    camera_service.start()
    
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
        print("Game running...", flush=True)
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
                print("Game is over.", flush=True)
                vest.mute()

    finally:
        print("Closed application", flush=True)
        vest.mute()
        camera_service.stop()
