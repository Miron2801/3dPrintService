#!/usr/bin/python
#@author:shreya
"""\
Simple g-code streaming script
"""
 
import serial
import time
import argparse

parser = argparse.ArgumentParser(description='This is a basic gcode sender. http://crcibernetica.com')
parser.add_argument('-p','--port',help='Input USB port',required=True)
parser.add_argument('-f','--file',help='Gcode file name',required=True)
args = parser.parse_args()
 
## show values ##
print ("USB Port: %s" % args.port )
print ("Gcode file: %s" % args.file )


def removeComment(string):
	if (string.find(';')==-1):
		return string
	else:
		return string[:string.index(';')]
 
# Open serial port
#s = serial.Serial('/dev/ttyACM0',115200)
print(serial.Serial)
s = serial.Serial(args.port,250000)
print('Opening Serial Port')
 
# Open g-code file
#f = open('/media/UNTITLED/shoulder.g','r');
f = open(args.file,'r');
print ('Opening gcode file')
 
# Wake up 
#s.write("\r\n\r\n") # Hit enter a few times to wake the Printrbot
time.sleep(2)   # Wait for Printrbot to initialize
s.flushInput()  # Flush startup text in serial input
print ('Sending gcode')
time.sleep(8)
print("END of SLEEP")
# Stream g-code
while True:
	line = str(input("qwe >> "))
	l = removeComment(line)
	l = l.strip() # Strip all EOL characters for streaming
	if  (l.isspace()==False and len(l)>0) :

		print ('Sending: ' + l)
		s.write(bytes(l,'utf-8') + b'\n') # Send g-code block
		grbl_out = s.readline()
		while(grbl_out != b'ok\n'):
				time.sleep(0.1)
				grbl_out = s.readline()
#				print("WAIT")
		print(grbl_out)
		print ((bytes(' : ',"utf-8")) + grbl_out.strip())
 
#raw_input("  Press <Enter> to exit.")
 
# Close file and serial port
f.close()
s.close() 