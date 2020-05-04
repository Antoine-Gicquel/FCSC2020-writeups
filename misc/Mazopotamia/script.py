import socket
import base64
import io
from PIL import Image
from heapq import *
 
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

oppose = {"N" : "S", "S": "N", "W": "E", "E": "W"}

def dijkstra (s, t, voisins):
    M = set()
    d = {s: 0}
    p = {}
    suivants = [(0, s)] # tas de couples (d[x],x)

    while suivants != []:

        dx, x = heappop(suivants)
        if x in M:
            continue

        M.add(x)

        for w, y in voisins(x):
            if y in M:
                continue
            dy = dx + w
            if y not in d or d[y] > dy:
                d[y] = dy
                heappush(suivants, (dy, y))
                p[y] = x

    path = [t]
    x = t
    if t not in d:
        return False

    while x != s:
        x = p[x]
        path.insert(0, x)

    return path


class Maze:
    
    tailleCase = 64
    free = (255,255,255)
    wall = (0, 0, 0)
    
    def __init__(self, base64string):
        msg = base64.b64decode(base64string)
        buf = io.BytesIO(msg)
        self.image = Image.open(buf).convert("RGB")
        self.sommets = dict() # (255, 0, 0) : [(1, 3), (7, 4), ...]
        self.aretes = dict() # ((1, 3, "N"), (7, 4, "E")) : 'NEEWES'
        
        self.colorOrder = []
        i = 2
        while self.image.getpixel((i*Maze.tailleCase + Maze.tailleCase//2, Maze.tailleCase + Maze.tailleCase//2)) != Maze.free:
            coul = self.image.getpixel((i*Maze.tailleCase + Maze.tailleCase//2, Maze.tailleCase + Maze.tailleCase//2))
            self.colorOrder.append(coul)
            self.sommets[coul] = []
            i+=2
        
        self.width, self.height = self.image.size
        self.width = self.width//Maze.tailleCase - 2
        self.height = self.height//Maze.tailleCase - 5
        self.map = [[0 for i in range(self.height)] for j in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                coul = self.image.getpixel((Maze.tailleCase + Maze.tailleCase//2 + i*Maze.tailleCase, 3*Maze.tailleCase + Maze.tailleCase//2 + j*Maze.tailleCase))
                self.map[i][j] = coul
                if coul in self.sommets.keys():
                    self.sommets[coul].append((i, j))
        
        # partie graphe
        for i in range(len(self.colorOrder)):
            coul = self.colorOrder[i]
            next_coul = self.colorOrder[(i+1)%len(self.colorOrder)]
            for case1 in self.sommets[coul]:
                for case2 in self.sommets[next_coul]:
                    for lat1 in self.lateralisation(case1):
                        for lat2 in self.lateralisation(case2):
                            if lat1 == "N":
                                case1lat = (case1[0], case1[1]-1)
                            if lat1 == "S":
                                case1lat = (case1[0], case1[1]+1)
                            if lat1 == "W":
                                case1lat = (case1[0]-1, case1[1])
                            if lat1 == "E":
                                case1lat = (case1[0]+1, case1[1])
                            if lat2 == "N":
                                case2lat = (case2[0], case2[1]-1)
                            if lat2 == "S":
                                case2lat = (case2[0], case2[1]+1)
                            if lat2 == "W":
                                case2lat = (case2[0]-1, case2[1])
                            if lat2 == "E":
                                case2lat = (case2[0]+1, case2[1])
                                
                            path = self.path_exists(case1lat, case2lat)
                            if path != False:
                                self.aretes[((case1[0], case1[1], lat1), (case2[0], case2[1], lat2))] = path
        
        # trouver le départ et l'arrivee
        
        self.depart = 0
        self.arrivee = 0
        for i in range(self.width):
            if self.map[i][-1] != Maze.wall:
                if self.map[i][-1] == self.colorOrder[0]:
                    self.depart = (i, self.height-1)
                else:
                    self.arrivee = (i, self.height-1)
            
        
    def path_exists(self, case1, case2):
        """ Retourne le chemin entre 2 cases si il existe, False sinon"""
        # on fait un dijkstra entre case1 et case2, en considérant toutes les cases blanches comme des points
        
        def voisins(case):
            ret = []
            x, y = case
            for eps in [-1, 0, 1]:
                for delt in [-1, 0, 1]:
                    if abs(eps) + abs(delt) == 1 and x+eps > 0 and x+eps < self.width and y+delt > 0 and y+delt < self.height:
                        if self.map[x+eps][y+delt] == Maze.free or (x+eps, y+delt) == case2:
                            ret.append((1, (x+eps, y+delt)))
            return ret
            
        p = dijkstra(case1, case2, voisins)
        if p == False:
            return False
        # on transforme maintenant le path en chaine de directions
        dir = ""
        for i in range(1, len(p)):
            x, y = p[i]
            xo, yo = p[i-1]
            if x - xo == 1:
                dir += "E"
            elif x - xo == -1:
                dir += "W"
            elif y - yo == 1:
                dir += "S"
            elif y - yo == -1:
                dir += "N"
        return dir
    
    def lateralisation(self, case):
        x, y = case
        if y+1 == self.height or self.map[x][y + 1] == Maze.free:
            return "NS"
        else:
            return "WE"
    
    
    def solve(self):
        finalPath = "N"
        
        def voisins(case):
            x, y, state = case
            if state[1:] == "int":
                return [(0.1, (x, y, oppose[state[0]]+"ext"))]
            else:
                # on cherche les sommets adjacents à (x, y, state[0])
                ret = []
                for a, b in self.aretes.keys():
                    if a == (x, y, state[0]):
                        ret.append((1, (b[0], b[1], b[2]+"int")))
                return ret
        
        p = dijkstra((self.depart[0], self.depart[1], "Next"), (self.arrivee[0], self.arrivee[1], "Nint"), voisins)
        for i in range(1, len(p), 2):
            finalPath += self.aretes[((p[i-1][0], p[i-1][1], p[i-1][2][0]), (p[i][0], p[i][1], p[i][2][0]))]
            finalPath += oppose[p[i][2][0]]
        return finalPath

## Main part
nc = Netcat("challenges2.france-cybersecurity-challenge.fr", 6002)

nc.read_until(b'ready...')
nc.write(b'\n')


nc.read_until(b'------------------------ BEGIN MAZE ------------------------')

for i in range(31):
    mazeStr = nc.read_until(b"------------------------- END MAZE -------------------------")
    nc.read_until(b">>>")
    mazeStr = mazeStr.decode("utf-8").replace('\n', '').replace('------------------------- END MAZE -------------------------', '')
    mazeToSolve = Maze(mazeStr)
    solution = mazeToSolve.solve()
    print(solution)
    nc.write(solution.encode() + b'\n')
    print(i)
    if i != 30:
        print(nc.read_until(b'------------------------ BEGIN MAZE ------------------------'))
    else:
        print(nc.read())






