# Le meilleur des mondes

Jeu d'exploration en Python et pygame.

La carte est stockée dans un fichier CSV où chaque chiffre désigne un type de
terrain : mer, prairie, champ, forêt, montagne. Le personnage reste au centre
de l'écran et c'est le monde qui défile autour de lui.

Trois objets sont disséminés sur la carte et modifient ce qu'on peut faire :
le bateau permet de traverser la mer, les chaussures de franchir la montagne,
l'épée change l'apparence du personnage. Sans l'objet correspondant, entrer
sur un terrain interdit renvoie au point de départ.

## Faire tourner le projet

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pygame-ce
python monde.py
```

Sur macOS ou Linux, remplacer la deuxième ligne par `source .venv/bin/activate`.

Déplacements aux flèches du clavier.

**Note :** on installe `pygame-ce` et non `pygame`. Le projet pygame d'origine
n'est plus maintenu depuis septembre 2024 et ne s'installe pas sur les versions
récentes de Python ; `pygame-ce` est le fork maintenu par une grande partie de
l'équipe initiale et s'importe sous le même nom.

## Reprise et corrections — août 2026

Projet écrit en première, en spécialité NSI (2024-2025), repris un an plus tard
pour être relu et corrigé. Deux bugs trouvés, dont l'un masquait l'autre.

### 1. Bornes de déplacement croisées

La carte est une liste de lignes, et l'accès se fait par `carte[ligne][colonne]`.
Donc `len(carte)` compte les lignes et `len(carte[0])` les colonnes.

Or les gardes de `deplacerPerso` bornaient l'indice de ligne avec le nombre de
colonnes, et l'indice de colonne avec le nombre de lignes. Les deux étaient
inversés.

L'erreur restait invisible sur une carte à peu près carrée. Sur `carte.csv`,
plus large que haute, elle permettait de dépasser la dernière ligne.

### 2. Ligne fantôme à la lecture du CSV

`lire_fichier` découpait le contenu du fichier avec `split('\n')`. Comme un
fichier texte se termine par un retour à la ligne, la dernière entrée produite
était une chaîne vide, et `''.split(';')` renvoie une liste d'un seul élément.

Sur un fichier de 3 lignes de 3 cases, `len(carte)` valait donc 4, et la
dernière « ligne » n'avait qu'une case. Y accéder provoquait un `IndexError`.

Corrigé avec `splitlines()`, qui ne produit pas d'élément vide final et gère
également les fins de ligne Windows, complété par un filtre sur les lignes vides.

### 3. Autres corrections

- Le bateau ne s'affichait que d'après le terrain, sans vérifier qu'il avait
  été ramassé
- `perso["eau"]` n'existait qu'une fois `dessinerMonde` passé sur la case du
  personnage ; les états sont maintenant initialisés dans `creerPerso`
- Taille de la fenêtre et limites d'affichage calculées à partir d'une seule
  constante au lieu d'être écrites en dur
- `positionX` et `positionY` renommés en `positionColonne` et `positionLigne`,
  avec la convention des indices documentée en commentaire
- Suppression de variables calculées mais jamais utilisées

## Ce qu'il reste à faire

La logique de jeu vit encore dans les fonctions d'affichage : `dessinerMonde`
décide si le personnage est sur l'eau ou en montagne, `dessinerObjets` gère le
ramassage. Comme ces fonctions s'exécutent après `deplacerPerso`, le blocage
est détecté avec une image de retard et le personnage apparaît brièvement sur
le terrain interdit avant d'être renvoyé au départ.

La prochaine étape est de séparer la mise à jour de l'état et l'affichage.

Restent aussi à nettoyer : les compteurs `r` et `c` de `dessinerMonde`,
incrémentés mais jamais lus, et une condition toujours vraie par construction
puisque les indices proviennent déjà d'un `range` sur le même intervalle.