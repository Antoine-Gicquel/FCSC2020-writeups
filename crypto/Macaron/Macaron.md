# Macaron

**200 points**

## Enoncé

Le but du challenge est de trouver une contrefaçon sur le code d'authentification de message Macaron.

## Ma solution

J'analyse le challenge, d'abord d'un point de vue haut niveau : on a 2 possibilités, tagger un message et vérifier si un couple (message, tag) est valide.
L'objet qui signe les messages dispose d'un compteur ctr ainsi que de 2 clés aléatoires k_1 et k_2, afin d'être certain de ne jamais chiffrer 2 fois le même message.

La signature se passe comme suit (de manière un peu réarrangée mais équivalente) :
- On ajoute un padding pour que la longueur du message soit un multiple de 60.
- On construit `B_i = message[30 * (i-1) : 30 * i]` et `n_i = ctr + (i-1)` pour tout i tel que B_i est défini.
- On calcule `H_i = HMAC(k_1, n_i B_i n_(i+1) B_(i+1), sha256)` pour tout i tel que H_i est défini.
- On calcule `H_1 XOR H_2 XOR H_3 XOR ...`
- On renvoie ce résultat, ainsi que la suite `n_1 n_2 n_3...`

Par la suite, on pourra noter sous la forme la forme `a A b B c C...` le message `ABC` associé aux nonces a, b, c

Pour valider le challenge, il faut arriver à **tagger un message soi-même**, à partir d'au maximum 32 messages taggés par le serveur.
Les premières idées qui me sont venues sont :

### Première option
**Se servir du padding** pour tagger un message A, puis proposer un message B (avec B != A) tel que B, une fois passé par le padding, soit égal à A, lui aussi passé par le padding.
J'aurais ainsi tag_hash(A) = tag_hash(B), et j'aurais réussi à tagger B.
Après quelques tentatives, je me rends compte que la tâche semble impossible.

### Deuxième option
Dans l'algorithme de vérification, **la taille du hash n'est pas correctement vérifiée**. Je me suis donc demandé si on pouvait exploiter cette erreur afin de tagger mon propre message, mais la réponse fut négative.

### Troisième option
Exploiter un **overflow du compteur**. Idée très vite abandonnée car produisant des blocs de 68 octets et non 64, trop bizarre.

### Quatrième option, qui mènera à la solution
J'utilise les propriétés du XOR, et plus particulièrement le fait que `A XOR A = 0`, quel que soit A. Aussi, j'utilise le fait que **les nonces** que l'on passe à l'algorithme de vérification **ne sont pas vérifiés**.
Ma première idée d'exploitation de cette piste était d'essayer de vérifier un message du type `n B n B n B n B`... afin d'obtenir un résultat nul. Ceci n'a pas été possible, le nombre de blocs étant pair et donc le nombre de XORs étant impair.
Ma seconde idée, qui fut la bonne : essayer de vérifier un message de la forme `0 B 0 B 0 B 1 B`. On aurait `tag_hash(BBBB, 0 0 0 1) = HMAC(0B0B) XOR HMAC(0B0B) XOR HMAC(0B1B) = HMAC(0B1B) = tag_hash(BB, 0 1)`.

Success !! J'ai juste à faire tagger `BB` (avec les nonces 0 et 1), puis d'envoyer pour vérification le message `BBBB`, avec les nonces 0,0,0,1 et le même hash que celui précédemment obtenu.
Ceci permet **l'obtention du flag !**
