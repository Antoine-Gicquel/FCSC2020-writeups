# Bestiary

**200 points**

## Enoncé

On vous demande simplement de trouver le flag.

## Ma solution

On repère rapidement le paramètre GET `monster` qui semble louche. On tente d'y
mettre un single quote (`'`), et bingo, *erreur*.
On a une belle **LFI** qui se profile...
On essaie donc des injections un peu plus osées :
`/?monster=php://filter/convert.base64-encode/resource=index.php`

On obtient le code source de la page index ! Et là, on apprend l'existence d'un
fichier flag.php. On essaie de l'inclure, mais on se heurte au filtre mis en place
(`strpos("flag", $monster) === False`).
J'ai cru pendant longtemps que l'objectif du challengeétait de bypass ce filtre.
J'ai donc tout tenté : double encoding, espérer que le file system ne soit pas
case sensitive, des null bytes, ... Beaucoup trop de choses, et ce durant des heures.

J'en suis venu à me dire, desespéré, que le filtre n'était pas bypassable. J'ai
donc cherché ce que je pouvais faire d'autre avec ma LFI, et me suis rappelé
qu'il était courant de passer d'une **LFI** à une **RCE**.
Une petite recherche google plus tard (`from LFI to RCE`) et je tombe sur [cette
page](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).
Cette page est une vraie mine d'or. En scrollant et en arrivant à la partie
"PHPSESSID", j'ai eu *le déclic*. Dans le code source de index.php, le développeur
a déplacé les fichiers de session a un endroit accessible.
C'est là que j'ai compris pourquoi cette opération avait été faite. Ainsi, une
simple requête sur `/?monster=sessions/sess_*inserer_sessid*` permet d'inclure le
contenu de notre session.
L'exploitation se fera donc en 2 parties :
- injecter notre payload dans notre fichier de session
- inclure le fichier de session.

Rappelons-nous qu'on n'a pas le droit d'utiliser le mot "flag" a aucun moment.
Aisni, notre payload sera :
```php
<?php include(base64_decode("cGhwOi8vZmlsdGVyL2NvbnZlcnQuYmFzZTY0LWVuY29kZS9yZXNvdXJjZT1mbGFnLnBocA==")) ?>
```
où
```php
base64_decode("cGhwOi8vZmlsdGVyL2NvbnZlcnQuYmFzZTY0LWVuY29kZS9yZXNvdXJjZT1mbGFnLnBocA==") = "php://filter/convert.base64-encode/resource=flag.php"
```
On a donc :
- `/?monster=%3C%3Fphp%20include%28base64_decode%28%22cGhwOi8vZmlsdGVyL2NvbnZlcnQuYmFzZTY0LWVuY29kZS9yZXNvdXJjZT1mbGFnLnBocA%3D%3D%22%29%29%20%3F%3E`
- `/?monster=sessions/sess_*inserer_sessid*`

Bingo, on voit le base64 du code source de `flag.php`, et **on récupère le flag** !
