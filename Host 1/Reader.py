import sys
import Getch
from Util import *
from socket import*

# Defined ip address of Rpi
serverName = '192.168.1.10' 
# Request for port number from Rpi
serverPort = int(input('Input the server port : ')) 
clientSocket = socket(AF_INET, SOCK_STREAM) 
# connect to Rpi
clientSocket.connect((serverName, serverPort)) 


val = int(input("Enter 0 for text transfer or 1 for file transfer : "))
# Option to enter text chosen
if val == 0: 
    print "Enter ESC to exit"
    getChObj = Getch._Getch()
    # reading from the keyboard 
    ch = getChObj.__call__() 
    # continuous read till ESC pressed
    while ch != chr(27) : 
        if ch == '\r':
            sys.stdout.write('\n')
        elif ch == chr(127):
            sys.stdout.write("\b")
        else:
            sys.stdout.write(ch)
            
        # send character to Rpi
        clientSocket.send(ch) 
        # read next character
        ch = getChObj.__call__() 
        sys.stdout.flush()
    print "closing.." 
    # closing on ESC keypress
    clientSocket.shutdown(SHUT_WR)
    clientSocket.close()
# Option to transfer file chosen
elif val == 1:
    # Kinshuk's edit
    filename = raw_input('Enter filename with extension: ')

    try:
        fopen = open(filename, "rb")
        byteval = fopen.read(1)
        while byteval != b'':
            print byteval
            clientSocket.send(byteval) 
            byteval = fopen.read(1)
            #clientSocket.send(`);
    except:
        print "Could not read file"
        sys.exit()
    finally:
        clientSocket.shutdown(SHUT_WR)
        clientSocket.close()
    # Edit ends    

    
else:
    print "WRONG INPUT: RE-RUN" 
