"""
AUTHOR:
Benjamin Knight

WHAT IS THIS:
This python program is to drive the UTA Mars Rover while
directly connected to the Rover's driving arduino with the standard
firmata sketch uploaded to it. This scheme uses a wired joystick, controlled through pygame's joystick layout.
OTHER JOYSTICKS MAY NOT BE MAPPED THE SAME.

JOYSTICK SCHEME:
y-axis      = power
x-axis      = turning
7 button    = kill program

Making senese of the "power" values:
0 - 0.49 | motors in "reverse", 0 is full power
0.51 - 1 | motors in "forwards", 1 is full power
0.5      | motors is not moving
"""
import pyfirmata
import pygame
import time
from pygame.locals import *

def remap(value, old_range_min, old_range_max, new_range_min, new_range_max):
    return (value - old_range_min) / (old_range_max - old_range_min) * (new_range_max - new_range_min) + new_range_min


pygame.init()

# controller setup
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
controller = joysticks[0]

# The port changes from linux to windows, with windows having multiple COM ports
board = pyfirmata.ArduinoMega('COM9') # this is (one of) windows ports
#board = pyfirmata.ArduinoMega('/dev/ttyACM0') # this is linux port

# setting pins
onboard_led =       board.get_pin('d:13:o')
l_motor_pin =       board.get_pin('d:2:p')
r_motor_pin =       board.get_pin('d:3:p')
motor_toggle_pin =  board.get_pin('d:24:o')

# pressing 'select' will quit program
while(1):
    pygame.event.pump()

    # puts rover in "stop" state if no input, avoids rover from "running away"
    motor_toggle_pin.write(0)
    l_motor_pin.write(.49804)
    r_motor_pin.write(.49804)

    # press button 7 (labelled 7), exit program
    if(controller.get_button(6)):
        print("Exiting...")
        exit()

    # both start at same power level (y axis)
    power = controller.get_axis(1)
    left_power = power
    right_power = power

    # how much we need to reduce x motors to turn (x axis)
    turn_modifier = controller.get_axis(0)

    # math stuff
    alpha = 0.5 * (turn_modifier + 1)

    # TURNING RIGHT
    if(turn_modifier > 0):
        if( alpha < 0.5 ):
            right_power = right_power = right_power * alpha
            left_power = left_power * (1-alpha)
        else:
            right_power = right_power = right_power * (1-alpha)
            left_power = left_power * alpha

    # TURNING LEFT
    elif(turn_modifier < 0):
        if( alpha > 0.5 ):
            right_power = right_power = right_power * alpha
            left_power = left_power * (1-alpha)
        else:
            right_power = right_power = right_power * (1-alpha)
            left_power = left_power * alpha

    # NOT TURNING DO NOTHING
    else:
        pass

    # remap the axis values from -1
    right_power = remap(right_power, -1, 1, 0, 1)
    left_power = remap(left_power, -1, 1, 0, 1)


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
