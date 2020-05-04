import os
os.chdir("D:\\Programmes\\Boxes\\KaliLinux\\FCSC2020\\forensics\\CryptoLocker")

f = open("flag.txt.enc", "rb")
encoded = f.read()
f.close()

f = open("key.txt", "rb")
key = f.read()
f.close()


flag = ""
for j in range(len(key)):
    flag = ""
    for i in range(len(encoded)):
        flag += chr((encoded[i] ^ key[(i+j)%len(key)]) % 256)
    if "FCSC" in flag:
        print(flag)
        break