import config as cfg
import numpy as np

class VibrationNavigationSystem:
    
    def __init__(self, device, marker_service):
        self._device = device
        self._marker_service = marker_service
        
    def update(self):
        # TODO: find correct actuators
        self._regulate_direction()
        
        # regulate frequency according to distance 
        self._regulate_frequency()
    
    def _regulate_direction(self):
        # get all markers
        markers = self._marker_service.get_markers()
        
        # if there are no markers visible, we will just mute the vest
        if markers is None:
            self._device.mute()
            return
        
        # find the average angle
        angles = []
        for m in markers:
            angles.append(self._marker_service.get_angle(m))
        
        # if there are no angles, mute vest
        if not angles:
            self._device.mute()
            return
        
        meanAngle = np.mean(angles)
        print("Mean angle: " + str(meanAngle))
        
        actuators = self._fetch_actuators_from_angle(meanAngle)
        
        if actuators is None:
            self._device.mute()
            return
        
        #print(actuators)
        for index in cfg.actuators:
            i = int(index)
            if i in actuators:
                print("Vibrating pin at index: " + index)
                self._device.setPin(i, 255)
            else:
                self._device.setPin(i, 0)
    
    def _fetch_actuators_from_angle(self, angle):
        actuatorRanges = cfg.actuatorRanges
        
        for r in actuatorRanges:
            startAngle = r["start"]
            endAngle = r["end"]
            if angle >= startAngle and angle <= endAngle:
                return r["actuators"]
        
        return None
        
    def _regulate_frequency(self):
        # get all markers
        markers = self._marker_service.get_markers()
        
        # if no markers are available return
        if markers is None:
            return       
        
        distances = []
        
        # find marker with min distance
        for m in markers:
            distances.append(self._marker_service.get_distance(m))
        
        # if list is empty return
        if not distances:
            return
        
        minDistance = min(distances)
        
        if minDistance < cfg.minDistance:
            self._device.setFrequency(cfg.frequencyClose)
        elif minDistance > cfg.minDistance and minDistance < cfg.maxDistance:
            self._device.setFrequency(cfg.frequencyOptimal)
        else:
            self._device.setFrequency(cfg.frequencyFar)     