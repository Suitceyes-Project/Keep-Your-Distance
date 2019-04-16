import arucreate
import camera_calibration
import time

# INITIATE GAME
# calibrates new camera with NO existing images, and determines "focal_length" and "cam_center"
focal_length, cam_center = camera_calibration.calibrate()
# _________________________________________ CHECK AGAIN ________________________________________________________________

# calibrates known camera with existing images, and determines "focal_length" and "cam_center"
#focal_length, cam_center = camera_calibration.fast_calibrate()

# initiate aruco library with camera parameters
police_chase_dic = arucreate.ARU_DICT()
police_chase_dic.set_marker_width(0.08) # in meter
police_chase_dic.set_focal_length(focal_length)
police_chase_dic.set_cam_center(cam_center)

game_duration = 300 # 5 minutes
delta = 0.0
sleep_time = 0.5
starting_time = time.time()
game_running = True

# GAME LOOP
while (game_running):

    delta += 0.01

    # detect marker
    if(delta > sleep_time):
        # marker: int 1 - 4, dist: float in cm, angle: float in degree
        marker, dist, angle = police_chase_dic.detect_aruco()

        # check messages to actuators (stop, turn or just continue)
        if marker == 1:
            print("Marker Nr. 1: front is recognized. STOP!")
        elif marker == 2:
            print("Marker Nr. 2: left is recognized. Turn is needed")
            print("Tell actuator angle to the left")
        elif marker == 3:
            print("Marker Nr. 3: right is recognized. Turn is needed")
            print("Tell actuator angle to the right")
        elif marker == 4:
            print("Marker Nr. 4: back is recognized. Just follow")
        else:
            print("Marker has no valuable id! Check out information from ARU_DICT.detect_aruco")

        if dist != -1:
            if dist < 50:
                print("Tell actuator detective is too clos to target")
            elif dist > 150:
                print("Tell actuator detective is too far away from target")

        # reset timer
        delta = 0.0

    # GAME END
    time_played = time.time() - starting_time
    if time_played > game_duration:
        time_played = 0.0
        delta = 0.0
        game_running = False


