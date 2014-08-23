#!/usr/bin/python

'''

IP Dongle Test
--------------

For use with the the IP dongle availiable at:

http://4tronix.co.uk/blog/?p=337

http://4tronix.co.uk/store/index.php?rt=product/product&path=43&product_id=377

Will allow a test of the IP dongle by displaying a count of 0 - 9 on all four availiable displays.


######GPL v3#######

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

''' 

import smbus, time, subprocess, RPi.GPIO as GPIO

# Define list for digits 0..9, space, dash and DP in 7-segment (active High)
digits = [0b00111111,0b00000110, 
	  0b01011011,0b01001111,
	  0b01100110,0b01101101, 
	  0b01111101,0b00000111, 
	  0b01111111,0b01101111, 
	  0b00000000,0b01000000] 
	  #0b10000000]

if GPIO.RPI_REVISION > 1:
   bus = smbus.SMBus(1) # For revision 1 Raspberry Pi, change to bus = smbus.SMBus(1) for revision 2.
else:
   bus = smbus.SMBus(0) # For revision 1 Raspberry Pi, change to bus = smbus.SMBus(1) for revision 2.
   

addr = 0x20 # I2C address of MCP23017
bus.write_byte_data(addr, 0x00, 0x00) # Set all of bank 0 to outputs 
bus.write_byte_data(addr, 0x01, 0x00) # Set all of bank 1 to outputs 
bus.write_byte_data(addr, 0x13, 0xff) # Set all of bank 1 to High (Off) 
#end of housekeeping


def sendDigit(digit, pos): #send digit to display
   '''
	led 0: 254
	led 1: 253
	led 2: 251
        led 3: 247
	none:  255
   '''
   t = (1<<pos) ^ 255
   bus.write_byte_data(addr, 0x13, 0) # Set bank 1 Pos to Low 
   print "sending value: "+str(digit)+" to the selected bank "+str(t)
   bus.write_byte_data(addr, 0x12,digit) # Set bank 0 to digit 

speed = 0.0005

z = len(digits)

print z
	
for x in range(0,len(digits)):
	print "digits[]: "+str(x)+" : "+str(digits[x])
	sendDigit(int(digits[x]),2)
	time.sleep(1)
        bus.write_byte_data(addr, 0x13, 0xff) # Set all of bank 1 to High (Off)
