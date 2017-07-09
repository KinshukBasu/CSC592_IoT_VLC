Arduino Code:
VLC_Arduino.ino

Since the program is already uploaded into the Arduino Uno, no steps
are required to run it. The program will start running as soon as the 
Arduino is powered up.

The program polls the voltage output from the photodiode every 25 ms.
This output is read from digital pin 7 on the board.
Since the polling is done using a variant of the digitalRead() function,
the Arduino only registers binary states of 1 and 0.

The digitalState() function is a high speed variant of digitalRead(),
developed by someone else, and posted on the following website:

http://masteringarduino.blogspot.com/2013/10/fastest-and-smallest-digitalread-and.html

This was used to minimise the execution time taken by the code so as to minimise the
effect of code runtime on how fast we can poll the input pin.

The Arduino Uno writes all incoming data onto the serial USB interface at a baud rate 
of 115200 bps
