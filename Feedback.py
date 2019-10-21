import config as cfg
import time

class Tap:
    duration = 0
    pins = []
    time_started = 0
    
    def __init__(self, duration: float, pins : [], time_started : float):
        self.duration = duration
        self.pins = pins
        self.time_started = time_started
    
class Feedback:
    current = None
    
    def tap(is_front, duration):
        pins =  (cfg.motors["front"] , cfg.motors["back"])[is_front == True]
        Feedback.current = Tap(duration, pins, time.time())
    
    def stop():
        Feedback.current = None
        
class FeedbackSystem:
    def __init__(self, vest):
        self._vest = vest
        self._vest.set_motor_speed(1)
        self._rotation = 0 # represents a rotation direction (back or forth)
        self._last_update = time.time()
        
    def update(self):
        # if there is no current feedback, do nothing
        if Feedback.current == None:
            return
        
        # if the current feedback has exceeded the duration,
        # reset values.
        current_time = time.time()
        if current_time - Feedback.current.time_started >= Feedback.current.duration:
            Feedback.current = None
            self._rotation = 0
            self._last_update = current_time
            return
        
        # motorInterval is the time between rotation direction changes
        # if we haven't exceeded this time, return
        if current_time - self._last_update < cfg.motorInterval:
            return
        
        # for each motor set the rotation
        for i in range(0, len(Feedback.current.pins)):
            self._vest.set_motor(Feedback.current.pins[i], (45 , 135)[self._rotation == 0])
        
        # change rotation direction and update last time
        self._rotation = (self._rotation + 1) % 2
        self._last_update = current_time
        
        