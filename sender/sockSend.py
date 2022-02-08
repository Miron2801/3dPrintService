import socket
import sys
import os
#s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.connect("file")
print("Starting SockSend at " + sys.argv[1])
prefix = "/var/www/html/3dPrintService/sender/"
os.system("touch "+prefix+"pids/" + sys.argv[1].replace('sockets/', '') + ".pid & echo '"+ str(os.getpid()) +"' >> "+prefix+"pids/" + sys.argv[1].replace('sockets/', '') + ".pid" )
while True:

	try:
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect(sys.argv[1])
		data = input()
		print("Send: " + data)
		#s.send(data.encode("utf-8"))
		s.sendall(data.encode("utf-8"))
		s.close()
	except (KeyboardInterrupt, EOFError):
                os.system("rm "+prefix+"pids/" + sys.argv[1].replace('sockets/', '') + ".pid")
                exit()
