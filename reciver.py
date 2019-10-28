import socket 
import struct
from ev3dev.ev3 import Leds
from ev3dev.ev3 import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_A, OUTPUT_C, MediumMotor, OUTPUT_D
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev.ev3 import *
from time import sleep

left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_D)
mid_motor = MediumMotor(OUTPUT_B)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '192.168.43.83'
port = 6166 # random number
a = False

# try : 
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
# except Exception:
    # pass
print('hi')
s.bind(('', port))
print('first done')
s.listen(5)
print('second done')
# creating a listening socket
print('lul')
conn, addr = s.accept()
print('conn gotten')
########################################################

def handleMessage(message):
    angle_coef = 20
    global readyToRide
    # print('delivered : '+ str(message[0]))
    if message[0] == 254:
        return
    if message[0] == 255:
        mid_motor.stop()
        
    if message[0] % 4 == 1:
        Leds.set_color(Leds.RIGHT, Leds.RED)
        Leds.set_color(Leds.LEFT, Leds.GREEN)  
        left_motor.run_forever(speed_sp= -1000)
        if(min((message[0] - 128) // 4 * angle_coef, 1000) < -800):
            right_motor.run_forever(speed_sp= min((message[0] - 128) // 4 * angle_coef, 1000))
        else:
            right_motor.run_forever(speed_sp= -1000)    
        print(-1000, min(-1000 + message[0] // 4 * angle_coef, 1000))
        # Sound.speak('RUN')
        # print("a")
        Sound.speak('Stop')
        print("b")
        print("ya loh")
        Sound.speak('HAHA PAPA CARLO YA OBMANUL TEBIA')
        print("ya loh1")
        sleep(5)
        print("ya loh2")
    if message[0] % 4 == 0:
        Leds.set_color(Leds.RIGHT, Leds.YELLOW) 
        right_motor.stop()
        left_motor.stop()
        Sound.speak('Stop')
        print("b")
        print("ya loh")
        Sound.speak('HAHA PAPA CARLO YA OBMANUL TEBIA')
        print("ya loh1")
        sleep(5)
        print("ya loh2")
    if message[0] % 4 == 2:
        Leds.set_color(Leds.LEFT, Leds.RED) 
        Leds.set_color(Leds.RIGHT, Leds.GREEN) 
        if(min((message[0] - 128) // 4 * angle_coef, 1000) < -800):
            left_motor.run_forever(speed_sp= min((message[0] - 128) // 4 * angle_coef, 1000))
        else:
            left_motor.run_forever(speed_sp= -1000)  
        right_motor.run_forever(speed_sp= -1000)
        print(min(-1000 + message[0] // 4 * angle_coef, 1000), -1000)
        Sound.speak('Stop')
        print("b")
        print("ya loh")
        Sound.speak('HAHA PAPA CARLO YA OBMANUL TEBIA')
        print("ya loh1")
        sleep(5)
        print("ya loh2")
    if message[0] % 4 == 3:
        readyToRide = True
        left_motor.run_forever(speed_sp=-1000)
        right_motor.run_forever(speed_sp=-1000)
# считывает сокет и выводит расшифрованное содержимое
def reader():
    global conn
    while a:
        message = []
        part = conn.recv(1)
        # print(part)

        if (len(part) == 0):
            conn.close()
            break

        message_size = int.from_bytes(part, byteorder='big')
            
        for i in range(message_size):
            part = conn.recv(8)
            message.append(int.from_bytes(part, byteorder='big', signed=True))
     #message.append(int.from_bytes(part, byteorder='big', signed=True))

        handleMessage(message)
        if len(part) == 0 : break

#send to ev3

def send(*args):
        
    #msg = len(args).to_bytes(1, byteorder='big')
    msg = len(args).to_bytes(1, byteorder='big')
    for a in args:
        msg += (a).to_bytes(8, byteorder='big', signed = True)
    
    # print(msg)
    conn.send(msg)

print(conn,'  ',addr)

a = True
try:
    reader()
except:
    mid_motor.stop()
    left_motor.stop()
    right_motor.stop()