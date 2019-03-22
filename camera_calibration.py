import numpy as np
import cv2 as cv

# handles camera calibration process
def calibrate(aruco_dict):
    images = capture_image()
    calibrate_arucos(images, aruco_dict)

# ----------------------------------------------------------------------------------------------------------------------
# captures images for calibration and saves them to _calibration
def capture_image():
    cam = cv.VideoCapture(0)
    cv.namedWindow("Calibrate Camera")
    images = []
    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv.imshow("Calibrate Camera", frame)
        if not ret:
            break
        k = cv.waitKey(1)

        # quit on q
        if k & 0xFF == ord('q'):

            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "camera_calibration_{}.png".format(img_counter)
            cv.imwrite("_calibration/{}".format(img_name), frame)
            images.append(frame)
            print("{} saved for calibration!".format(img_name))
            img_counter += 1

    cam.release()
    cv.destroyAllWindows()

    return images

# ----------------------------------------------------------------------------------------------------------------------
# detects aruco markers in the calibration images and calculates corners, ids
def calibrate_arucos(images, aruco_dict):
    """
    Charuco base pose estimation.
    """
    print("There are {} images for calibration. POSE ESTIMATION STARTS:".format(str(len(images))))
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv.imread(im)
        corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(frame, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv.cornerSubPix(frame, corner,
                                 winSize = (3, 3),
                                 zeroZone = (-1, -1),
                                 criteria = criteria)
            res2 = cv.aruco.interpolateCornersCharuco(corners, ids, frame, board)
            if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = frame.shape
    return allCorners, allIds, imsize

# calibrates camera via matrix and distortion coefficients estimation (needed for pose estimation)
def calibrate_camera(allCorners, allIds, imsize):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv.CALIB_USE_INTRINSIC_GUESS + cv.CALIB_RATIONAL_MODEL + cv.CALIB_FIX_ASPECT_RATIO)
    #flags = (cv.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv.TERM_CRITERIA_EPS & cv.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

