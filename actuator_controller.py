import config as cfg

class ActuatorController:
  
    def __init__(self, device, arucreate):
        self._device = device
        self._arucreate = arucreate
        device.setFrequency(0)
        
    def update(self, angle):               
        # get pins from angle
        actuatorConfig = cfg.get_actuators()
        pins = self.__angleToPinArray(angle)
        for pinIndex in actuatorConfig:
            if pinIndex in pins:
                self._device.setPin(int(pinIndex), 0)
            else:
                self._device.setPin(int(pinIndex), 0)
            
    
    def __angleToPinArray(self, angle):
        # print(angle)
        # TODO: 
        return [0,1];
