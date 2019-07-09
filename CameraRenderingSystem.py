import cv2 as cv

class CameraRenderingSystem:

    def __init__(self, camera_service):
        self._camera_service = camera_service
        
    def __enter__(self):
        cv.startWindowThread()
        cv.namedWindow("video frame")
        return self

    def update(self):
        # Display the resulting frame
        frame = self._camera_service.get_current_frame()
        if frame is None:
            return        
        cv.imshow('video frame', frame)
    
    def __exit__(self, exc_type, exc_value, traceback):
        cv.destroyAllWindows()