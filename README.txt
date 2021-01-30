Steps to driving the Rover:

Before doing anything:
	-HAVE PYTHON DOWNLOADED AND KNOW HOW TO RUN A PYTHON PROGRAM
	-HAVE THESE PYTHON MODULES INSTALLED:
		-socket
		-threading
		-pyfirmata
		-pygame
		-time
		-ast
	-KEEP THE ROVER ELEVATED BEFORE THE PROGRAM IS RUNNING (for now)
	-SOMEONE NEEDS TO STAY NEAR IT IN CASE A WIRE DISCONNECTS AND IT RUNS OFF (she moves fast)
	-BE SAFE HAVE FUN (:

1.) Power the Rover. This will also power the raspberry pi that is the "brains" of the drive.
	The raspberry pi will project its own wifi that you need to connect the client computer to.

2.) Connect to the raspberry pi's wifi. 
	Network:	"NameOfNetwork"
	Password:	"password"

3.) Make sure your joystick / controller is connected 

4.) Run the joystick_client.py or controller_client.py program
	- The program will automatically connect to the pi (it will timeout if it doesn't)
	- There motors of the Rover may start on startup

5.) Flip the 2nd switch on the Rover to allow power to the motors.

6.) To kill the programs press:
	Xbox Controller -> Select button
	Joystick -> "7" button
	or "ctrl + c" in your terminal
