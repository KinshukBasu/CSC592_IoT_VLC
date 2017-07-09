from socket import*
import pickle
import time
from PiUtil import *
import RPi.GPIO as GPIO
from threading import Thread
import random

unacked = ""

connectionSocket=None
ackConnectionSocket=None

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.input(16)

#Setting up Rpi as the server
serverName = '192.168.1.10'
serverPort = random.randint(10000,32000)
print 'Server listening on ', serverPort, ' for data'
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1);
serverSocket.listen(1)


ack_socket = socket(AF_INET, SOCK_STREAM)
ackPort = random.randint(32000, 60000)
print 'Server listening on ', ackPort, ' for acknowledgement'
ack_socket.bind(('', ackPort))
ack_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1);
ack_socket.listen(1)

class RaspPi:
    
    def sendToLED(self, listmesg):#function to send data to LED
        for character in listmesg:
                    for i in character:
                        if i == '1':
                            GPIO.output(18, True)
                            time.sleep(0.025)
                            GPIO.output(18, False)
                        else:    
                            GPIO.output(18, False)
                            time.sleep(0.025)
    
    def formatPacket(self, payload):#function to calculate and append checksum to data
        checksum = generateChecksum(payload)
        return "1"+payload+('{0:08b}'.format(checksum))
    
    
            
    def getAscii(self,character):#function to convert character to binary representation
        val = ord(character)
        string = "{0:b}".format(val)
        if len(string)<8:
            string = '0'*(8-len(string)) + string
        return string

    def sync(self):
        global ackConnectionSocket
        preamble = "111111111111111100000000"
        stat = "5"
        while stat == "5":
            self.sendToLED(preamble)
            stat = ackConnectionSocket.recv(1)
        
        
    def communicate(self) :
        global serverSocket, unacked, ack_socket, count, stat, ackConnectionSocket, connectionSocket
        
        connectionSocket, addr1 = serverSocket.accept()#connection with Host1
        print "Host 1 ", addr1, " connected"
        
        ackConnectionSocket, addr2 = ack_socket.accept()#connection with Host2
        print "Host 2 ", addr2, " connected"
        
        print "Waiting for data from Host 1\n"
        print "Ctrl -Z to exit"
        mesg = connectionSocket.recv(1)#receive from Host1
        
        
        if mesg:
            print "received : ",mesg
            toSend = self.formatPacket(self.getAscii(mesg))#toSend = binary of char + checksum
            unacked = toSend #currently unacknowledged data
            self.sendToLED(toSend)
            try:
                ackConnectionSocket.settimeout(3)
                stat=ackConnectionSocket.recv(1) #listening for ACK
            except timeout:
                stat = "-1"
            
            while True:
                if stat=="-1": #retransmit on Timeout
                    print "RT : ",mesg
                    self.sendToLED(unacked)
                    try:
                        ackConnectionSocket.settimeout(3)
                        stat=ackConnectionSocket.recv(1)
                    except timeout:
                        stat="-1"
                elif stat=="0": #retransmit on NAK
                    print "NAK : ",mesg
                    self.sendToLED(unacked)
                    try:
                        ackConnectionSocket.settimeout(3)
                        stat=ackConnectionSocket.recv(1)
                    except timeout:
                        stat="-1"
                elif stat == "1" :#transmit next packet on ACK
                    print "received : ", mesg
                    mesg = connectionSocket.recv(1)
                    if mesg:
                        toSend = self.formatPacket(self.getAscii(mesg))
                        unacked = toSend
                        self.sendToLED(toSend)
                        try:
                            ackConnectionSocket.settimeout(3)
                            stat=ackConnectionSocket.recv(1)
                        except timeout:
                            stat="-1"
                    else:
						stat = "7"
                elif stat == "2":#needs synchronization
                    print "SYNC"
                    self.sync()
                    self.sendToLED(unacked)
                    try:
                        ackConnectionSocket.settimeout(3)
                        stat=ackConnectionSocket.recv(1)
                    except timeout:
                        stat="-1"
                else:
                    break
    
berry = RaspPi()
try:
    berry.communicate()          
except KeyboardInterrupt:
    print "End of Input:key"
except EOFError:
    print "End of Input:eof"
finally:
    GPIO.output(18,False)
    GPIO.cleanup()
    ack_socket.shutdown(0)
    ack_socket.close()
    serverSocket.shutdown(0)
    serverSocket.close()
