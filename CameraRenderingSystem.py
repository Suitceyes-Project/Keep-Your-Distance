import cv2 as cv

class CameraRenderingSystem:

    def __init__(self, camera_service):
        self._camera_service = camera_service
        cv.startWindowThread()
        cv.namedWindow("video frame")

    def update(self):
        # Display the resulting frame
        frame = self._camera_service.get_current_frame()
        if frame is None:
            return        
        cv.imshow('video frame', frame)
    
    def dispose(self):
        cv.destroyAllWindows()