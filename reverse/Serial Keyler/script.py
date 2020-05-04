# nom à l'envers XOR 1f

import socket 

def generateKey(nom):
    ret = nom[::-1]
    ret = [chr(x ^ 0x1f) for x in ret]
    ret = "".join(ret)
    return ret.encode()

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

nc = Netcat('challenges2.france-cybersecurity-challenge.fr', 3001)

for i in range(55):
    name = nc.read_until(b'\n')
    name = name.split(b': ')[-1][:-1]
    print(name)
    key = generateKey(name)
    print(key)
    print('----- '+str(i))
    nc.write(key+b'\n')
    if i == 54:
        print(nc.read())