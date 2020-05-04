import os
from PIL import Image
os.chdir("D:\\Programmes\\Boxes\\KaliLinux\\FCSC2020\\reverse\\Infiltrate")

im = Image.open("infiltrate.png").convert('1')

w, h = im.size

binres = ''

for j in range(h):
    for i in range(w):
        if im.getpixel((i,j)) > 100:
            binres += '1'
        else:
            binres += '0'

binlist = []

for i in range(0, len(binres), 8):
    binlist.append(int(binres[i:i+8], 2))

f = open('decoded', 'wb')
binary_format = bytearray(binlist[16:])
f.write(binary_format)
f.close()