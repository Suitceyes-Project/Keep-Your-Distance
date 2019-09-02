import cv2 as cv
import cv2.aruco as aruco
import config as cfg
import numpy as np
import fisheye_calibration

class MarkerDetectionSystem:

    parameters = aruco.DetectorParameters_create()
    
    def __init__(self, marker_service, camera_service):
        self._marker_service = marker_service
        self._camera_service = camera_service
        self._aruco_dict = cfg.arucoDictionary
    
    def update(self):
        marker = 0
        distance = 0.0
        angle = 180.00

        # Clear all markers (maybe this should not be done)
        self._marker_service.clear()

        # Capture frame-by-frame
        ret, frame = self._camera_service.read()       

        # If nothing was returned, just exit
        if ret == False:
            return     

        # Convert to grayscale image
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self._aruco_dict, parameters=self.parameters)       
        
        if ids is not None:
            # update corners
            self._marker_service.set_corners_array(corners)
            
            for i in range(0, len(ids)):
                # Get corner
                c = corners[i][0]
                
                # Calculate marker centerq
                marker_center = [c[:, 0].mean(), c[:, 1].mean()]
                
                # Calculate distance to camera
                distance = self._dist_to_marker(c)
                
                # Calculate the angle to camera center (uv coordinates are used here)
                angle = self._angle_to_marker(marker_center)               
                
                # Update markers database
                self._marker_service.update_marker(ids[i][0], c, marker_center, distance, angle)           
                 

    def _dist_to_marker(self, corner):
        marker_width = cfg.markerWidth
        focal_length = self._camera_service.get_focal_length()
        if focal_length != 0.0 and marker_width != 0.0:
            dist_x1 = corner[0][0] - corner[1][0]
            dist_y1 = corner[0][1] - corner[1][1]
            dist_x2 = corner[0][0] - corner[3][0]
            dist_y2 = corner[0][1] - corner[3][1]
            length_px_1 = np.linalg.norm([abs(dist_x1), abs(dist_y1)])
            length_px_2 = np.linalg.norm([abs(dist_x2), abs(dist_y2)])
            dist = (marker_width * focal_length) / max(length_px_1, length_px_2)
            #print("The calculated distance marker - camera is:" + str(dist))
            return dist
        else:
            print("Sorry, focal length or marker width is not yet defined. Please use set_focal_length(f) or set_marker_length(w) to define these parameters")
            return -1.0

# ----------------------------------------------------------------------------------------------------------------------
# approximates the angle between the center of a detected marker and the camera (in radians and degrees)
    def _angle_to_marker(self, m_center):

        # get camera center and focal length
        cam_center = self._camera_service.get_camera_center()
        focal_length = self._camera_service.get_focal_length()
        
        # calculates length of opposite leg
        dist_x = float(m_center[0]) - float(cam_center[0])

        # calculates angle from center-vertical to shown marker (1. quadrant positive, 2. quadrant negative)
        alpha_rad = np.arctan(dist_x/focal_length)
        alpha_deg = np.degrees(alpha_rad)

        #print("The angle between the marker's center and the camera is: ", alpha_deg)
        return alpha_deg
