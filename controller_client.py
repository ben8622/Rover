"""
AUTHORS:
Gregory Ferguson & Benjamin Knight

WHAT IS THIS:
This python program is to drive the UTA Mars Rover while
wirelessly connected (sockets) to the Rover's driving arduino with the standard
firmata sketch uploaded to it. This scheme uses a wired Xbox 360 (NOT XBOX ONE)
controller, controlled through pygame's joystick layout

CONTROLLER SCHEME:
Left trigger            = power sent to left motors
Right trigger           = power sent to right motors
Left + Right bumpers    = motors now go in reverse
A button                = toggles full power
Select button           = exit program

Making senese of the "power" values:
0 - 0.49 | motors in "reverse", 0 is full power
0.51 - 1 | motors in "forwards", 1 is full power
0.5      | motors is not moving
"""

import socket
import threading
import ast
import time
from inputs import get_gamepad
import pygame
from pygame.locals import *

# Raspberry Pi's IP on network it projects
HOST = '192.168.4.1'

# function to send strings to server
def send(threadName, socket):

    # controller initiaization
    pygame.init()
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
    controller = joysticks[0]
    reverse = False

    while True:
        pygame.event.pump()

        if(controller.get_button(6)):
            print("Exiting...")
            exit()

        # divider ensure only half power given unless "A" button pressed down
        divider = 0.125
        reverse = 0
        right_power =   controller.get_axis(5)
        left_power =    controller.get_axis(2)

        # "A" button pressed, give full power
        if(controller.get_button(0)):
            divider =  0.25

        right_power =   divider * (right_power + 1)
        left_power =    divider * (left_power + 1)

        # Bumpers are pressed, go reverse. Must be doing both to avoid breaking bot
        if(controller.get_button(4) and controller.get_button(5)):
            left_power =    0.5 - left_power
            right_power =   0.5 - right_power
            reverse = 1
        else:
            left_power =    0.5 + left_power
            right_power =   0.5 + right_power

        # construct packet string array
        data = [str(round(left_power, 2)), str(round(right_power, 2)), str(reverse)]

        print(data)

        sent = socket.send(str(data).encode('utf8'))

        if(sent == 0):
            raise RuntimeError("socket connection broken")

        time.sleep(.1)
        del data[:]


def receive(threadName, socket):

    data = socket.recv(1024)

    strings = data.decode('utf8')

    #Converting string to list
    res = strings.strip('][').split(', ')

    print(res)

    #At this point, will check to see what the data from server is and update the GUI


def main():


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, 5220))

    print("Connected")


#    t2 = threading.Thread(target = receive, args = ("Thread-2", s))
#
#    t2.start()

    t1 = threading.Thread(target = send, args = ("Thread-1", s))
    t1.start()
    t1.join()


if __name__=="__main__":
    main()
