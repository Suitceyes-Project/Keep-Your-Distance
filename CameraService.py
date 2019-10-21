import camera_calibration
import fisheye_calibration
import cv2 as cv
import config as cfg
import numpy as np
from threading import Thread

class CameraService:

    def __init__(self):
        self._stopped = False
        self._grabbed = False
        self._frame = None
        if cfg.calibrate:
            self._focal_length, self._cam_center, self._cam_matrix, self._dist_coeffs = (fisheye_calibration.fast_calibrate(), camera_calibration.fast_calibrate())[cfg.useFisheye]
        else:
            self._focal_length = cfg.focalLength
            self._cam_center = cfg.camCenter
            self._cam_matrix = cfg.camMatrix
            self._dist_coeffs = cfg.distortCoeffs
        
    def __enter__(self):
        self._cap = cv.VideoCapture(cfg.camera) # 0 webcam of laptop # 1 external cam
        self._cap.set(cv.CAP_PROP_FRAME_WIDTH, cfg.resolutionX)
        self._cap.set(cv.CAP_PROP_FRAME_HEIGHT, cfg.resolutionY)
        self._cap.set(cv.CAP_PROP_FPS, 30)
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        print("Releasing video capture")
        self._cap.release()
    
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def stop(self):
        self._stopped = True
    
    def update(self):
        while True:
            if self._stopped:
                return
            
            (grabbed, frame) = self._cap.read()

            if cfg.useFisheye:
                self._frame = fisheye_calibration.undistort_frame(frame, self._cam_matrix, self._dist_coeffs)
            else:
                self._frame = frame
            self._grabbed = grabbed
    
    def get_matrix(self):
        return self._cam_matrix
    
    def get_distortion_coefficients(self):
        return self._dist_coeffs
    
    def get_focal_length(self):
        return self._focal_length
    
    def get_camera_center(self):
        return self._cam_center
    
    def get_current_frame(self):
        return (self._grabbed, self._frame)   