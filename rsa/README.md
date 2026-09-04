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
| 2 | Algorithme d'Euclide étendu | à faire |
| 3 | Test de primalité | à faire |
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
La fonction doit permettre de trouver le PGCD de deux nombres `a` et `b` et de trouver les deux coefficients `u` et `v` tels que `a*u+b*v=PGCD(a,b)`

### La formule qui n'existait pas

Tout d'abord, j'ai cherché une formule finale après la boucle `while` pour trouver `u` et `v`. J'avais créé une liste de coefficients `q` et de restes `r`.

Mais après plusieurs essais non concluants, j'ai essayé avec une autre perspective.

J'ai cherché à quoi correspond `r(n)` par rapport à `r(n-1)` et `n(-2)`. Soit

`r.append(r(-2)-r(-1)*q(-1))` et après plusieurs fausses pistes comme remonter à `r(2)` en partant de `r[-1]` en créant une nouvelle boucle `for` après, à la suite, j'ai fait l'inverse. J'ai donc finalement trouvé que c'est une récurrence avec tout simplement `v.append(v(-2)-v(-1)*q(-1))` et pareil pour `u`. Finalement, j'ai supprimé les listes inutiles par des variables et utilisé cet idiome nouveau pour moi : `u1, u2 = u2 - u1*q, u1` pour supprimer les variables temporaires.

### Le piège du q[3]=1

Ma fonction fonctionnait dès que q[3]=1. Elle renvoyait les bons `u` et `v`.

Mais lorsque j'ai effectué un balayage, ça bloquait. Donc maintenant, je teste des valeurs "extrêmes" `a=0`, `n=2`, `a>=n`.
