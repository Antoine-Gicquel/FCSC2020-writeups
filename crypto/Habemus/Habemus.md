# Habemus Clavem Corrumpere

**500 points**

## Enoncé

On vous demande d’analyser a posteriori une page mémoire extraite d’une machine compromise.

Beaucoup de données ont été effacées, mais il est primordial pour votre interlocuteur de récupérer un flag qu'il était sur le point de déchiffrer.

## Ma solution

Le challenge nous donne une page mémoire. En passant `binwalk` sur cette page un trouve 2 fichiers : `flag.txt.enc`, et un fichier DER.
On extrait le flag chiffré, et on parse la clé RSA grâce à [cette page](https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem) et un parser python que je n'ai pas retrouvé au moment de faire ce write-up.

On a donc : N, e, invq mod p, et les premiers bits de p.

Après un peu de mathématiques, j'arrive à l'équation : `invq * q² - q = 0 mod N` (prendre la définition de invq, multiplier par q l'équation)

J'effectue ensuite des recherches sur ce type d'équation, jusqu'à tomber sur [cette page](https://en.wikipedia.org/wiki/Coppersmith_method) expliquant la **méthode de Coppersmith** pour trouver les solutions d'une telle équation.

Encore et toujours des recherches, mais cette fois je sens que *je me rapproche de la solution !* Je finis par trouver une [implémentation de cette méthode avec Sage](https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/coppersmith.sage) !

Pour converger rapidement vers la solution, on peut "translater" notre équation : au lieu d'avoir une équation en q, on a une équation en (A + q'), où A contient les MSB de q, obtenable en calculant N//MSB(p). On obtient A = 0xf97104 * 256**61

Je lance le script Sage, qui trouve la valeur de `q'`. Je prends donc `q = A + q'`. Après vérification, *le résultat semble valide !*

Un rapide script python permet enfin le **déchiffrement du flag.**
