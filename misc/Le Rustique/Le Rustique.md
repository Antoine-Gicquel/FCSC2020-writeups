# Le Rustique

**200 points**

## Enoncé

On vous demande d'auditer cette solution de vérification syntaxique en Rust.

## Ma solution

On ne dispose que de l'information suivante : **le programme a-t-il compilé ?**

Ainsi, la seule chose que je peux exploiter est l'ensemble de fonctions de
type `const fn` de Rust, qui s'exécutent au moment de la compilation (et qui
peuvent par conséquent provoquer des erreurs de compilation)

On utilise dans un premier temps la macro `std::include_str!`, qui inclut un fichier
sous forme de chaine de caractère *au moment de la compilation*.
Ceci peut me permettre de localiser le flag, par guessing. En effet, après
quelques tentatives infructueuses, je trouve un fichier `flag.txt` dans le répertoire parent.
Coup de chance, on prend :)

Maintenant, on peut essayer de faire une *attaque blind* sur le contenu de cette
chaine de caractères :
L'idée, c'est de faire crash la compilation en assignant à un entier unsigned
une valeur négative.
Le payload final pour la dichotomie caractère par caractère:
```Rust
fn main() {
    const WHATEVER: u8 = std::include_str!("../flag.txt").as_bytes()[$c] - $val - 1;
}
```
où `$c` est l'indice du caractère sur lequel on effectue la dichotomie, et `$val` la
valeur de comparaison.

Ce code va compiler si et seulement si l'octet d'indice `$c` est plus grand
(strictement) que `$val`.

Je fais un petit script python pour automatiser tout ça, et on **obtient le flag !**
