import config as cfg

class VestController:

    def __init__(self, device):
        self._device = device
        self._actuatorsMask = {}
        # 1 indicates that actuator is being used
        for actuator in cfg.actuators:
            self._actuatorsMask[actuator] = 1

    def get_actuator_indices(self):
        return cfg.actuators

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
            self._device.set_pin(pin, 0)
        self._device.set_pin(pin, value)