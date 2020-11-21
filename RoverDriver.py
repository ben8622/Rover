import msvcrt
import pyfirmata
import time

# BASIC DRIVE CONTROL VALUES
FORWARD = bytes([255])
REVERSE = bytes([0])
STOP = bytes([127])

board = pyfirmata.ArduinoMega('COM4')

# setting pins
onboard_led =       board.get_pin('d:13:o')
l_motor_pin =       board.get_pin('d:11:p')
r_motor_pin =       board.get_pin('d:12:p')
motor_toggle_pin =  board.get_pin('d:24:o')

# constantly updates statuses for example if reading analog input from potentiometer
it = pyfirmata.util.Iterator(board)
it.start()

# will be used to determine drive controls from keyboard input
ctrl = ''


# pressing 'q' will quit program
while(ctrl != b'q'):
    
    # puts rover in "stop" state if no input, avoids rover from "running away"
    motor_toggle_pin.write(0)
    l_motor_pin.write(.49804)
    r_motor_pin.write(.49804)
    
    # grab input from keyboard, don't have to press enter
    ctrl = msvcrt.getch()
    
    # forward drive, press 'w'
    if(ctrl == b'w'):
        motor_toggle_pin.write(1)
        l_motor_pin.write(1)
        r_motor_pin.write(1)
        time.sleep(.05)
        print("forwards")
        
    # backwards drive, press 's'
    elif(ctrl == b's'):
        motor_toggle_pin.write(1)
        l_motor_pin.write(0)
        r_motor_pin.write(0)
        time.sleep(.05)
        print("backwards")
        
        
# after exiting while loop, "turn off" motors
motor_toggle_pin.write(0)
l_motor_pin.write(.49804)
r_motor_pin.write(.49804)
        
    
