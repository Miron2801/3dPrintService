
import sys
import os
import re
import threading
import socket
import time
import serial
if os.name == 'nt': 
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))

def removeComment(string):
	if (string.find(';')==-1):
			return string
	else:
			return string[:string.index(';')]
def grep(regexp, include_links=False):
    r = re.compile(regexp, re.I)
    for info in comports(include_links):
        port, desc, hwid = info
        if r.search(port) or r.search(desc) or r.search(hwid):
            yield info


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Serial port enumeration')

    parser.add_argument(
        'regexp',
        nargs='?',
        help='only show ports that match this regex')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show more messages')

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress all messages')

    parser.add_argument(
        '-n',
        type=int,
        help='only output the N-th entry')

    parser.add_argument(
        '-s', '--include-links',
        action='store_true',
        help='include entries that are symlinks to real devices')

    args = parser.parse_args()

    hits = 0
    # get iteraror w/ or w/o filter
    if args.regexp:
        if not args.quiet:
            sys.stderr.write("Filtered list with regexp: {!r}\n".format(args.regexp))
        iterator = sorted(grep(args.regexp, include_links=args.include_links))
    else:
        iterator = sorted(comports(include_links=args.include_links))
    # list them
    ports_detected = []
    for n, (port, desc, hwid) in enumerate(iterator, 1):
        if args.n is None or args.n == n:
#            sys.stdout.write("{:20}\n".format(port))
            ports_detected.append(port)
            if args.verbose:
                sys.stdout.write("    desc: {}\n".format(desc))
                sys.stdout.write("    hwid: {}\n".format(hwid))
        hits += 1
    return ports_detected
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# test

print(main())
activeSock  = [[],[]]   #0 - sockets 1 - serials
activePorts = []
def processPort(serial, socketCon):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        connection, address = socketCon.accept()
        message = connection.recv(1024).decode()
        l = removeComment(str(message))
        l = l.strip() # Strip all EOL characters for streaming
        if  (l.isspace()==False and len(l)>0) :
            print ('Sending: ' + l)
            serial.write(bytes(l,'utf-8') + b'\n') # Send g-code block
            grbl_out = serial.readline()
            while(grbl_out != b'ok\n'):
                    time.sleep(0.1)
                    grbl_out = serial.readline()
            print(grbl_out)
            print ((bytes(' : ',"utf-8")) + grbl_out.strip())
    
printers = []
while 1:
    nowPorts = main()
    for i in nowPorts:      #add port
            if(i not in activePorts):
                nameFile = "sockets/" + i.split('/')[2]
                if(os.path.exists(nameFile)):
                    os.remove(nameFile)
                print("New dev: " + i)
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.bind("sockets/" + i.split('/')[2])
                s.listen(1)
                os.system("sudo chmod 777 "+ "sockets/" + i.split('/')[2])
                activeSock[0].append(s)         #сокет
                activeSock[1].append(serial.Serial(i,250000))       #сериал
                activePorts.append(i)

                printers.append(threading.Thread(
                target=processPort, name=i, args=(serial.Serial(i,250000), s, )))
                printers[len(printers)-1].start()
            else:
                pass
    for port in activePorts:  #remove port
            if(not(os.path.exists(port))):
                for i in activeSock[0]:
                    if(i.getsockname() == port.replace("/dev/", "sockets/")):
                        for printer in printers:
                                if(printer.getName() == port):
                                        printer.do_run = False
                        i.close()
                        activeSock[0].remove(i)
                        os.remove("sockets/" + port.split('/')[2])
                        activePorts.pop(port)
                        activeSock[1].remove(activePorts.pop(port))
                        print(activePorts)
            else:
                pass
    


