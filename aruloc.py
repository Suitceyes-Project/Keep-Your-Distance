import cv2 as cv
import arucreate

# captures camera view
def camera_cap():
    cap = cv.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv.imshow('video frame', gray)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


police_chase_dic = arucreate.ARU_DICT(4, 4,"front", "left", "right", "back")
#camera_cap()
