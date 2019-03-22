import arucreate
import camera_calibration


police_chase_dic = arucreate.ARU_DICT()
#police_chase_dic = arucreate.ARU_DICT(3, 7, ["front", "left", "right"])

camera_calibration.calibrate(police_chase_dic._aruco_dict)

#police_chase_dic.save_aruco_images()

#police_chase_dic.lookup_aruco_nr(4)
police_chase_dic.detect_aruco()
