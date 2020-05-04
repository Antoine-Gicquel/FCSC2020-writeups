# Clepsydre

**200 points**

## Enoncé

À l'origine, la clepsydre est un instrument à eau qui permet de définir la durée d'un évènement, la durée d'un discours par exemple. On contraint la durée de l’évènement au temps de vidage d'une cuve contenant de l'eau qui s'écoule par un petit orifice. Dans l'exemple du discours, l'orateur doit s'arrêter quand le récipient est vide. La durée visualisée par ce moyen est indépendante d'un débit régulier du liquide ; le récipient peut avoir n'importe quelle forme. L'instrument n'est donc pas une horloge hydraulique (Wikipedia).

## Ma solution

Le challenge a une allure d'énigme du Père Fouras...

Ma première piste a été d'imaginer une *clepsyre numérique*, avec un compteur qui commençait "plein", et qui diminuait régulièrement jusqu'à arriver à 0 au bout de 15 secondes. J'ai donc essayé d'envoyer un mot de passe quelconque au bout de 14.99s. Sans succès.

Je me suis dit que la clé n'était pas dans le temps d'attente, et j'ai envoyé des mots de passe aléatoires. A chaque fois, je me fais kick instantanément. Dans le désespoir, j'envoie la citation du jour, et là : **une seconde d'attente** avant le kick.
J'essaie de comprendre ce qui a changé, entre les mots de passe aléatoires et cette phrase : je rajoute des lettres, j'en enlève, j'en modifie... Jarrive à la conclusion que **seul le `T` du début** provoque ce délai.
C'est ici que j'ai compris que chaque lettre correcte supplémentaire allait allonger le délai, et je suis parti sur un script python.

On laisse tourner le script, et au bout de quelques minutes (et 6 caractères trouvés) le serveur me répond **avec le flag !**
