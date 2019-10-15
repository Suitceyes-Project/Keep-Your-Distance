from vest_device import VestDevice
import time

vest = VestDevice("10:d0:7a:16:b8:d7")
vest.setMotorSpeed(1)
i = 0;

while(i < 50):
    vest.setMotor(0, 45)
    time.sleep(0.2)
    vest.setMotor(0, 135)
    time.sleep(0.2)
    i+=1
