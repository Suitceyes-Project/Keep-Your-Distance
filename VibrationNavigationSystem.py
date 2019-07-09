import config as cfg

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
        for index in cfg.actuators:
            self._device.setPin(int(index), 255)
        
        
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
            print("Person is too close")
            self._device.setFrequency(0)
        elif minDistance > cfg.minDistance and minDistance < cfg.maxDistance:
            print("Person is in optimal range")
            self._device.setFrequency(100)
        else:
            print("Person is too far away")
            self._device.setFrequency(10)
        
        
        