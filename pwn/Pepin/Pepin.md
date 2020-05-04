# Pepin

**50 points**

## Enoncé

Vous avez accès à une machine qui semble avoir un noyau Linux possédant un appel système \#333 particulier.

Une fois connecté via SSH, utilisez le `wrapper` pour lancer le challenge.

## Ma solution

Ce challenge nous plonge dans l'étude du fonctionnement des syscalls et du kernel
unix, et j'ai beaucoup appris en le réalisant.

La première difficulté, c'est de comprendre le setup du challenge : On se ssh sur
une machine, qui nous met dans une VM. Cette VM est très restreinte, nano et vim
n'existent pas.

Je me dis donc qu'on peut écrire du code en sortant de la VM (`exit`), mais cela
fait disparaitre le dossier `tmp.XXXXXX` qui est partagé entre la VM et l'hôte.
Finalement, ma méthode fut d'utiliser `scp` depuis ma machine.

On ne peut pas non plus compiler depuis la VM. On va donc compiler sur la machine
hôte (Ubuntu) (avec l'option `-static` pour inclure libc, pas présente sur la VM)
*Bon, j'ai compris le setup*.

Maintenant, passons au coeur du challenge : **comprendre cette histoire de syscall 333**.
J'ai beaucoup cherché comment dump le nom puis le code source des syscalls du kernel, et
je suis tombé sur cette commande : `</proc/kallsyms sed -n 's/.* sys_//p'`

Celle-ci permet de lister tous les syscalls. On repère un syscall getflag, mais
la question subsiste : comment appeler ce syscall ?
Je trouve la méthode syscall en C, qui permet d'appeler un syscall en lui passant
le numéro du syscall.
On essaie un simple payload :
```C
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    printf("%li\n", syscall(333));
    return 0;
}
```
Ce payload affiche 0... Bon...
Je me suis ensuite dit qu'il fallait appeler ce syscall depuis un autre syscall (ce qui s'est avéré faux),
et j'ai cherché à apprendre comment faire mon propre syscall. C'est ainsi que
j'ai appris l'existence du fichier de log du kernel, lisible avec `dmesg` depuis
un shell.
Le syscall du tutoriel affichait "Hello World" dans ce fichier. Je me suis donc
demandé si le syscall 333 n'affichait pas quelque chose dans ce fichier de log,
et bingo ! **On y trouve le flag**
