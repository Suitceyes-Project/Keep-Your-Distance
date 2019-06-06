from vest_device import VestDevice

device = VestDevice("10:d0:7a:16:b8:d7")
device.setPin(0,255)
device.setFrequency(0)
device.mute()

print("Disconnected")        
