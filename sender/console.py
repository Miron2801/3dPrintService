import socket
import os
import serial
import time
nameFile = "sockets/file"

def removeComment(string):
	if (string.find(';')==-1):
			return string
	else:
			return string[:string.index(';')]
s = serial.Serial("/dev/ttyACM0",250000)
s.flushInput()
time.sleep(8)
if(os.path.exists(nameFile)):
	os.remove(nameFile)
#os.system("sudo chmod 777 "+ nameFile)
socketCon = socket.socket(
    socket.AF_UNIX, socket.SOCK_STREAM)
socketCon.bind(nameFile)
socketCon.listen(1)
os.system("sudo chmod 777 "+ nameFile)

while True:
	connection, address = socketCon.accept()
	message = connection.recv(1024).decode()
	l = removeComment(str(message))
	l = l.strip() # Strip all EOL characters for streaming
	if  (l.isspace()==False and len(l)>0) :
		print ('Sending: ' + l)
		s.write(bytes(l,'utf-8') + b'\n') # Send g-code block
		grbl_out = s.readline()
		while(grbl_out != b'ok\n'):
				time.sleep(0.1)
				grbl_out = s.readline()
#                               print("WAIT")
		print(grbl_out)
		print ((bytes(' : ',"utf-8")) + grbl_out.strip())
s.close()
f.close()
socketCon.close() 
