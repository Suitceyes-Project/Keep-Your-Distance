import config as cfg
from Feedback import Feedback
import numpy as np

class TargetLookAtSystem:
    def __init__(self, marker_service):
        self._marker_service = marker_service
        self._has_provided_feedback = False
        self._was_looking_at_me = False
        
        
    def update(self):
        front_marker_id = cfg.get_marker_id("front")
        marker = self._marker_service.get_forward(front_marker_id)
        
        # if no marker was detected and we haven't yet notified the user
        # that it's ok to go again, tap the back
        if marker is None and self._has_provided_feedback == False and self._was_looking_at_me:
            Feedback.tap(False, 3)
            self._was_looking_at_me = False
            self._has_provided_feedback = True
            return
        
        # exit, if feedback was provided and no marker was detected
        if marker is None:
            return
        
        # if we have already told the user to stop moving, return
        if self._was_looking_at_me:
            return
        
        # check if the target is looking at the user
        dot = np.dot(marker, [0,0,1])
                        
        if dot > cfg.targetLookAtThreshold:           
            # tell the user to stop walking
            #print("Target is looking at me!", True)
            Feedback.tap(True, 3)
            self._has_provided_feedback = False
            self._was_looking_at_me = True
        
        
