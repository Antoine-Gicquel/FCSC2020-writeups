import os
import rsa
os.chdir("D:\\Programmes\\Boxes\\KaliLinux\\FCSC2020\\crypto\\Habemus")

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def power(x, y, p) : 
    res = 1     # Initialize result 
  
    # Update x if it is more 
    # than or equal to p 
    x = x % p  
  
    while (y > 0) : 
          
        # If y is odd, multiply 
        # x with result 
        if ((y & 1) == 1) : 
            res = (res * x) % p 
  
        # y must be even now 
        y = y >> 1      # y = y/2 
        x = (x * x) % p 
          
    return res 

f = open("flag.txt.enc", 'rb')
message = f.read()
f.close()


n = 0xc18a6587d05c9d13e1f9df29cea97ddce10950ad2fffc8989462453ee056f6669350fe9c8ceee132e19ad9066145b1913403c2c66d53800e57fe8780e63de9f42365991883c87629a458161ea5b9ce19f2a263874f58b0067619d4b57725d0d8e694769186d2e2ebc2aa83060af82ff617011d330c3476c072c93adb4426a987
e = 65537

p = 0xc6a11d #65 bytes en on connait les 3 les plus grands

invQModP = 0x37e35b36abe4935aef71bebcbc1eb956dbbdd4fc2214bb2e09a8bc45ad3ccd565a192bf04e4c276d5d417443a2e81aeaccfafd20c356347c72901ad5497de83b

q=13064308888549438571370873238488445448652891169296386393835510331457054039783407619351737697077042913998790268029251634147470753905493239198015418902856297

p = n // q

phi = (p-1)*(q-1)

d = modinv(e, phi)


pk = rsa.PrivateKey(n, e, d, p, q)
pt = rsa.decrypt(message, pk)
print(pt)