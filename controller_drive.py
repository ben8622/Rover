"""
AUTHOR:
Benjamin Knight

WHAT IS THIS:
This python program is to drive the UTA Mars Rover while
directly connected to the Rover's driving arduino with the standard
firmata sketch uploaded to it. This scheme uses a wired Xbox 360 (NOT XBOX ONE)
controller, controlled through pygame's joystick layout
"""

"""
CONTROLLER SCHEME

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
import pyfirmata
import pygame
import time
from pygame.locals import *

pygame.init()

# controller setup
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
controller = joysticks[0]

# The port changes from linux to windows, with windows having multiple COM ports
board = pyfirmata.ArduinoMega('COM3') # this is (one of) windows ports
#board = pyfirmata.ArduinoMega('/dev/ttyACM0') # this is linux port

# setting pins
onboard_led =       board.get_pin('d:13:o')
l_motor_pin =       board.get_pin('d:11:p')
r_motor_pin =       board.get_pin('d:12:p')
motor_toggle_pin =  board.get_pin('d:24:o')

while(1):
    pygame.event.pump()

    # puts rover in "stop" state if no input, avoids rover from "running away"
    motor_toggle_pin.write(0)
    l_motor_pin.write(.49804)
    r_motor_pin.write(.49804)

    # press select button, exit program
    if(controller.get_button(6)):
        print("Exiting...")
        exit()

    # divider ensure only half power given unless "A" button pressed down
    divider = 0.125
    reverse = False
    right_power = controller.get_axis(2)
    left_power = controller.get_axis(5)

    # "A" button pressed, give full power
    if(controller.get_button(0)):
        divider =  0.25

    right_power =   divider * (right_power + 1)
    left_power =    divider * (left_power + 1)

    # Bumpers are pressed, go reverse. Must be doing both to avoid breaking bot
    if(controller.get_button(4) and controller.get_button(5)):
        left_power =    0.5 - left_power
        right_power =   0.5 - right_power
        reverse = True
    else:
        left_power =    0.5 + left_power
        right_power =   0.5 + right_power

    # send motors their values
    motor_toggle_pin.write(1)
    l_motor_pin.write(left_power)
    r_motor_pin.write(right_power)

    # visualize what's being sent
    print(f"L Power:{left_power} |R Power:{right_power}")

    # avoid cpu overloading
    time.sleep(.05)

# after exiting while loop, "turn off" motors
motor_toggle_pin.write(0)
l_motor_pin.write(.49804)
r_motor_pin.write(.49804)
