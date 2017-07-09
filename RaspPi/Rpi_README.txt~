Pi.py
To execute run: python Pi.py on Raspbian

Change Server name in Pi.py to the current IP address of the RaspberryPi
RaspberryPi is the server and is always on. It waits for connections from Host1 and Host2 (in that order). 
Upon establishing the connection, RaspberryPi listens(blocking) for a message (i.e. data byte) from Host1. 
The received message is formatted using formatPacket() which calculates and appends checksum for the data byte represented in its binary

This formatted data is stored as 'last unacked' data which can be used if retransmission is required.  
The sendToLED() function is used to send data to LED i.e. to control the LED.
The RaspberryPi then listens for an ACK/NAK/SYN from Host2. Different actions are taken in the event of each message as follows:
	ACK received (stat = 1):
	Read next byte from Host 1, update unacked and send to LED. 
	NAK received (stat = 0):
	Retransmit data in unacked. 
	SYN received (stat = 2):
	Transmit the synchronization stream (111111111111111100000000) to Arduino till a SYNACK (stat = 4) is received from Host 2. If a 	 SYNNAK (stat = 5) is received from Host2, continue sending synchronization stream. This helps to regain synchronization and prevents 		any drift in reading of bits. 

Loss of ACK
A timer is used to wait for an ACK, if the timer times-out, the data in 'last unacked' is retransmitted.

If the communication channel is down, the server will keep trying to re-transmit data, i.e. no loss of data will occur even when the channel is down, such as in the example of using cardboard given in the project description.


                                                                  ::::Methods used::::

sendToLED (self,listmesg):: Controls the LED connected to GPIO port 18. LED is ON for 25msecs for a bit '1' and it is OFF for 25msecs for a bit '0' 

formatPacket(self,payload):: Generates checksum and creates and returns packet to be transmitted.
			     Packet format : '1' + payload + checksum
			     The leading '1' is to ensure we can catch the beginning of every transmission, like a primitive preamble.

getAscii(self,character):: returns binary representation of a character in the form of a string. 

sync(self):: transmits the synchronization stream and continues to do so every time a SYNNAK is received. It returns only when a SYNACK is received. 

generateChecksum(payload):: returns checksum for the payload. Checksum = key^payload and key =137, mutually decided between Host1 and Host2.
