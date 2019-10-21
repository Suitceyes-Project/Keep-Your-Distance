class VibrationPatternPlayer:    

    def __init__(self, vest_controller):
        self._vest_controller = vest_controller
        self._get_frames_list = []
        self.speed = 1
        self._current_time = 0
        self._actuators = {}
        actuators = vest_controller.get_actuators()
        for i in range(0, len(actuators)):
            self._actuators[actuators[i]] = 0
        

    def _get_frames_until(self, time):
        self._get_frames_list.clear()
        frames = clip["frames"]
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
                    if actuator["pin"] == key:
                        self._actuators[key] = actuator["value"]
            self._vest_controller.vibrate(key, self._actuators[key])


    def play_clip(self, clip):
        self._current_time = 0
        speed = 1
        is_playing = True
        self.clip = clip

    def update(self, deltaTime):

        if self.is_playing == False:
            return

        if self.clip == None:
            return

        self._current_time += deltaTime * speed
        duration = clip["duration"]
        
        if self._current_time > duration:
            if clip["isLooped"]:
                self._current_time = self._current_time - duration
            else:
                self._vest_controller.mute()
                self.is_playing = False
                return

        self.sample(self._current_time)
