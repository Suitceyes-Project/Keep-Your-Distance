import cv2
assert cv2.__version__[0] >= '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob
import camera_calibration as cc
import config as cfg
import json

map1 = None
map2 = None

def fast_calibrate():
    cc.capture_image()
    ret,k,d,rvecs,tvecs = calibrate_fisheye()
    focal_length = k[0][0]
    cam_center = [k[0][2], k[1][2]]
    undistort('_calibration/camera_calibration_0.png', k, d)
    
    with open('config.json', 'r') as file:
        json_data = json.load(file)
        json_data['focalLength'] = focal_length
        json_data['camCenter'] = cam_center
        json_data['camMatrix'] = k.tolist()
        json_data['distortCoeffs'] = d.tolist()
    with open('config.json', 'w') as file:
        json.dump(json_data, file)
    
    return focal_length, cam_center, k, d

def undistort(img_path, k, d):
    # You should replace these 3 lines with the output in calibration step
    DIM=(cfg.resolutionX, cfg.resolutionY)
    K=k
    D=d

    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calibrate_fisheye():
    CHECKERBOARD = (6,9)
    subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    _img_shape = None
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    images = glob.glob('_calibration/*.png')
    
    for fname in images:
        img = cv2.imread(fname)
        if _img_shape == None:
            _img_shape = img.shape[:2]
        else:
            assert _img_shape == img.shape[:2], "All images must share the same size."
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),subpix_criteria)
            imgpoints.append(corners)
    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    rms, _, _, _, _ = \
        cv2.fisheye.calibrate(
            objpoints,
            imgpoints,
            gray.shape[::-1],
            K,
            D,
            rvecs,
            tvecs,
            calibration_flags,
            (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
        )
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape[::-1]))
    print("K=np.array(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")
    return rms, K, D, rvecs, tvecs

def undistort_frame_diff(img, K, D, DIM, balance=0.0):    
    img_dim = img.shape[:2][::-1]  

    scaled_K = K * img_dim[0] / DIM[0]  
    scaled_K[2][2] = 1.0  
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, img_dim, np.eye(3), P=None, balance=balance,new_size=DIM)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(new_K, D, np.eye(3),new_K, img_dim, cv2.CV_16SC2)
    return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

def undistort_frame(img, K, D):
    DIM=(cfg.resolutionX, cfg.resolutionY)    
    nk = K.copy()
    nk[0,0] = K[0,0]/2
    nk[1,1] = K[1,1,]/2
    global map1
    global map2
    if map1 is None or map2 is None:
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), nk, DIM, cv2.CV_16SC2)  # Pass k in 1st parameter, nk in 4th parameter
    return cv2.remap( img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    
if __name__ == '__main__':
    #fast_calibrate()
    DIM=(cfg.resolutionX, cfg.resolutionY)  
    k = cfg.camMatrix
    d = cfg.distortCoeffs
    img = cv2.imread('_calibration/camera_calibration_3.png')
    undistorted_img = undistort_frame(img, k, d)
    cv2.imshow('image',undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    