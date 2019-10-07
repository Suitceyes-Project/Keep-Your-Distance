import cv2 as cv
import sys

class CameraRenderingSystem:

    def __init__(self, camera_service):
        if 'headless' in sys.argv:
            print("Running in headless mode", flush=True)
            self._is_headless = True
        else:
            self._is_headless = False
        self._camera_service = camera_service
        
    def __enter__(self):
        if not self._is_headless:
            cv.startWindowThread()
            cv.namedWindow("video frame")
        return self

    def update(self):
        if self._is_headless:
            return
        
        # Display the resulting frame
        frame = self._camera_service.get_current_frame()
        if frame is None:
            return        
        cv.imshow('video frame', frame)
    
    def __exit__(self, exc_type, exc_value, traceback):
        cv.destroyAllWindows()