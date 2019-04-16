import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as py_mpl

class ARU_DICT:

    focal_length = 0.0
    marker_width = 0.0
    cam_center = [0, 0]

# creates a custom aruco dictionary (_aruco_dict) with n aruco markers in marker size s (_aruco_needed) with labels from the given list of labels
    def __init__(self, n=4, s=4, labels=["front", "left", "right", "back"]):
        if len(labels) != n:
            print("There are " + str(len(labels)) + " labels found for " + str(n) + " markers. Please insert one label for each marker.")
            return
        '''
        if s == 4:
            dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        elif s == 5:
            dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)
        elif s == 6:
            dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
        elif s == 7:
            dict = aruco.getPredefinedDictionary(aruco.DICT_7X7_50)
        else:
            print("no useful marker size entered! Choose marker size 4, 5, 6 or 7")
            return
        '''

        self._aruco_dict = aruco.custom_dictionary(n, s)
        self._aruco_needed = n
        self._aruco_labels = labels

        self.show_arucos()

# ----------------------------------------------------------------------------------------------------------------------
# shows all 4 relevant aruco markers in one window
    def show_arucos(self):

        frame = py_mpl.figure("Markers")
        subplot1 = np.ceil(self._aruco_needed / 2)

        for i in range(1, self._aruco_needed + 1):
            win = frame.add_subplot(2, subplot1, i)
            img = aruco.drawMarker(self._aruco_dict, (i-1), 500)
            py_mpl.imshow(img, cmap=mpl.cm.gray)
            win.axis("off")

        py_mpl.show()

# ----------------------------------------------------------------------------------------------------------------------
# detects markers from respective custom dictionary in an image or captured video and prints out the information
    def detect_aruco(self):

        # get camera image for comparison
        cap = cv.VideoCapture(1) # 0 webcam of laptop # 1 external cam

        #while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, self._aruco_dict, parameters=parameters)

        frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

        if ids is not None:
            for i in range(0, len(ids)):
                c = corners[i][0]
                marker_center = [c[:, 0].mean(), c[:, 1].mean()]

            print("recognized marker: " + str(ids[i]+1))
            marker = ids[i]+1
            distance = ARU_DICT.dist_to_marker(corners)
            angle = ARU_DICT.angle_to_marker(marker_center)

        # Display the resulting frame
        cv.imshow('video frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            return

        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()

        return marker, distance, angle

# ----------------------------------------------------------------------------------------------------------------------
# sets focal length for distance computation
    def set_focal_length(self, f):
        ARU_DICT.focal_length = f

# ----------------------------------------------------------------------------------------------------------------------
# sets width of the markers for distance computation
    def set_marker_width(self, w):
        ARU_DICT.marker_width = w

# ----------------------------------------------------------------------------------------------------------------------
# sets camera center from camera calibration martix for computation of the angle between marker and camera
    def set_cam_center(self, c):
        ARU_DICT.cam_center = [c[0], c[1]]

# ----------------------------------------------------------------------------------------------------------------------
# approximates the distance between a detected marker and the camera
    def dist_to_marker(corners):
        if ARU_DICT.focal_length != 0.0 and ARU_DICT.marker_width != 0.0:
            corner = corners[0][0]
            dist_x1 = corner[0][0] - corner[1][0]
            dist_y1 = corner[0][1] - corner[1][1]
            dist_x2 = corner[0][0] - corner[3][0]
            dist_y2 = corner[0][1] - corner[3][1]
            length_px_1 = np.linalg.norm([abs(dist_x1), abs(dist_y1)])
            length_px_2 = np.linalg.norm([abs(dist_x2), abs(dist_y2)])
            dist = (ARU_DICT.marker_width * ARU_DICT.focal_length) / max(length_px_1, length_px_2)
            print("The calculated distance marker - camera is:" + str(dist))
            return dist
        else:
            print("Sorry, focal length or marker width is not yet defined. Please use set_focal_length(f) or set_marker_length(w) to define these parameters")
            return -1

# ----------------------------------------------------------------------------------------------------------------------
# approximates the angle between the center of a detected marker and the camera (in radians and degrees)
    def angle_to_marker(m_center):

        # calculates length of opposite leg
        dist_x = float(m_center[0]) - float(ARU_DICT.cam_center[0])

        # calculates angle from center-vertical to shown marker (1. quadrant positive, 2. quadrant negative)
        alpha_rad = np.arctan(dist_x/ARU_DICT.focal_length)
        alpha_deg = np.degrees(alpha_rad)

        print("The angle between the marker's center and the camera is: ", alpha_deg)
        return alpha_deg
