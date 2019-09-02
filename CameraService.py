import camera_calibration
import fisheye_calibration
import cv2 as cv
import config as cfg
import numpy as np

class CameraService:
    def __init__(self):        
        if cfg.calibrate:
            self._focal_length, self._cam_center, self._cam_matrix, self._dist_coeffs = (fisheye_calibration.fast_calibrate(), camera_calibration.fast_calibrate())[cfg.useFisheye]
        else:
            self._focal_length = cfg.focalLength
            self._cam_center = cfg.camCenter
            self._cam_matrix = cfg.camMatrix
            self._dist_coeffs = cfg.distortCoeffs
        
    def __enter__(self):
        self._cap = cv.VideoCapture(cfg.camera) # 0 webcam of laptop # 1 external cam  
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        print("Releasing video capture")
        self._cap.release()
    
    def get_matrix(self):
        return self._cam_matrix
    
    def get_distortion_coefficients(self):
        return self._dist_coeffs
    
    def get_focal_length(self):
        return self._focal_length
    
    def get_camera_center(self):
        return self._cam_center
    
    def get_current_frame(self):
        return self._frame
    
    def read(self):
        ret, self._frame = self._cap.read()
        
        # Undistort image if using fisheye
        if cfg.useFisheye:
            DIM=(cfg.resolutionX, cfg.resolutionY)
            h,w = self._frame.shape[:2]
            K = self._cam_matrix
            D = self._dist_coeffs
            map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
            self._frame = cv.remap(self._frame, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
        
        #self._frame = fisheye_calibration.undistort_frame(self._frame, self._cam_matrix, self._dist_coeffs, 0.2)
        
        return ret, self._frame

    
    