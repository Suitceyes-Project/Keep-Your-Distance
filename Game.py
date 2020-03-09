import config as cfg

class Game:   

    def __init__(self):
        self._is_over = False
        self._elapsed_time = 0
        self._game_duration = cfg.gameDuration
        self._did_win = False
        self._is_running = False
        self._progress = 0
        
    def can_catch_thief(self):
        return self._can_catch_thief
    
    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        self._progress = value

    @property
    def is_over(self):
        return self._is_over
    
    @property
    def is_running(self):
        return self._is_running
    
    @property
    def did_win(self):
        return self._did_win
        
    def start(self):
        self._is_running = True
        self._is_over = False
        self._did_win = False
        self._elapsed_time = 0
    
    def update(self, delta_time):
        self._elapsed_time += delta_time      

        if self._elapsed_time > self._game_duration:
            self.end(False)        
    
    def end(self, did_win):
        self._is_over = True
        self._is_running = False
        self._did_win = did_win