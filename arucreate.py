import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as py_mpl
import imageio

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
# find aruco marker i with its label and displays it
    def lookup_aruco_nr(self, i):
        if i == 1:
            frame = py_mpl.figure("Aruco Nr 1 -" + self._aruco_labels[i-1])
        elif i == 2:
            frame = py_mpl.figure("Aruco Nr 2 -" + self._aruco_labels[i-1])
        elif i == 3:
            frame = py_mpl.figure("Aruco Nr 3 -" + self._aruco_labels[i-1])
        elif i == 4:
            frame = py_mpl.figure("Aruco Nr 4 -" + self._aruco_labels[i-1])
        else:
            print("This marker is unknown for this application. Known marker ids: \n id_1: front \n id_2: left \n id_3: right \n id_4: back")
            return

        img = aruco.drawMarker(self._aruco_dict, (i - 1), 500)
        py_mpl.imshow(img, cmap=mpl.cm.gray)
        py_mpl.axis("off")
        py_mpl.show()

# ----------------------------------------------------------------------------------------------------------------------
# detects markers from respective custom dictionary in an image or captured video and prints out the information
    def detect_aruco(self):
        # get img for comparison
        #checkimg = cv.imread("_markers/marker_advanced.jpg")

        # get camera image for comparison
        cap = cv.VideoCapture(1) # 0 webcam of laptop

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, self._aruco_dict, parameters=parameters)

            frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

            if ids is not None:
                py_mpl.figure()
                py_mpl.imshow(frame_markers, origin = "upper")
                for i in range(0, len(ids)):
                    c = corners[i][0]
                    marker_center = [[c[:, 0].mean()], [c[:, 1].mean()]]
                    py_mpl.plot(marker_center.x, marker_center.y, "+", label="Marker = {0}".format(ids[i]+1))
                    #py_mpl.plot([c[:, 0].mean()], [c[:, 1].mean()], "+", label="Marker = {0}".format(ids[i]+1))
                py_mpl.legend()
                py_mpl.axis("off")

                # print/show image with information about recognized markers
                #py_mpl.show()
                print("recognized marker: " + str(ids[i]+1))

                ARU_DICT.dist_to_marker(corners)
                ARU_DICT.angle_to_marker(marker_center)

            # Display the resulting frame
            cv.imshow('video frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()

# ----------------------------------------------------------------------------------------------------------------------
# saves all needed (_aruco_needed) markers from custom dictionary (_aruco_dict) to the folder _markers
    def save_aruco_images(self):

        if isinstance(self._aruco_needed, int):
            for i in range(0, self._aruco_needed):
                img = aruco.drawMarker(self._aruco_dict, i, 500)
                imageio.imwrite("_markers/marker_"+str(i+1)+".jpg", img)
                print("Marker", str(i+1), "saved.")

# ----------------------------------------------------------------------------------------------------------------------
# sets focal length for distance computation
    def set_focal_length(self, f):
        ARU_DICT.focal_length = f

# ----------------------------------------------------------------------------------------------------------------------
# sets width of the markers for distance computation
    def set_marker_width(self, w=0.08):
        ARU_DICT.marker_width = w

# ----------------------------------------------------------------------------------------------------------------------
# sets camera center from camera calibration martix for computation of the angle between marker and camera
    def set_cam_center(self, cx, cy):
        ARU_DICT.cam_center = [cx, cy]

# ----------------------------------------------------------------------------------------------------------------------
# approximates the distance between a detected marker and the camera
    def dist_to_marker(self, corners):
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
        else:
            print("Sorry, focal length or marker width is not yet defined. Please use set_focal_length(f) or set_marker_length(w) to define these parameters")

# ----------------------------------------------------------------------------------------------------------------------
# approximates the angle between the center of a detected marker and the camera (in radians and degrees)
    def angle_to_marker(self, m_center):
        # brings points on the same line, to only calculate the horizontal angle
        ARU_DICT.cam_center = [ARU_DICT.cam_center.x, m_center.y]

        dist_x = ARU_DICT.cam_center.x - m_center.x
        dist_y = ARU_DICT.cam_center.y - m_center.y

        angle_rad = np.arctan2(dist_x, dist_y)
        angle_deg = np.rad2deg(angle_rad)

        print("The angle between the marker's center and the camera is: ", angle_deg)
