import config as cfg
import numpy as np

class ProximityConditionSystem:
    def __init__(self, game, marker_service):
        self._game = game
        self._marker_service = marker_service
        self._is_in_danger = False        
        self._max_time_in_danger = 4        
        self._time_in_danger = 0
        self._distances = []
        
    def update(self, delta_time):
        markers = self._marker_service.get_markers()
        
        if markers is None:
            return
        
        marker_count = len(markers)
        # if no marker detected and was in range
        if marker_count == 0 and self._is_in_danger == True:                       
            self._decrease_time(delta_time)            
                
        elif marker_count > 0:
            # get average distance
            average_distance = self._get_average_distance(markers)
            # if distance to any marker in near / far range
            if average_distance < cfg.minDistance or average_distance > cfg.maxDistance:
                self._increase_time(delta_time)
                # if time > max time allowed
                if self._time_in_danger > self._max_time_in_danger:
                    # end game
                    self._game.end(False)
            elif self._is_in_danger == True:
                self._decrease_time(delta_time)
    
    def _increase_time(self, delta_time):
        # increment time
        self._time_in_danger += delta_time
        print("User is in danger: " + str(self._time_in_danger))
        # set flag
        self._is_in_danger = True
    
    def _decrease_time(self, delta_time):
        self._time_in_danger -= delta_time
        self._time_in_danger = max(0, self._time_in_danger)
        print("User is safe. Cooldown: " + str(self._time_in_danger))
        # if time > time before reset
        if self._time_in_danger == 0:               
            # reset time
            self._is_in_danger = False
            
    def _get_average_distance(self, markers):
        self._distances.clear()
        
        for i in range(0, len(markers)):
            self._distances.append(self._marker_service.get_distance(markers[i]))
        
        return np.mean(self._distances)