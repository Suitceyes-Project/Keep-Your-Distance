class VibrationPatternPlayer:    

    def __init__(self, vest_controller):
        self._vest_controller = vest_controller
        self._get_frames_list = []
        self.speed = 1
        self._current_time = 0
        self._actuators = {}
        self._is_playing = False
        self._clip = None
        actuators = vest_controller.get_actuator_indices()
        for i in range(0, len(actuators)):
            self._actuators[actuators[i]] = 0
        

    def _get_frames_until(self, time):
        self._get_frames_list.clear()
        frames = self._clip["frames"]
        for frame in frames:
            if frame["time"] <= time:
                self._get_frames_list.append(frame)
            else:
                break

        return self._get_frames_list


    def _reset_actuator_values(self):
        for key in self._actuators:
            self._actuators[key] = 0

    def sample(self, time):
        frames = self._get_frames_until(time)
        self._reset_actuator_values()

        for key in self._actuators:
            for frame in frames:
                for actuator in frame["actuators"]:
                    if int(actuator["pin"]) == int(key):                        
                        self._actuators[key] = int(actuator["value"])
            self._vest_controller.vibrate(key, self._actuators[key])


    def play_clip(self, clip):
        self._current_time = 0
        self._vest_controller.set_frequency(0)
        self.speed = 1
        self.is_playing = True
        self._clip = clip

    def update(self, deltaTime):

        if self.is_playing == False:
            return

        if self._clip == None:
            return

        self._current_time += deltaTime * self.speed        
        duration = self._clip["duration"]
        
        if self._current_time > duration:
            if self._clip["isLooped"] == True:
                self._current_time = self._current_time - duration
            else:
                self._vest_controller.mute()
                self.is_playing = False
                return
            
        #print(self._current_time)
        self.sample(self._current_time)
