Host2 Code
SerialRead.py

To execute run: python SerialRead.py


Host2 establishes TCP Connection with the RaspberryPi
When the server on the RaspberyPi is running, it displays a port number on which it is listening for 'acknowledgement'.
When the Host 2 code is executed, this port number must be entered as the server port.

Host2 writes data to a file/console (as per the option selected)

User options:

0 : Write to console
	Incoming data is displayed on the terminal on Host 2.
	Our application has support for characters such as 'Enter','Tab' and 'Backspace', but not for 'Arrow keys'.
	Use 'Ctrl+C' or 'Ctrl+Z' to exit the program.

1 : Write to file
	Incoming data is written to a file which will be created in the same working directory. The user is required to
	give an input for the file name. To ensure reconstruction, give the destination file the same extension as the
	source file.
	Use 'Ctrl+C' or 'Ctrl+Z' to exit the program.


Host2 continuously reads from the serial USB port, detection of a 1 indicates beginning of data. Host2 reads 16 bits and checks the checksum**. 
	If checksum checksout: Host 2 sends an ACK to RaspberryPi represented by '1'. Data is written on the console.
	If checksum does not : Host 2 sends a NAK to RaspberryPi represented by '0'.

After 3 consecutive NAKs detected on the same packet, a SYN signal is sent to RaspberryPi represented by '2'. 
Once a request for SYN is sent, Host2 listens for SYN Stream, and sends a SYN-ACK to RaspberryPi (represented by '4') on receiving a SYN Stream. If a synchronization stream is not  received for 600msecs, a SYN-NAK is sent to RaspberryPi, represented by '5' and Host 2 continues to listen for subsequent synchronization streams.    

** Checksum = data^key. key = 137, mutually decided between Host1 and Host2. 
