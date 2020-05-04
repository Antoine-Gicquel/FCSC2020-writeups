# Pippin

**200 points**

## Enoncé

Après avoir constaté que le serveur précédent était vulnérable à des attaques, les concepteurs ont modifié leur algorithme en limitant le nombre de requêtes autorisées. Il semblerait cependant que certaines valeurs ne soient pas convenablement générées cette fois.

## Ma solution

On reprend le script de Merry, pour regarder les 30 premières lignes de `S`.
On remaque qu'il y a toujours deux 0, un 1 et un -1 sur chaque ligne.
On ne teste donc que les lignes de cette forme.
Dans le pire des cas, cela fait `280*(3+3+6) = 3360` requêtes, et en moyenne
`3360/2 = 1680`, ce qui est sous les 3000.

Effectivement, en lançant le script, **on obtient le flag !**
