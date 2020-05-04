# Serial Keyler

**50 points**

## Enoncé

On vous demande d'écrire un générateur d'entrées valides pour ce binaire, puis de le valider sur les entrées fournies par le service distant afin d'obtenir le flag.

## Ma solution

J'utilise Ghidra pour le reverse.
Le reverse est assez direct (modulo les erreurs de décompilation de Ghidra, facilement repérables et compréhensibles). On y voit une boucle, qui parcourt l'input dans le sens inverse, et qui réalise un XOR avec 0x1f.

C'est donc là notre keygen : **Il prend le nom, le retourne, et XOR chaque caractère avec 0x1f**.

Encore une fois on réalise un script Python pour automatiser la partie réseau, et on **obtient le flag** au bout de 55 tours.
