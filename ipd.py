#!/usr/bin/python
'''
IP Dongle v0.4
--------------

For use with the the IP dongle availiable at:

http://4tronix.co.uk/blog/?p=337

http://4tronix.co.uk/store/index.php?rt=product/product&path=43&product_id=377

Will display the IP addresses of any found network device.

At the moment, with a single wifi adaptor and eth0 connection, the first displayed address is eth0 and the second is the wifi adaptor.


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
  
####################

'''
 





import smbus, time, subprocess, RPi.GPIO as GPIO

# Define list for digits 0..9, space, dash and DP in 7-segment (active High)
digits = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110, 0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111, 0b00000000, 0b01000000, 0b10000000]


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
   bus.write_byte_data(addr, 0x13, t) # Set bank 1 Pos to Low 
   bus.write_byte_data(addr, 0x12,digit) # Set bank 0 to digit 

speed = 0.005
	
def scroll(str1, count):#(to be scrolld, amount of times)
   string = '   ' + str1 + '   '#space at begining and end of ip
   for j in range(count):#j = repitition 
	for i in range(len(string)-3): #i appears to be number code
		str2 = string[i:(i+4)]#for scrolling text chunks of four at a time
		sDisplay2(str2, count)
      
def sDisplay2(safeStr, count): #displays number, called in scroll()
   d1 = val(safeStr[3])
   d2 = val(safeStr[2])
   d3 = val(safeStr[1])
   d4 = val(safeStr[0])
   count2 = 0
   while count2 < 10: #affects scroll speed
      sendDigit(digits[d1], 0) # '1'
      time.sleep(speed)
      sendDigit(0, 0)
      sendDigit(digits[d2], 1) # '2'
      time.sleep(speed)
      sendDigit(0, 1)
      sendDigit(digits[d3], 2) # '3'
      time.sleep(speed)
      sendDigit(0, 2)
      sendDigit(digits[d4], 3) # '0'
      time.sleep(speed)
      sendDigit(0, 3)
      count2 += 1

def val(digit): #called in sdiplay2. Looks like it converts the supplied value into bcd
   if (ord(digit) >= 48 and ord(digit) <= 57):
      return ord(digit) - 48 #bcd conversion 0-9
   elif ord(digit) == 32: #space
      return 10  # 10 is a blank
   elif ord(digit) == 46: #period
      return 11  # 11 is a dash


def get_ip(): #pulls interface info, cycles through them to retreive IP addresses and returns them all
	
	interfaces={}
	interfaceList=[]
	retreive = subprocess.Popen("ls /sys/class/net", shell = True, stdout = subprocess.PIPE)
	retreiveData = retreive.communicate()
	interfaceList = retreiveData [0].split()

	for interface in interfaceList:
		retreive = subprocess.Popen("ifconfig "+interface+" | grep -P 'inet addr' | cut -d: -f2 | awk '{ print $1}'", shell = True, stdout = subprocess.PIPE)
		retreiveData = retreive.communicate()
		ip=retreiveData[0]
		if ip:
			interfaces[interface]=ip.rstrip()
	return interfaces

addp=get_ip()
ipAddresses= sorted(addp.items()) #returned dictionary needs to be sorted...otherwise IP addresses will be presented out of order :S

for p,q in ipAddresses:
	print str(p)+": "+addp[p]
	scroll(addp[p],1)	

bus.write_byte_data(addr, 0x13, 0xff) # Set all of bank 1 to High (Off)
