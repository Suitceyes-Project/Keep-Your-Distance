import StateMachine
import numpy as np
import config as cfg
import json

class NavigationState(StateMachine.State):

    def __init__(self, vest_controller, marker_service):
        self._device = vest_controller
        self._marker_service = marker_service

    def enter(self):
        return
    
    def exit(self):
        return

    def update(self, deltaTime):
        # find correct actuators
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
        
        sign = np.dot([0,1,0], cross)

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
                self._device.vibrate(i, 255)
            else:
                self._device.vibrate(i, 0)
    
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
            self._device.set_frequency(cfg.frequencyClose)
        elif minDistance > cfg.minDistance and minDistance < cfg.maxDistance:
            self._device.set_frequency(cfg.frequencyOptimal)
        else:
            self._device.set_frequency(cfg.frequencyFar)
            
class CatchThiefState(StateMachine.State):
    def __init__(self, vest_controller, vibration_pattern_player, state_machine):
        self._vest_controller = vest_controller
        self._vpp = vibration_pattern_player
        self._state_machine = state_machine
        with open("vibration_patterns/catch_thief.json") as json_file:
            self._clip = json.load(json_file)
            
    def enter(self):
        self._vest_controller.clear_mask()
        self._vpp.play_clip(self._clip)

    def update(self, deltaTime):
        self._vpp.update(deltaTime)
        if self._vpp.is_playing == False:
            print("Changing back to navigation")
            self._state_machine.change_to("navigation")

    def exit(self):
        return