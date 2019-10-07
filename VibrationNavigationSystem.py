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
        
        # get all translations
        translations = []
        for m in markers:
            position = self._marker_service.get_translation(m)
            translations.append(position)
        
        if not translations:
            self._device.mute()
            return
        
        # calculate average position
        meanTranslation = np.mean(translations, axis=0)
        
        # normalize the direction
        direction = meanTranslation/np.linalg.norm(meanTranslation)
        
        # calculate angle 
        dot = np.dot(direction, [0,0,1])
        angle = np.rad2deg(np.arccos(dot))
        cross = np.cross(direction, [0,0,1])
        
        sign = np.dot([0,1,0], cross);

        if sign > 0:
            angle = -angle
        
        #print(angle, flush=True)
        # fetch correct actuators
        actuators = self._fetch_actuators_from_angle(angle)
        
        if actuators is None:
            self._device.mute()
            return
        
        #print(actuators)
        for index in cfg.actuators:
            i = int(index)
            if i in actuators:
                #print("Vibrating pin at index: " + index)
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