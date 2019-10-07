import config as cfg
import cv2.aruco as aruco
import cv2 as cv
import numpy as np
import math

class MarkerTransformationSystem:
    
    def __init__(self, marker_service, camera_service):
        self._marker_service = marker_service
        self._camera_service = camera_service
        
    
    def update(self):
        markers = self._marker_service.get_markers()
        frame = self._camera_service.get_current_frame()
        
        if markers is None:
            return
        
        # get values for pose estimation
        cam_matrix = self._camera_service.get_matrix()
        dist_coeffs = self._camera_service.get_distortion_coefficients()
        marker_length = float(cfg.markerWidth);
        corners = self._marker_service.get_corners_array()
        
        # get an array of rotation vectors and translation vector
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_length, cam_matrix, dist_coeffs)
        
        for i in range(0, len(markers)):
            # Convert rotation vector to rotation matrix
            dst, _ = cv.Rodrigues(rvecs[i])
            
            # Set the translation vector
            self._marker_service.set_translation(markers[i], tvecs[i][0])
            
            # Calculate the forward vector from the rotation matrix
            fwd = np.matmul(dst, [0,0,-1])
            
            # Add forward vector to marker service
            self._marker_service.set_forward(markers[i], fwd)
            #dot = np.dot(fwd, [0,0,1])
            #angle = np.arccos(dot)

            aruco.drawAxis(frame, cam_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)    
   