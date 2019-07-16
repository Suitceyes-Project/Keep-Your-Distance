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
        
        cam_matrix = self._camera_service.get_matrix()
        dist_coeffs = self._camera_service.get_distortion_coefficients()
        marker_length = float(cfg.markerWidth);
        corners = self._marker_service.get_corners_array()
                
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_length, cam_matrix, dist_coeffs)
        
        for i in range(0, len(markers)):
            ##print("Distance: " + str(np.linalg.norm(tvecs[i])))
            dst, _ = cv.Rodrigues(rvecs[i])
            fwd = np.matmul(dst, [0,0,-1])
            dot = np.dot(fwd, [0,0,1])
            #angle = np.arccos(dot)
            #print(np.rad2deg(angle))
            aruco.drawAxis(frame, cam_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)    
   