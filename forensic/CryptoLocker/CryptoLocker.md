# CryptoLocker

**200 points**

## Enoncé

Un de nos admins nous a appelé en urgence suite à un CryptoLocker qui s'est lancé sur un serveur ultra-sensible, juste après avoir appliqué une mise à jour fournie par notre prestataire informatique.

Ce malware vise spécifiquement un fichier pouvant faire perdre des millions d'euros à notre entreprise : il est très important de le retrouver !

L'administrateur nous a dit que pour éviter que le logiciel ne se propage, il a mis en pause le serveur virtualisé et a récupéré sa mémoire vive dès qu'il a détecté l'attaque.

Vous êtes notre seul espoir.

## Ma solution

J'ai effectué ce challenge avec Volatility. Le profil est `Win7SP1x86`. On liste les commandes utilisées, et on trouve un programme `update_v0.5.exe`, pid 3388, lancé depuis le bureau, qui affiche un message suspect.
Je récupère ce programme, afin de le reverse.

J'y trouve l'existence d'un fichier `key.txt` ainsi qu'un fichier `flag.txt.enc`, tous deux sur le bureau. Je les récupère depuis le dump, et j'essaie un simple XOR. Sans succès. Ici, lors de ma résolution, j'ai tenté une attaque bruteforce sur tous les offsets possibles pour le XOR (commencer par le 2ème octet de la clé, puis par le 3ème, etc...), **ce qui m'a donné le flag**. Je n'ai réalisé que plus tard que le décalage était trouvable dans l'exécutable.
