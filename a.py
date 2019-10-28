#!/usr/bin/env python3
import smbus, threading
from threading import Thread

import time

from math import acos, pi

from ev3dev2.motor import LargeMotor, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_A, OUTPUT_C, MediumMotor, OUTPUT_D
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import TouchSensor

from ev3socketclient import Client



lastMessage = []

host = '192.168.1.3'
port = 51004 # fig number

# code goes here ---------------




client = Client(host, port)





class MessageHandler():
    def __init__(self):
        self.state = 0
        self.message = []
    
    def updateMessage(self, message):
        self.message = message
        self.state = message[0]
        print("in handler : " + str(message) + " " + str(self.state))

messagehandler = MessageHandler()



#rotateServoOnDefault()


print("connecting")

client.connect(messagehandler)

print("connected")

time.sleep(0.2)

waitForCommand()

# drone_motor.on(SpeedPercent(-100))

# time.sleep(0.3)

# drone_motor.reset()

finish()