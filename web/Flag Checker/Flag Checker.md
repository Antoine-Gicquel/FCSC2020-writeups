# Flag Checker

**200 points**

## Enoncé

Voici un service qui permet simplement de vérifier si le flag est correct.

## Ma solution

Par automatisme, je lance Burp en lançant le challenge. Je tente quelques flags, mais ne capture aucune requête. *"Ah tiens, de la déobfuscation JS ?"*
Je regarde le js, tout est clair. Je tombe sur une fonction cwrap, et après quelques recherches Google je comprends qu'il s'agit d'une fonction en **WebAssembly**.
Je regarde donc le fichier `index.wasm`, au bas duquel je trouve une chaine ressemblant fortement à un flag chiffré : *70 caractères, avec le 2ème et le 4ème égaux...*

Je me dis ensuite que je vais débugger le .wasm pour trouver comment déchiffrer le flag. Avec des breakpoints dans la fonction 4, je vois que chacun des caractères que j'ai renté est XORé avec 3. Je ne tilt que quelques minutes plus tard : `'F' XOR 3 = 'E'`, `'C' XOR 3 = '@'`, ...

J'écris donc 3 lignes de pthon pour afficher le résultat d'une telle opération, qui me **donne le flag !**
