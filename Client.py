"""
Gregory Ferguson
"""

import socket
import threading
import ast
import time
from inputs import get_gamepad
import pygame
from pygame.locals import *


#HOST = '192.168.43.179'
HOST = 'localhost'

controller_command = 'A'

def send(threadName, socket):

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

    """
     while True:
        events = get_gamepad()
        for event in events:

            if(event.ev_type != "Sync"):
#                print(event.code, event.state)
#                print()

                data = [controller_command, event.code, event.state]

                print(data)

                sent = socket.send(str(data).encode('utf8'))

                if(sent == 0):
                    raise RuntimeError("socket connection broken")

                del data[:]
    """


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
