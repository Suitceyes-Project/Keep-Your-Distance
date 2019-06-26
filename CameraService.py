import camera_calibration
import cv2 as cv
import config as cfg

class CameraService:
    def __init__(self):
        self._focal_length, self._cam_center, self._cam_matrix, self._dist_coeffs = camera_calibration.fast_calibrate()              
        
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
        return ret, self._frame

    
    