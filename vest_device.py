from bluepy.btle import UUID, Peripheral
import PyCmdMessenger
from abc import ABC, abstractmethod
import sys
sys.path.insert(1, '/home/pi/Documents/PCA9685-Controller')
from suitceyes import VibrationMotorDriver

class VestDevice(ABC):
    
    @abstractmethod
    def set_pin(self, index, intensity):
        pass
    
    @abstractmethod
    def set_frequency(self, frequency):
        pass
    
    @abstractmethod
    def mute(self):
        pass
    
    @abstractmethod
    def set_motor(self, index, rotation):
        pass
    
    @abstractmethod
    def set_motor_speed(self, speed):
        pass

class DummyVestDevice(VestDevice):
    def set_pin(self, index, intensity):
        pass
    
    def set_frequency(self, frequency):
        pass
    
    def mute(self):
        pass
    
    def set_motor(self, index, rotation):
        pass
    
    def set_motor_speed(self, speed):
        pass

class I2CVestDevice(VestDevice):
    def __init__(self, *addresses):
        self._board_count = len(addresses)
        self._driver = VibrationMotorDriver(*addresses)
    
    def __enter__(self):
        self._driver.start()
        return self

    def __exit__(self, type, value, traceback):
        # Make sure the vest is muted and that the connection is closed.
        self._driver.stop()
    
    def set_pin(self, index, intensity):
        # map 0 - 255 value to 0 - 1 range
        intensity = intensity / 255        
        self._driver.set_vibration(index, intensity)
    
    def set_frequency(self, frequency):
        for i in range(self._board_count):
            self._driver.set_frequency(i, frequency)
    
    def mute(self):
        self._driver.mute_all()
    
    def set_motor(self, index, rotation):
        pass
    
    def set_motor_speed(self, speed):
        pass

class BleVestDevice(VestDevice):
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
            
    def set_pin(self, index, intensity):
        """Sets a pin to a given intensity.
        index: an integer from 0 - 6
        intensity: an integer from 0 - 255
        """
        if self.__isValidState():
            rList=[0,index,intensity]
            self.__write(bytes(rList))
            
    def set_frequency(self,frequency):
        """Sets the frequency of the entire vest.
        frequency.
        """
        if self.__isValidState():
            rList=[4, frequency & (255), (frequency & (255 << 8)) >> 8, (frequency & (255 << 16)) >> 16, (frequency & (255 << 24)) >> 24]
            b = bytes(rList)
            self.__write(b)
    
    def mute(self):
        """Stops all motors on the vest from vibrating"""
        if self.__isValidState():
            rList=[3]
            self.__write(bytes(rList))
    
    def set_motor(self,index,rotation):
        """
        Sets a given motor index to a given target rotation.
        """
        if self.__isValidState():
            rList = [11,index,rotation]
            self.__write(bytes(rList))
            
    def set_motor_speed(self,speed):
        """
        Changes how long it takes to move 1 degree per millisecond.
        """
        if speed <= 0:
            raise ValueError("speed must be greater than 0.")
        rList = [12,speed]
        self.__write(bytes(rList))
        
class UsbVestDevice:
    """
    Basic interface for sending commands to the vest using a
    serial port connection.
    """

    commands = [["PinSet","gg"],
                ["PinMute","g"],
                ["GloveSet","gg*"],
                ["GloveMute",""],
                ["FreqSet","g"],
                ["PinGet","g"],
                ["FreqGet",""],
                ["PinState","gg"],
                ["FreqState","g"],
                ["StringMsg","s"],
                ["DebugSet","g"],
                ["SetMotor", "gg"],
                ["SetMotorSpeed", "g"]]

    def __init__(self, device):
        """
        Creates a new instance of Vest.
        Inputs:        
            device:
                The path to the device, e.g.: "/dev/ttyACM0" or "COM3"
        """
        self._board = PyCmdMessenger.ArduinoBoard(device, baud_rate=115200)
        self._connection = PyCmdMessenger.CmdMessenger(self._board, UsbVestDevice.commands, warnings=False)        

    def __enter__(self):
        self.set_frequency(0)
        return self

    def __exit__(self, type, value, traceback):
        # Make sure the vest is muted and that the connection is closed.
        self.mute()
        self._board.close()

    def set_pin(self,pin,value):
        """
        Sets a pin to a given value. This sets the vibration intensity of a given pin.
        Inputs:
            pin: 
                The pin index whose value should be set. This should be a byte value.
            value:
                A byte value (0-255) representing the vibration intensity. 0 is no vibration, 255
                is the max intensity.
        """
        self._connection.send("PinSet",pin,value)

    def mute_pin(self,pin):
        """
        Sets the vibration intensity for a given pin to 0.
        Inputs:
            pin: The pin which will be muted.
        """
        self._connection.send("PinMute", pin)

    def mute(self):
        """
        Mutes all pins on the vest.
        """
        self._connection.send("GloveMute")
    
    def set_frequency(self,frequency):
        """
        Sets the frequency of the entire vest.
        Inputs:
            frequency: The frequency in milliseconds.
        """
        self._connection.send("FreqSet", frequency)
        
    def set_vest(self, pin_value_dict, frequency):
        values = []

        for key in pin_value_dict:
            values.append(key)
            values.append(pin_value_dict[key])
        
        values.append(frequency)
        self._connection.send("GloveSet", *values)
    
    def get_pin(self,pin):
        """
        Gets the vibration intensity for a given pin.
        Inputs:
            pin: The pin index whose intensity should be fetched.
        """
        self._connection.send("PinGet", pin)
        return self._connection.receive()
    
    def set_motor(self,index,rotation):
        self._connection.send("SetMotor",index,rotation)
        
    def set_motor_speed(self,speed):
        """
        Changes how long it takes to move 1 degree per millisecond.
        """
        self._connection.send("SetMotorSpeed", speed)