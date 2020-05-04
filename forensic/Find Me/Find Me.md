# Find Me

**50 points**

## Enoncé

Vous avez accès à un fichier find_me qui semble renfermer un secret bien gardé, qui n'existe peut-être même plus. Retrouvez son contenu !

## Ma solution

###Première idée

J'ai commencé par monter le volume, et j'ai vu le dossier `lost+found`. Le volume
est donc corrompu. Après quelques recherches, je tombe sur la commande `fsck`. Cette commande *répare* les volumes corrompus.
Cela n'a pas fonctionné, et j'ai abandonné cette piste.

### Seconde idée

Je me rappelle des challs Forensics sur RootMe, et de l'utilitaire `testdisk`.
En l'utilisant, on récupère les 20 fichiers *cachés* du volume : part00, part01, ...

On recolle le message en base64, puis on le décode. On déchiffre le fichier LUKS grâce à [cette page](https://askubuntu.com/questions/835525/how-to-mount-luks-encrypted-file).
Et on **trouve le flag !**
