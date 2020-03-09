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
from StateMachine import StateMachine
import States
from VibrationController import VestController
import CatchThief
from VibrationPatterns import VibrationPatternPlayer
from ProgressRequestSystem import ProgressRequestSystem
import listeners

print("entered police-chase script", flush=True)

# create services
marker_service = MarkerService()
message_interval = 5
last_message = time.time()
delta = 0.0
sleep_time = cfg.timeStep
time_prev_frame = time.time()
game = Game()
real_time_message_bus = listeners.RealtimeMessageBus()

# make sure camera is released
with CameraService() as camera_service, \
     LoggingSystem(marker_service) as logging_system, \
     CameraRenderingSystem(camera_service) as camera_rendering_system:     

     #vest_device.I2CVestDevice(0x41, 0x40) as vest:
    vest = vest_device.DummyVestDevice()
    camera_service.start()
    
    # create systems
    marker_detection_system = MarkerDetectionSystem(marker_service, camera_service)
    #vibration_navigation_system = VibrationNavigationSystem(vest, marker_service)
    marker_transformation_system = MarkerTransformationSystem(marker_service, camera_service)
    proximity_condition_system = ProximityConditionSystem(game, marker_service)
    target_look_at_system = TargetLookAtSystem(marker_service)
    feedback_system = FeedbackSystem(vest)
    vest_controller = VestController(vest)
    vibration_pattern_player = VibrationPatternPlayer(vest_controller)
    catch_thief_condition = CatchThief.CatchThiefCondition()    
    
    # create states
    state_machine = StateMachine()    
    catch_thief_event_handler = CatchThief.CatchThiefEventHandler(state_machine)
    navigation = States.NavigationState(vest_controller, marker_service)
    catch_thief = States.CatchThiefState(vest_controller, vibration_pattern_player, state_machine)    
    request_progress = States.RequestProgressState(vest_controller, vibration_pattern_player, state_machine, game)
    state_machine.add_state("navigation", navigation)
    state_machine.add_state("catch-thief", catch_thief)
    state_machine.add_state("request-progress", request_progress)
    state_machine.change_to("navigation")
    
    catch_thief_listener = listeners.CatchThiefMessageListener(state_machine, real_time_message_bus)
    set_progress_listener = listeners.SetProgressMessageListener(real_time_message_bus, game)
    progress_request_system = ProgressRequestSystem(state_machine)
    
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
            
            # this just prints a message every x seconds
            if current_time - last_message > message_interval:
                print("Game running", flush=True)
                last_message = current_time
            
            # update systems
            game.update(delta)
            progress_request_system.update(delta)
            marker_detection_system.update()
            marker_transformation_system.update()
            camera_rendering_system.update()
            #catch_thief_condition.update(delta)
            state_machine.update(delta)
            #vibration_navigation_system.update()
            target_look_at_system.update()
            feedback_system.update()
            proximity_condition_system.update(delta)
            
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
