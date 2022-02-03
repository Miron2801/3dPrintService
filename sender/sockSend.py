import socket

#s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.connect("file")
while True:
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect("sockets/ttyUSB0")
	try:
		data = input()
	except KeyboardInterrupt:
		exit()
	print("Send: " + data)
	#s.send(data.encode("utf-8"))
	s.sendall(data.encode("utf-8"))
	s.close()
