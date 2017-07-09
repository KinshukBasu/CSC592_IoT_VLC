import time, serial
from socket import*
import pickle
import sys

#well known server name and port for the raspi
rasppiName = '192.168.1.10'
raspiport = int(input('Input the server port : '))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((rasppiName,raspiport))


outputType = int(input('Enter 0 for console output, 1 for file output : '))

if outputType==0:
	print ""
else:
	filename = raw_input('Enter filename : ')


#for global scope
#file in write binary mode
if(outputType != 0):
	f = open(filename,"wb")
	f.close()

ser = serial.Serial('/dev/ttyACM0',115200)
time.sleep(1)
data = ""
NAK_ctr = 0
msg = 0

#checksum calculation, used in checking the checksum
def generateChecksum(datachunk):
	dat = int(datachunk,2)
	return (137 ^ dat)

#checking the checksum
def check_checksum(data, checksum):
	new_checksum = generateChecksum(data)
	if checksum!=new_checksum:
		return 0
	return 1

#to write characters into the file
def fileWrite(data):
	global filename
	a = data[0:8]
	ch = chr(int(a,2))
	with open(filename, "ab") as f:
		f.write(ch)

#to display characters on the console
def display(data):
	a = data[0:8]
	if a=="00001101":
		sys.stdout.write("\n")
	elif a=="01111111":
		sys.stdout.write("\b")
	else:
		ch = chr(int(a,2))
		sys.stdout.write(ch)
	sys.stdout.flush()

#to check for the receipt of the preamble - (synchronsation stream),
#if not received the preamble in 600 ms, timer expires and sends a status 5 to the raspi
#if received the preamble, send status 4 to the raspi
def listenForSync():
	start = time.time()
	ctr = 0
	global reading
	global msg
	global ser
	global clientSocket
	
	while True:
		reading = ser.read()
		duration = time.time()-start
		if(duration>=0.6):
			#print duration
			clientSocket.send('5')
			start=time.time()

		#print "reading : ",reading,"counter: ",ctr
		if(reading=='1'):
			ctr+=1
		else:
			ctr=0


		if(ctr>=10):
			while ser.read()!="0":
				pass
			msg = '4'
			#print "sync-ed"
			return




while(True):

	data = ""
	
	#listens till it receives a '1'
	while(ser.read() != '1'):
		pass
		
	#reads the following 16 bits
	data = ser.read(16)
	
	#to calculate the checksum
	a = check_checksum(data[0:8], int(data[8:],2) )			
	#returns 1 if it's ok

	#if checksum is a desired value
	if(a==1):
		msg = '1'
		if(outputType==0):
			display(data)
		else:
			fileWrite(data)

		NAK_ctr=0

	#if checksum is giving a value not desired
	#on the receipt of 3 NAKs, send a status 2 and try to sync with the raspi
	else:
		msg = '0'
		#print "NAK"
		NAK_ctr += 1
		if(NAK_ctr ==3):
			NAK_ctr=0
			clientSocket.send('2')
			listenForSync()

	#send the status message to the raspi
	clientSocket.send(msg)