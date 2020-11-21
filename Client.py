"""
Gregory Ferguson
"""

import socket
import threading
import ast
from inputs import get_gamepad


#HOST = '192.168.43.179'
HOST = 'localhost'

controller_command = 'A'

def send(threadName, socket):
    
    
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