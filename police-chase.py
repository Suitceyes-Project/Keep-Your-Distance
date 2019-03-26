import arucreate
import camera_calibration


#focal_length = camera_calibration.calibrate() # check camera_calibration.calibrate_arucos "im.filename" does not exist (no problem for fast_calirate()
focal_length = camera_calibration.fast_calibrate()

police_chase_dic = arucreate.ARU_DICT()
#police_chase_dic = arucreate.ARU_DICT(3, 7, ["front", "left", "right"])

police_chase_dic.set_focal_length(focal_length)
police_chase_dic.set_marker_width()

#police_chase_dic.save_aruco_images()
#police_chase_dic.lookup_aruco_nr(4)
police_chase_dic.detect_aruco()
