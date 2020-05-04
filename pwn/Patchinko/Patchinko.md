# Patchinko

**200 points**

## Enoncé

Venez tester la nouvelle version de machine de jeu Patchinko ! Les chances de victoire étant proches de zéro, nous aidons les joueurs. Prouvez qu'il est possible de compromettre le système pour lire le fichier `flag`.

Note : le service permet de patcher le binaire donné avant de l'exécuter.

## Ma solution

J'utilise Ghidra. Je commence par analyser rapidement l'exécutable, et faire un tour sur le service pour bien comprendre son fonctionnement. A première vue, on a énormément de points de départ possibles, j'en liste quelques uns :
- le `FILE*` est refermé plus tard que nécéssaire, on peut peut-être incruster quelque chose par là ?
- les buffers sont tous trop grands, on peut incruster le mot "flag" dedans ? (notamment le buffer pour 'y'/'n')
- une autre fonction, inutile, est définie. Peut-être peut on faire en sorte de démarrer le programme dans celle-ci (en changeant l'adresse dans le `__libc_start_main` )?
- le fait de pouvoir patcher 1 byte peut nous permettre de bypass un check, par exemple le 'y'/'n'
- cela peut aussi nous permettre de modifier la taille de ce qui est récupéré par fgets, et donc causer un buffer overflow
- on peut aussi changer une fonction en une autre,
- etc

La liste est donc longue, et j'ai longtemps cherché à exploiter chacune des possibilités... Le challenge avait un nombre important de solves, ce qui m'a fait abandonner plusieurs pistes que j'ai jugées *trop compliquées*.

En arrivant à l'option *changer une fonction en une autre*, j'ai parcouru chacune des fontions utilisées... jusqu'à la ligne 27 dans Ghidra : `sVar1 = strlen(local_58);`.
Juste avant cette ligne, nous avons rentré 64 caractères de notre choix dans `local_58` (supposée contenir notre nom).

*Tiens, tout à l'heure j'a déjà essayé d'exploiter une fonction à 1 seul paramètre, une chaîne de caractères... `system` !*

J'utilise donc Ghidra (`Ctrl + Shift + G`) pour changer le `strlen` en `system`, et effectivement je remarque qu'un seul octet change ! C'est gagné !

On effectue un premier test sur le netcat en modifiant cet octet et en mettant comme nom `whoami` : la commande est bien interprétée !

Un `cat flag` nous **donne enfin le flag** :)
