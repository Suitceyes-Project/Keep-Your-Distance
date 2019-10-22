import config as cfg
from blinker import signal

class CatchThiefCondition:
    
    def __init__(self):
        self._catch_thief_after_time = cfg.catchThiefAfterTime
        self._current_time = 0
        self._signal_fired = False
        self._can_catch_thief = False
        
    def can_catch_thief(self):
        return self._can_catch_thief
    
    def update(self, delta_time):
        self._current_time += delta_time
        
        if self._current_time > self._catch_thief_after_time and self._signal_fired == False:
            self._can_catch_thief = True
            self._signal_fired = True
            s = signal('catch-thief')
            s.send(self)
            
class CatchThiefEventHandler:
    def on_catch_thief(self, sender):
        print("Catch the thief!", flush=True)
        self._state_machine.change_to("catch-thief")
    
    def __init__(self, state_machine):
        s = signal('catch-thief')
        s.connect(self.on_catch_thief)
        self._state_machine = state_machine
        
    