import numpy as np
import cv2 as cv
from cv2 import aruco
import matplotlib as mpl
import matplotlib.pyplot as py_mpl
from PIL import Image
import os, os.path


# get charuco board from predefined dictionary
predef_aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
board = aruco.CharucoBoard_create(7, 5, 1.1, 1, predef_aruco_dict)

# calibrates camera if aruco-board images are already available
def fast_calibrate():
    images = []
    path = "_calibration/"
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower().endswith(".png"):
            images.append(Image.open(os.path.join(path, f)))

    # initiates next calibration steps
    allCorners, allIds, imsize = calibrate_arucos(images)
    ret, matrix, dist, rot_vect, trans_vect = calibrate_camera(allCorners, allIds, imsize)

    # visually checks calibration
    check_calibration(matrix, dist)

    focal_length = matrix[0][0]
    cam_center = [matrix[2][0], matrix[2][1]]

    return focal_length, cam_center

# handles camera calibration process
def calibrate():
    # draw and save board
    imboard = board.draw((2000, 2000))
    cv.imwrite("_calibration/charuco_board.jpg", imboard)
    fig = py_mpl.figure("Aruco-Board for Calibration")
    ax = fig.add_subplot(1, 1, 1)
    py_mpl.imshow(imboard, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")
    py_mpl.show()

    # initiates next calibration steps
    images = capture_image()
    allCorners, allIds, imsize = calibrate_arucos(images)
    ret, matrix, dist, rot_vect, trans_vect = calibrate_camera(allCorners, allIds, imsize)

    # visually checks calibration
    check_calibration(matrix, dist)

    focal_length = matrix[0][0]
    cam_center = [matrix[2][0], matrix[2][1]]

    return focal_length, cam_center

# ----------------------------------------------------------------------------------------------------------------------
# captures images for calibration and saves them to _calibration
def capture_image():
    cam = cv.VideoCapture(1) # 0 webcam of laptop
    cv.namedWindow("Calibrate Camera")
    images = []
    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv.imshow("Calibrate Camera", frame)
        print("Please take several images of different angles of the Aruco-Board using your camera. Press space to take a photo.")
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
def calibrate_arucos(images):
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
        # import image in grayscale
        frame = cv.imread(im.filename, 0)
        corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(frame, predef_aruco_dict)

        if len(corners) > 0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv.cornerSubPix(frame, corner,
                                 winSize=(3, 3),
                                 zeroZone=(-1, -1),
                                 criteria=criteria)
            res2 = cv.aruco.interpolateCornersCharuco(corners, ids, frame, board)
            if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3 and decimator % 1 == 0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator += 1

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

def check_calibration(mtx, dist):
    py_mpl.figure()
    frame = cv.imread("_calibration/camera_calibration_3.png")
    img_undist = cv.undistort(frame, mtx, dist, None)
    py_mpl.subplot(1, 2, 1)
    py_mpl.imshow(frame)
    py_mpl.title("Raw image")
    py_mpl.axis("off")
    py_mpl.subplot(1, 2, 2)
    py_mpl.imshow(img_undist)
    py_mpl.title("Corrected image")
    py_mpl.axis("off")
    py_mpl.show()




