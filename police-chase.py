#import arucreate
import camera_calibration
import time
import config as cfg
from MarkerService import MarkerService
from vest_device import VestDevice
from actuator_controller import ActuatorController
from CameraService import CameraService
from MarkerDetectionSystem import MarkerDetectionSystem
from CameraRenderingSystem import CameraRenderingSystem

# INITIATE GAME
# calibrates new camera with NO existing images, and determines "focal_length" and "cam_center"
#focal_length, cam_center = camera_calibration.calibrate()

# create services
marker_service = MarkerService()


game_duration = cfg.gameDuration
delta = 0.0
sleep_time = cfg.timeStep
starting_time = time.time()
game_running = True

# Initialize the bluetooth connection to the vest
vest = VestDevice("10:d0:7a:16:b8:d7")

# make sure camera is released
with CameraService() as camera_service:

    # create systems
    marker_detection_system = MarkerDetectionSystem(marker_service, camera_service)
    camera_rendering_system = CameraRenderingSystem(camera_service)
    # Create controller for controlling vest logic
    #actuator_controller = ActuatorController(vest, police_chase_dic)
    try:
        # GAME LOOP
        while (game_running):

            delta += 0.01

            # detect marker
            if(delta > sleep_time):
                # marker: int 1 - 4, dist: float in cm, angle: float in degree
                #marker, dist, angle = police_chase_dic.detect_aruco()
                marker_detection_system.update()
                camera_rendering_system.update()
                # check messages to actuators (stop, turn or just continue)
    ##            if marker == 1:
    ##                print("Marker Nr. 1: front is recognized. STOP!")
    ##            elif marker == 2:
    ##                print("Marker Nr. 2: left is recognized. Turn is needed")
    ##                print("Tell actuator angle to the left")
    ##            elif marker == 3:
    ##                print("Marker Nr. 3: right is recognized. Turn is needed")
    ##                print("Tell actuator angle to the right")
    ##            elif marker == 4:
    ##                #vest.setPin(0,255)
    ##                print("Marker Nr. 4: back is recognized. Just follow")
    ##            elif marker > 4:
    ##                print("Marker has no valuable id! Check out information from ARU_DICT.detect_aruco")

                #if dist != -1.0 and dist != 0.0:
                #    if dist < 50:
                #        print("Tell actuator detective is too clos to target")
                #    elif dist > 150:
                #        print("Tell actuator detective is too far away from target")
                    
                #actuator_controller.update(angle)

                # reset timer
                delta = 0.0

                print("Game running...")

                # GAME END
            time_played = time.time() - starting_time
            if time_played > game_duration:
                time_played = 0.0
                delta = 0.0
                game_running = False
                #police_chase_dic.close_aruco_detection()
                vest.mute()
    finally:
        vest.mute()
        camera_rendering_system.dispose()


