# Merry

**500 points**

## Enoncé

Un serveur a été conçu pour utiliser un algorithme d'échange de clés avec ses clients. Cet algorithme génère et garde le même bi-clé pour plusieurs requêtes. Il notifie aussi ses clients quand l'échange a échoué et que la clé partagée n'est pas la même. Votre but est de retrouver la clé secrète du bi-clé généré par le serveur.

## Ma solution

Le principal problème dans ce challenge réside dans la fonction `__decode`.
Pour simplifier les équations, on peut essayer de lui passer une matrice `C - U * S`
qui n'aura pas besoin de se faire recentrer (pour l'instant ce n'est qu'une idée,
on verra cela concrètement plus tard).
Il apparait aussi intéressant que `C - U * S` ait tous ses coefficients entre 0 et
q - 1 pour qu'elle ne soit pas affectée par le modulo.
En conclusion, on voudrait avoir `C - U * S` qui a tous ses coefficients entre 0 et
q/2, pour que `__decode` applique juste la division par q/4 (et l'arrondi)


Ainsi, la fonction `check_exchange` deviendrait :
`(C - U*S) * 4/q == key_b ?`

On aimerait pouvoir extraire de l'information sur `S` à partir de cette question.
L'idée est de rendre `U * S` très simple, en mettant tous les coefficients de `U` à 0,
sauf un (à la première ligne, colonne j) qui serait non nul, posons le égal à k.
Ainsi, le résultat de `U * S` serait une matrice 4 * 4 dont tous les coefficients
seraient nuls excepté la première ligne, qui contient `k * [S]j` (la ligne j de S).
Mais là, premier problème : `S` contient des coefficients positifs comme négatifs,
et dans les conditions de nos simplifications on ne voulait que des coefficients
positifs ! On est donc contraints de contrebalancer ces derniers dans `C`
On va donc poser `C`, nulle partout sauf à la première ligne, `(k k k k)`.
Ainsi, C - U*S contiendra :
- des 0 sur les lignes 2 et suivantes
- les valeurs 0, k ou 2k à la première ligne correspondant aux 1, 0, -1
(respectivement) de `S`

*Bien, on est pas mal avancés !* Rappelons nous maintenant des contraintes associées
à la fonction `__decode`. Pour que nos simplifications soient valides, il faut que
`C - U * S` ait ses coefficients entre 0 et q/2
Notre k est tout choisi ! `2k = q/2 <=> k = q/4`

Ainsi `__decode(C - U*S)` contient les valeurs 0, 1 ou 2, correspondant aux valeurs
1, 0, et -1 (respectivement) de la ligne j de `S`.

On va maintenant faire une boucle (indicée sur j), qui tournera autant de fois
qu'il y a de lignes dans S.
Chaque tour de boucle sera chargé de trouver une ligne de `S`. Pour cela, on va
envoyer au serveur les paramètres `C` et `U` déterminés précédemment, et on va les
tester contre toutes les matrices nulles aux lignes 2 et suivantes, et qui
contiennent un élément de `{0, 1, 2} ^ 4` à la première ligne
La réponse du serveur ne sera positive que pour une de ces matrices, et on a
ainsi déterminé la ligne j de `S` (cf paragraphe du dessus)

Une fois S reconstitué, on applique juste `((B - A*S) % q + 1) % q - 1` (les
modulos q +-1 sont simplement là pour transformer les 2047 en -1) pour trouver `E`.

On envoie cela au serveur, et **c'est gagné !**
