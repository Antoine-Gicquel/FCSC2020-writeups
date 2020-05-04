# Chapardeur de mots de passe

**200 points**

## Enoncé

Un ami vous demande de l'aide pour déterminer si l'email qu'il vient d'ouvrir au sujet du Covid-19 était malveillant et si c'était le cas, ce qu'il risque.

Il prétend avoir essayé d'ouvrir le fichier joint à cet mail sans y parvenir. Peu de temps après, une fenêtre liée à l'anti-virus a indiqué, entre autre, le mot `KPOT v2.0` mais rien d'apparent n'est arrivé en dehors de cela.

Après une analyse préliminaire, votre ami vous informe qu'il est probable que ce malware ait été légèrement modifié, étant donné que le contenu potentiellement exfiltré (des parties du format de texte et de fichier avant chiffrement) ne semble plus prédictible. Il vous recommande donc de chercher d'autres éléments pour parvenir à l'aider.

Vous disposez d'une capture réseau de son trafic pour l'aider à déterminer si des données ont bien été volées et lui dire s'il doit rapidement changer ses mots de passe !

## Ma solution

On commence par regarder le .pcap : beaucoup de traffic HTTP, parmi lequel je repère des fichiers `gate.php` qui semblent louches, mais pas + d'infos. En parallèle, je mène mes recherches sur `KPOT v2.0` et je trouve [cette page](https://www.proofpoint.com/us/threat-insight/post/new-kpot-v20-stealer-brings-zero-persistence-and-memory-features-silently-steal) qui explique parfaitement le fonctionnement du malware.
Elle me confirme que la piste des fichiers `gate.php` est la bonne. Il faut donc que je trouve la bonne clé afin de déchiffrer les commandes données par le serveur, et la réponse du client.
Pour ce qui suit (la recherche de la clé), je travaille avec la requête GET, c'est-à-dire la phase 1 du malware, où le client demande ses instructions.

J'utilise pour cela une propriété très utile du XOR : `Message XOR Cle = Cipher => Message XOR Cipher = Cle`. Or on dispose du chiffré, et on a le format du message dans l'article mentionné au dessus. Je commence donc par effectuer un XOR entre les 16 premiers octets du chiffré et la chaine `1111111111111100`, afin d'obtenir une première clé (approximative), suffisante pour corriger le reste du message clair.

Pour obtenir la clé finale, je XOR le message clair (obtenu en corrigeant manuellement les erreurs sur le "clair" obtenu avec la première clé) avec le chiffré.

Enfin, je XOR la réponse du client (requête POST) avec la clé pour **obtenir le flag** !
