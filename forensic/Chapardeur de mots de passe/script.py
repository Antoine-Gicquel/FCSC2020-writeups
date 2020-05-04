import os
import base64
os.chdir("D:\\Programmes\\Boxes\\KaliLinux\\FCSC2020\\forensics\\Chapardeur de mots de passe")


def xor(message, cle):
    ret = ""
    for i in range(len(message)):
        ret += chr(message[i] ^ cle[i%len(cle)])
    return ret.encode()

f = open("Gates/input.php", "r")
input_commands = f.read()
f.close()

f = open("Gates/output.php", "rb")
output = f.read()
f.close()

input_commands = base64.decodebytes(input_commands.encode())

cle = b'tDlsdL5dv25c1RhvtDlsdL5dv25c1Rhv'

print(xor(input_commands, cle))

print(xor(output, cle))