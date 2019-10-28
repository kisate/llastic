import socket, threading
from mailbox import Client, MessageHandler
# from ev3dev.ev3 import Leds
lastMessage = []
host = '192.168.43.83'
port = 6166 # fix number
msg = [0]


class MyMessageHandler(MessageHandler):
    def processMessage(self):
        # if (self.state == 1) :
            # if (self.message[1] == 1):
                # Leds.set_color(Leds.RIGHT, Leds.ORANGE) 
                # print("a")
        # elif (self.state == 2):
            # Leds.set_color(Leds.RIGHT, Leds.GREEN) 
            # print("b")
        print(self.message[1])        


# client.reader()