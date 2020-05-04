# Infiltrate

**50 points**

## Enoncé

Des agents ont réussi à exfiltrer un fichier en utilisant la LED du disque dur durant une copie de disque. Ils nous ont fourni l'image de la capture.

Retrouvez le flag.

## Ma solution

### 1ère partie : décodage de l'image

On repère tout de suite que les pixels blancs/noirs correspondent aux 0 et aux 1 de la tête de lecture.
On se lance donc dans l'écriture de 2 fichiers : l'un en parcourant l'image ligne par ligne, l'autre colonne par colonne (en réalité j'ai essayé les deux séparément), ne sachant pas dans quel sens la prendre.
En passant les 2 fichiers extraits dans `binwalk`, on remarque que l'un des deux est un exécutable (en enlevant les 16 premiers octets)

### 2ème partie : reverse de l'exécutable

J'utilise Ghidra.
Je repère rapidement que l'input qui est passé à l'exécutable est hashé SHA1, et que ce hash est comparé à une valeur hardcodée. On utilise un [SHA1 reverse](https://md5decrypt.net/Sha1/) et on obtient le flag (ne pas oublier de le mettre entre FCSC{})
