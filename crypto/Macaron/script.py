import socket

## Partie réseau

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



nc = Netcat('challenges1.france-cybersecurity-challenge.fr', 2005)

nc.read_until(b'>>> ')

nc.write(b't\n')

nc.read_until(b'>>> ')

nc.write(b'999\n')

nc.read_until(b'Tag hash:')
tag_hash = nc.read_until(b'\n').decode()[2:-1]

nc.read_until(b'>>> ')

nc.write(b'v\n')

nc.read_until(b'>>> ')

nc.write(b'9'*63 + b'\n')

nc.read_until(b'>>> ')

nc.write(tag_hash.encode() + b'\n')

nc.read_until(b'>>> ')

nc.write(b'0000000000000001\n')

print(nc.read())