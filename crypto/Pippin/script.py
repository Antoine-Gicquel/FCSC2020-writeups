import numpy as np
import socket
from base64 import b64encode as b64e, b64decode as b64d
from zlib import compress, decompress

q = 2**11
n     = 280
n_bar = 4
m_bar = 4

def get_E_from_ABSq(A, B, S, q):
    return np.mod(np.mod((B- A*S), q) + 1, q) - 1

def tryUCkb(U, C, kb):
    # vérifie si self.__decode(np.mod(C - np.dot(U, self.__S_a), self.q)) == kb
    pass

## partie tests:

S_a = np.matrix(np.random.randint(-1, 2, size = (280, 4))).astype('int64')
A = np.matrix(np.random.randint( 0, 2**11, size = (280, 280))).astype('int64')
E_a = np.matrix(np.random.randint(-1, 2, size = (280, 4))).astype('int64')
B     = np.mod(A * S_a + E_a, 2**11).astype('int64')

U = np.matrix(np.random.randint(0, q, size = (4, 280))).astype('int64')
C = np.matrix(np.random.randint(0, 1, size = (4, 4))).astype('int64')
b = np.matrix(np.random.randint(-1, 2, size = (4, 4))).astype('int64')


def __decode(mat):
    def recenter(x):
        if x > q // 2:
            return x - q
        else:
            return x

    def mult_and_round(x):
        return round((x / (q / 4)))

    out = np.vectorize(recenter)(mat)
    out = np.vectorize(mult_and_round)(out)
    return out

def __decaps(U, C):
    key_a = __decode(np.mod(C - np.dot(U, S_a), q))
    return key_a
    
    

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

nc = Netcat('challenges1.france-cybersecurity-challenge.fr', 2002)


def recupererAB():
    raw = nc.read_until(b"Possible actions:").decode()
    #nc.read()
    raw = raw.split("\n")
    Ab64 = raw[1][4:]
    Bb64 = raw[2][4:]
    A = np.reshape(np.frombuffer(decompress(b64d(Ab64)), dtype = np.int64), (280, 280))
    B = np.reshape(np.frombuffer(decompress(b64d(Bb64)), dtype = np.int64), (280, 4))

    return A, B

def testKeys(U, C, keyB):
    raw = nc.read_until(b">>> ")
    nc.write(b'1\n')
    nc.read_until(b'U = ')
    nc.write(b64e(compress(U.tobytes())) + b'\n')
    nc.read_until(b'C = ')
    nc.write(b64e(compress(C.tobytes())) + b'\n')
    nc.read_until(b'key_b = ')
    nc.write(b64e(compress(keyB.tobytes())) + b'\n')
    ret = nc.read_until(b'\n').decode()
    return 'Success' in ret

def sendKeys(S, E):
    raw = nc.read_until(b">>> ")
    nc.write(b'2\n')
    nc.read_until(b'S_a = ')
    nc.write(b64e(compress(S.tobytes())) + b'\n')
    nc.read_until(b'E_a = ')
    nc.write(b64e(compress(E.tobytes())) + b'\n')
    print(nc.read())
    

## implementation


A, B = recupererAB()


reconstitution_Sa = [[0,0,0,0] for i in range(n)]
C = [[0 for _ in range(n_bar)] for __ in range(n_bar)]
C[0] = [q/4, q/4, q/4, q/4]
C = np.matrix(C).astype('int64')
possibilites_Sa = [-1, 0, 1]
possibilitesLignes = []
for a in possibilites_Sa:
    for b in possibilites_Sa:
        for c in possibilites_Sa:
            for d in possibilites_Sa:
                l = [a,b,c,d]
                if l.count(0) == 2 and l.count(1) == 1 and l.count(-1) == 1:
                    possibilitesLignes.append([a,b,c,d])



for i in range(n):
    trouve_ligne = False
    U = [[0 for _ in range(n)] for __ in range(n_bar)]
    U[0][i] = -q/4
    U = np.matrix(U).astype('int64')
    for j in range(len(possibilitesLignes)):
        a,b,c,d = possibilitesLignes[j]
        keyB = [[0 for _ in range(n_bar)] for __ in range(n_bar)]
        keyB[0] = [-a+1, -b+1, -c+1, -d+1]
        keyB = np.matrix(keyB).astype('int64')
        res = testKeys(U, C, keyB)
        if res:
            trouve_ligne = True
            reconstitution_Sa[i] = [-a, -b, -c, -d]
            break
    
    if not trouve_ligne:
        print("Echec ligne" + str(i))
    else:
        if i%10 == 0:
            print(i)
            

print("Fini de dump S")

reconstitution_Sa = np.matrix(reconstitution_Sa).astype('int64')
E = get_E_from_ABSq(A, B, reconstitution_Sa, q)

sendKeys(reconstitution_Sa, E)