# Petite Frappe 2

**50 points**

## Enoncé

Lors de l’investigation d’un poste GNU/Linux, vous analysez un nouveau fichier qui semble être généré par un programme d’enregistrement de frappes de clavier. Retrouvez ce qui a bien pu être écrit par l’utilisateur de ce poste à l’aide de ce fichier !

Format du flag : `FCSC{xxx}`, où `xxx` est la chaîne que vous aurez trouvée.

## Ma solution

Après des tentatives infructueuses en utilisant le fichier header contenant les keycodes sur UNIX, je me décide à utiliser Google de manière efficace :
En effet, Google permet d'effectuer une recherche parmi toutes les pages web contenant exactement les mots voulus grace aux guillemets.
Je recherche donc : `"key press 46"` afin de voir si cela correspond à quelque chose de connu... On ne sait jamais !

Effectivement, les 2 premiers liens nous parlent de Xinput.
Je recherche donc `xinput decoder`, et le [premier lien](https://github.com/ronanguilloux/Bin/blob/master/python/xinput-decoder.py) nous donne un script python décodant les fichiers enregistrés avec Xinput.
En exécutant le script avec : `chmod +x xinput-decoder.py && cat petite_frappe_2.txt | ./xinput-decoder.py` **j'obtiens le flag !**
