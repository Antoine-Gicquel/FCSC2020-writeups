# NECessIR

**50 points**

## Enoncé

Vous avez trouvé une télécommande infrarouge étrange dans une décharge. Visiblement, celle-ci a été modifiée par son précédent propriétaire. Curieux, vous avez enregistré le signal avec votre carte son et une vieille photodiode. Pour l'enregistrement, voici la commande tapée :

`arecord -D hw:1 -r192000 -t raw -f S16_BE -c1 ir-signal.raw`

Pouvez-vous en extraire quelque chose ?

## Ma solution

Je recherche la man page de la commande qui est utilisée. Je comprend que le
fichier qui nous est donné correspond au voltage mesuré aux bornes de la photodiode,
à une fréquence de 192kbps, et représentés par des entiers signés sur 16 bits en
big endian.

Après une phase de parsing, j'affiche l'onde ainsi obtenue. On remarque instantanément
4 blocs.

En parallèle, je fais des recherches sur le titre du challenge. NEC est un
protocole de transfert de données par infrarouge.
Google Image m'a bien aidé à comprendre comment marchait ce protocole, et m'a
permis d'approfondir mon traitement du signal obtenu.
On continue donc le parsing, pour obtenir les 0 et les 1 de chaque trame, puis
les entiers (sur 8 bits), puis passer en ASCII. Ici, lors de ma résolution
initiale, je me suis mis en Little Endian comme il était préconisé sur toutes
les images de Google Image.
Néanmoins, après une légère déception, j'ai testé le Big Endian, qui m'a **révélé
le flag** (et m'a montré que les 4 trames étaient identiques !).
