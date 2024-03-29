import config as cfg

class VestController:

    def __init__(self, device):
        self._device = device
        self._device.set_frequency(0)
        self._actuatorsMask = {}
        self._actuatorValues = {}
        # 1 indicates that actuator is being used
        for actuator in cfg.actuators:
            self._actuatorsMask[int(actuator)] = 1
            self._actuatorValues[int(actuator)] = 0

    def get_actuator_indices(self):
        return list(cfg.actuators.keys())  

    def set_mask(self, pin):
        self._actuatorsMask[int(pin)] = 0

    def unset_mask(self, pin):
        self._actuatorsMask[int(pin)] = 1
    
    def clear_mask(self):
        for key in self._actuatorsMask:
            self._actuatorsMask[key] = 1
    
    def set_frequency(self, frequency):
        self._device.set_frequency(frequency)

    def mute(self):
        self._device.mute()
    
    def vibrate(self, pin, value):
        index = int(pin)
        v = int(value)
        if self._actuatorsMask[index] == 0:
            v = 0
        
        self._device.set_pin(index, v)