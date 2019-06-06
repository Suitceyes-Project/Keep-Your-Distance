from bluepy.btle import UUID, Peripheral

class VestDevice:
    def __init__(self, deviceAddr):
        try:
            self._peripheral = Peripheral(deviceAddr)
            serviceUUID = UUID("713d0000-503e-4c75-ba94-3148f18d941e")
            characteristicUUID = UUID("713d0003-503e-4c75-ba94-3148f18d941e")
            s = self._peripheral.getServiceByUUID(serviceUUID)
            self._characteristic = s.getCharacteristics(characteristicUUID)[0]
        except Exception as e:
            print("Error: " + str(e))
            
    def __isValidState(self):        
        return self._peripheral.getState() == "conn"
    
    def __write(self, byteArr):
        self._peripheral.writeCharacteristic(self._characteristic.getHandle(), byteArr)
            
    def setPin(self, index, intensity):
        """Sets a pin to a given intensity.
        index: an integer from 0 - 6
        intensity: an integer from 0 - 255
        """
        if self.__isValidState():
            rList=[0,index,intensity]
            self.__write(bytes(rList))
            
    def setFrequency(self,frequency):
        """Sets the frequency of the entire vest.
        frequency: an integer from 0 - 255
        """
        if self.__isValidState():
            rList=[4,frequency]
            self.__write(bytes(rList))
    
    def mute(self):
        """Stops all motors on the vest from vibrating"""
        if self.__isValidState():
            rList=[3]
            self.__write(bytes(rList))