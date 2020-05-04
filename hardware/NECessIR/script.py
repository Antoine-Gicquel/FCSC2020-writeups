import os
import ctypes
import matplotlib.pyplot as plt
os.chdir("D:\\Programmes\\Boxes\\KaliLinux\\FCSC2020\\hardware\\NecessIR")

f = open("ir-signal.raw", "rb")
data = f.read()
f.close()

frequ = 192000//16

# conversion S16_BE
def to8bin(n):
    binN = bin(n)[2:]
    return "0"*(8-len(binN)) + binN

cleanData = [0, 0, 0]
for i in range(0, len(data), 2):
    int16 = int( to8bin(data[i]) + to8bin(data[i+1]), 2)
    int16_signed = ctypes.c_int16(int16).value
    cleanData.append(int16_signed)

timeStamps = [i for i in range(len(cleanData))]


fig = plt.figure()
l, = plt.plot(timeStamps, cleanData)
plt.show()



# passage en fronts montants (1) /descendants (0)

fronts = []
for i in range(2, len(cleanData)-1):
    if abs(cleanData[i]) > 2 and abs(cleanData[i-1]) + abs(cleanData[i-2]) < 2:
        fronts.append((1, i))
    elif cleanData[i] == 0 and cleanData[i+1] == 0 and cleanData[i-1] != 0:
        fronts.append((0, i))



frames = [[] for i in range(4)]

i = 1
frameNb = -1
while i < len(fronts):
    if fronts[i][0] == fronts[i-1][0]:
        print(fronts[i][1])
    if fronts[i][0] == 0 and fronts[i-1][0] == 1 and fronts[i][1] - fronts[i-1][1] > 1650 and fronts[i][1] - fronts[i-1][1] < 1800:
        frameNb += 1
        i+=1
    elif fronts[i][0] == 1:
        if fronts[i-2][0] == 1 and fronts[i][1] - fronts[i-2][1] > 190 and fronts[i][1] - fronts[i-2][1] < 240:
            frames[frameNb].append(0)
        elif fronts[i-2][0] == 1 and fronts[i][1] - fronts[i-2][1] > 380 and fronts[i][1] - fronts[i-2][1] < 480:
            frames[frameNb].append(1)
    
    i+=1

# passage en entiers
intFrames = [[] for i in range(len(frames))]

for i in range(len(frames)):
    for j in range(0, len(frames[i]), 8):
        bitstring = frames[i][j:j+8]
        bitstring = [str(x) for x in bitstring]
        entier = int(''.join(bitstring), 2)
        intFrames[i].append(entier)


# toutes les frames sont identiques -> on en regarde une

frame = intFrames[0]
print(''.join([chr(x) for x in frame]))






































