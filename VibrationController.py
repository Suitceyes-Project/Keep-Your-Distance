import config as cfg

class VestController:

    def __init__(self, device):
        self._device = device
        self._device.set_frequency(0)
        self._actuatorsMask = {}
        self._actuatorValues = {}
        # 1 indicates that actuator is being used
        for actuator in cfg.actuators:
            self._actuatorsMask[actuator] = 1
            self._actuatorValues[actuator] = 0

    def get_actuator_indices(self):
        return list(cfg.actuators.keys())

    def set_mask(self, pin):
        self._actuatorsMask[pin] = 0

    def unset_mask(self, pin):
        self._actuatorsMask[pin] = 1
    
    def clear_mask(self):
        for key in self._actuatorsMask:
            self._actuatorsMask[key] = 0

    def mute(self):
        self._device.mute()
    
    def vibrate(self, pin, value):
        if self._actuatorsMask[pin] == 0:
            value = 0
        
        if self._actuatorValues[pin] != value:
            self._actuatorValues[pin] = value            
            self._device.set_pin(pin, value)