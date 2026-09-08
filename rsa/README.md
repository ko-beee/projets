# RSA — de l'arithmétique au chiffrement

Implémentation de RSA à partir de zéro, sans bibliothèque de cryptographie, puis
étude expérimentale du coût de l'attaque par factorisation.

L'objectif n'est pas de produire du chiffrement utilisable — il ne faut jamais
utiliser une implémentation maison en production — mais de comprendre pourquoi
RSA tient : non pas sur un secret, mais sur un écart de difficulté entre deux
opérations arithmétiques.

## État d'avancement

| Étape | Contenu | État |
|---|---|---|
| 1 | Exponentiation modulaire rapide | fait |
| 2 | Algorithme d'Euclide étendu | fait |
| 3 | Test de primalité | fait |
| 4 | Génération de clés, chiffrement, déchiffrement | à faire |
| 5 | Attaque par factorisation et mesure du coût | à faire |

## Étape 1 — Exponentiation modulaire rapide

### Le problème

Calculer `a^b mod n`. La difficulté n'est pas le modulo, qui s'écrit en un
caractère, mais le fait qu'en RSA l'exposant `b` fait couramment 2048 bits.
Former `a**b` puis réduire produirait un nombre de plusieurs centaines de
milliers de chiffres : impossible en pratique.

La contrainte est donc que **les nombres manipulés restent petits à chaque
instant du calcul**, jamais seulement à la fin.

### Ce que j'ai construit

Plutôt que d'élever au carré successivement, l'algorithme construit une suite
d'exposants dans laquelle chaque terme est la somme de deux termes déjà
atteints, jusqu'à obtenir `b` exactement. En parallèle, il maintient les
puissances correspondantes de `a`, réduites modulo `n` à chaque ajout.

Cette structure s'appelle une **chaîne d'additions**. Je l'ai retrouvée sans
la connaître, en cherchant à minimiser le nombre de multiplications sur papier.
Déterminer la plus courte chaîne d'additions menant à un entier donné est un
problème réputé difficile ; ma version est *gloutonne* — elle retient le premier
pas valable, pas le meilleur.

### Vérification

Python fournit `pow(a, b, n)`, qui fait exactement ce calcul. Il n'est pas
utilisé dans l'implémentation, seulement comme référence de test :

```python
for _ in range(1000):
    a = random.randint(2, 10**6)
    b = random.randint(2, 10**6)
    n = random.randint(2, 10**6)
    assert exponentiation_modulaire(a, b, n) == pow(a, b, n)
```

Les mille tirages passent.

**Ce que ce test ne voyait pas.** Il tire `b` à partir de 2. Un balayage
exhaustif des exposants de 0 à 299 a révélé une seule erreur, toujours la
même : `b = 0` renvoyait `a mod n` au lieu de 1. Corrigé.

La leçon vaut d'être notée : un test aléatoire ne couvre que ce qu'il tire.
Les cas limites — 0, 1, la borne supérieure — se testent explicitement.

### Coût mesuré

La contrainte de taille est respectée. Avec `n` de l'ordre de 10⁵, le plus
grand entier manipulé pendant tout le calcul fait **33 bits**, quelle que soit
la taille de l'exposant.

En revanche, le caractère glouton de la chaîne a un prix. Comparaison avec
l'exponentiation binaire classique :

| Exposant | Chaîne gloutonne | Exponentiation binaire |
|---|---|---|
| 100 | 11 multiplications, 12 valeurs stockées | 8 multiplications, 2 variables |
| 10³ | 20 multiplications, 21 valeurs stockées | 14 multiplications, 2 variables |
| 10⁶ | 73 multiplications, 74 valeurs stockées | 25 multiplications, 2 variables |
| 2³² | 264 multiplications, 265 valeurs stockées | 32 multiplications, 2 variables |
| 2⁶⁴ | 2 163 multiplications, 2 164 valeurs stockées | 64 multiplications, 2 variables |

### Limites connues

L'écart avec la méthode binaire se creuse avec la taille de l'exposant, et la
consommation mémoire croît linéairement avec le nombre d'étapes puisque toutes
les valeurs intermédiaires sont conservées. Sur un exposant de taille RSA
réelle, cette implémentation serait inutilisable.

Une version à deux variables, sans stockage, reste à écrire. Elle sera reprise
à l'étape 5, quand la mesure du coût de l'attaque rendra la différence visible.

## Faire tourner les tests

```
python rsa/arithmetique.py
```

## Ce que j'ai appris

Que la difficulté d'un problème n'est pas toujours là où on la cherche : mes
deux premières tentatives portaient sur la nature arithmétique des nombres,
alors que tout se jouait dans la structure du calcul.

Et qu'un programme juste n'est pas nécessairement un programme utilisable.
Celui-ci passe tous les tests et reste inexploitable à l'échelle réelle.

## Étape 2 - euclide étendu & inverse modulaire

### Ce que fait la fonction
La fonction doit permettre de trouver le PGCD de deux nombres `a` et `b`
 et de trouver les deux coefficients `u` et `v` tels que `a*u+b*v=PGCD(a,b)`

### La formule qui n'existait pas

Tout d'abord, j'ai cherché une formule finale après la boucle `while` pour
 trouver `u` et `v`. J'avais créé une liste de coefficients `q` et de restes `r`.

Mais après plusieurs essais non concluants, j'ai essayé avec une autre perspective.

J'ai cherché à quoi correspond `r(n)` par rapport à `r(n-1)` et `n(-2)`. Soit

`r.append(r(-2)-r(-1)*q(-1))` et après plusieurs fausses pistes comme remonter
 à `r(2)` en partant de `r[-1]` en créant une nouvelle boucle `for` après, à la
suite, j'ai fait l'inverse. J'ai donc finalement trouvé que c'est une récurrence
avec tout simplement `v.append(v(-2)-v(-1)*q(-1))` et pareil pour `u`. Finalement,
j'ai supprimé les listes inutiles par des variables et utilisé cet idiome nouveau
pour moi : `u1, u2 = u2 - u1*q, u1` pour supprimer les variables temporaires.

### Le piège du q[3]=1

Ma fonction fonctionnait dès que q[3]=1. Elle renvoyait les bons `u` et `v`.

Mais lorsque j'ai effectué un balayage, ça bloquait. Donc maintenant, je teste
 des valeurs "extrêmes" `a=0`, `n=2`, `a>=n`.

## Étape 3 — la génération des clés

### fonction est_premier

Je devais construire une fonction qui prouvait qu'un nombre n'était pas premier grâce
au petit théorème de Fermat, en utilisant ma fonction exponentiation_modulaire. On entre
le nombre dont on cherche à savoir s'il est premier ou pas, p, et le nombre de tests
qu'on va effectuer sur ce nombre. En effet, si le nombre qu'on trouvait était différent
de 1, p n'était pas premier.

Cela fonctionnait très bien sauf pour les nombres de Carmichael, comme
1 042 789 205 881 = 5581 × 11161 × 16741, déclaré premier 99 fois sur 100 par Fermat.
Les nombres de Carmichael ayant de grands facteurs premiers sont presque toujours
déclarés premiers par ce test. En dessous de 50 000, leurs facteurs sont assez petits
pour qu'un témoin tiré au hasard en partage souvent un : Fermat les attrape alors, mais
par ce biais et non par le théorème.

C'est pour ça que j'ai utilisé l'idée de Miller-Rabin. Elle part du lemme suivant :
modulo un nombre premier, 1 n'a que deux racines carrées, 1 et −1. L'idée utilise la
décomposition de p−1 en d × 2^s, avec d un nombre impair. L'objectif est donc maintenant
de parcourir les `exponentiation_modulaire(a, b, p)` de b = d jusqu'à b = p−1 = d × 2^s,
pour chaque test. Si on détecte que l'exponentiation modulaire d'un rang n est différente
de 1 et de p−1, et que celle du rang n+1 vaut 1, alors p n'est pas premier. C'est
exactement ce que nous dit l'idée de Miller-Rabin. Le même nombre 1 042 789 205 881 est
alors déclaré premier 0 fois sur 100.

Avec la seule idée de Miller-Rabin, le test donnait 17 107 faux positifs : quand la suite
n'atteint jamais 1, il n'y a aucune racine carrée à examiner, donc rien à rejeter — 9
était déclaré premier. J'ai donc ajouté un test final sur le dernier terme de la suite,
qui doit valoir 1 : c'est le test de Fermat, remis en garde-fou.

Finalement, le programme donne 0 faux négatif et 0 faux positif pour p de 3 à 50 000,
0/100 sur les 15 nombres de Carmichael testés, et 0 désaccord avec sympy sur 300 nombres
de 61 bits. Ces tests prouvent que p n'est pas premier ; l'inverse ne fonctionne pas.

### fonction exponentiation_rapide

Ma fonction exponentiation_modulaire était trop lente pour un exposant de 512 bits. De
plus, la mémoire de ma machine ne suffisait même pas. Une méthode plus efficace pour
calculer une exponentiation modulaire est de la calculer à l'aide de l'écriture binaire
de b.
```
 bits | multiplications | log2(b)
   20 |              75 |      20
   40 |             522 |      40
   60 |           2 064 |      60
  100 |          16 504 |     100
  140 |         131 091 |     140
  180 |         524 413 |     180
  200 |       1 048 809 |     200
```
Dans ce tableau, la colonne « multiplications » donne le nombre de multiplications
nécessaires pour un exposant de cette taille avec la première méthode, et la colonne
« log2(b) » avec la seconde.

Par exemple, pour 200 bits, la première méthode prenait 1,3871 s et la nouvelle
seulement 0,0002 s, soit un écart d'un facteur 7000.

Je garde cette fonction inutilisée car elle témoigne de mon raisonnement : j'étais allé
intuitivement dans cette direction avant de chercher autre chose.

### fonction generer_premier(bits)

Cette fonction doit générer un nombre premier d'un certain nombre de bits. C'est pourquoi
l'intervalle aléatoire dans lequel le nombre est choisi est primordial. Cet intervalle est
tout simplement [2^(bits−1), 2^bits − 1] : un nombre choisi dedans aura donc exactement
bits bits. Ensuite il suffit d'utiliser la fonction est_premier pour vérifier, et s'il ne
l'est pas, d'en choisir un autre aléatoirement.

On peut même utiliser le théorème des nombres premiers pour estimer le nombre d'appels à
est_premier. Pour bits = 512, ln(2^512) vaut environ 355 candidats. Or on ne choisit que
des nombres impairs (car 2 est le seul nombre premier pair), et on appellera donc en
moyenne 178 fois est_premier avant d'en trouver un pour 512 bits. J'ai lancé le programme
et trouvé en moyenne 164 candidats impairs testés sur 100 tirages écart cohérent avec la variance.

### fonction generer_cles

Cette fonction est le cœur du fonctionnement de RSA, car c'est elle qui crée les clés
publique et privée. Elle utilise toutes les fonctions précédentes. Elle génère d'abord
deux nombres premiers p et q (non égaux), puis calcule phi = (p−1)(q−1). À partir de là,
un nombre e est choisi aléatoirement et on génère son inverse modulo phi ; en réalité il
doit souvent être rechoisi, car tous les nombres n'ont pas d'inverse modulo phi.

Pourquoi modulo phi ? Tout simplement parce que `m^phi ≡ 1 [n]` lorsque m est premier
avec n, et que si `e*d ≡ 1 [phi]`, alors `m^(e*d) ≡ m [n]`. Ce sont les clés publique
(n, e) et privée (n, d).

Pour chiffrer un nombre, il suffit d'utiliser la fonction chiffrement avec le nombre et
la clé publique. Cette fonction utilise simplement exponentiation_rapide, et pour le
déchiffrement c'est le même principe et la même fonction qui est appelée. Les tests
effectués montrent que 10 clés de 512 bits sont générées en 5,22 s, avec 200
chiffrements/déchiffrements corrects par taille, de 32 à 512 bits.

Avant d'arriver là, ma fonction passait tous les tests alors qu'elle ne chiffrait rien
du tout : les clés ne modifiaient pas le message. C'est le même problème que pour q3, où
mon code passait les tests sans être utilisable. La réaction a été d'ajouter un test qui
vérifie que le message chiffré est bien différent du message clair.