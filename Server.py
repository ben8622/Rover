
"""
Gregory Ferguson
"""
import socket
import threading
import msvcrt
import pyfirmata
import time
import struct


#HOST = '192.168.43.179'
HOST = 'localhost'

FORWARD = 'ABS_RZ'
BACKWARD = 'ABS_Z'

board =             pyfirmata.ArduinoMega('COM4')
l_motor_pin =       board.get_pin('d:11:p')
r_motor_pin =       board.get_pin('d:12:p')
motor_toggle_pin =  board.get_pin('d:24:o')

# constantly updates statuses for example if reading analog input from potentiometer
it = pyfirmata.util.Iterator(board)
it.start()

controller_command = 'A'

ser = 0



"""
TODO

Need to implement a standard between server and arduino to allow for communication. 
"""


def Serial_Send(data, ser):
    
    
    #print("NA")
    #At this point, need to use struct to pack that data into bytes
    
    
    #Once you have the data in bytes, send to embedded system. 
    encoded_data = []
    
    for i in range(0, len(data)):
        length = len(data[i])
        data[i] = data[i].encode('utf-8')
        encoded_data.append(struct.pack(str(length) + 's', data[i]))
    
    print(encoded_data)
       
def Serial_Receive(ser):
    
    time.sleep(5)
    #print("NA")
    
    #t = threading.Thread(target = Client_Send, args = (clientsocket, data))
    
    #t.start()
    
    while True:
        x = ser.read()
        
        #x = x.decode("utf-8")
        
        print(x)
    
    ser.close()

#This should only be called inside Serial_Receive for now
#Later on, other functions may call it, but it should never always be running
def Client_Send(clientsocket, data):
    
    
    print("NA")
    
#Easier to understand than binary data, send strings between server and client.
#Then convert to list to be used later on, data can be any type. 
def Client_Receive(clientsocket):
    global ser
    counter = 0
    while (counter < 1000):
        
        # no forward or reverse command, stop
        motor_toggle_pin.write(0)
        l_motor_pin.write(.49804)
        r_motor_pin.write(.49804)
        
        counter += 1
    
        data = (clientsocket.recv(1024))
        
        strings = data.decode('utf8')
        
        # Converting string to list 
        res = strings.strip('][').split(', ') 
        
        data = [res[0], res[1]]
        
        text = data[1].strip()
        print(text)
        
        if (text == "'ABS_RZ'"):
            motor_toggle_pin.write(1)
            l_motor_pin.write(1)
            r_motor_pin.write(1)
            time.sleep(.05)
            print("forwards")
            #send value/2 +28
            
        elif (text == "'ABS_Z'"):
            motor_toggle_pin.write(1)
            l_motor_pin.write(0)
            r_motor_pin.write(0)
            time.sleep(.05)
            print("backwards")
            #send value/2
    
            
    
    #At this point, need to check first index (res[0]) to determine what the packet data is for
    #e.g. drive commands, arm commands, etc. 
    
    

def main():
    
    
    #################################
    # Server and Client Setup
    ##################################
    
    # Using IPv4 with a TCP socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind the socket to a public host, and a well-known port
    serversocket.bind((HOST, 5220))
    # become a server socket
    serversocket.listen(5)
    
    clientsocket, address = serversocket.accept()
        
    
    t1 = threading.Thread(target = Client_Receive, args = (clientsocket,))
   
    t1.start()
    
    
    
    #Once server and client are connected, will try to connect to a serial device.
    #The rest of the system will still work if this fails
    #Will attempt to connect until successful
    
    ###################################
    # Embedded System Setup
    ###################################
    
    
 
#    
#    global ser
#    ser = serial.Serial()
#    ser.baudrate = com_port_baudrate
#    ser.port = com_port
#    ser.open() 
#    ser.flushInput()
#    
#    print(ser)
#    
#    
#    
#    if(ser.is_open != True):
#       # print("NA")
#        ser.open()
#    
#    if(ser.is_open == True):
#        
#        print("Port open")
#        #If succesful in connecting and opening the com port, start threads
#                
#        
#        
#        t2 = threading.Thread(target = Serial_Receive, args = ( ser,))
#        t2.start()
    
    #Else, try to connect again. 
    
#    data = ["XR", "220"]
#    
#     #Send controller data to embedded system
#    t = threading.Thread(target = Serial_Send, args = (data, ser))
#    t.start()
    
       
if __name__=="__main__":
    main()