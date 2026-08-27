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
- Chemins d'accès aux images et à la carte rendus relatifs au fichier
  (`Path(__file__).parent`) et non plus au dossier de lancement : le jeu
  plantait dès qu'on l'exécutait depuis ailleurs.
- Suppressions des variables 'perso[objet]' pour aléger le code et moins de 
  confusion car si `perso[objet][...]=True == objet[...][perso]=True`
- Simplification des calculs pour savoir quand afficher l'objet, permettant 
  ainsi de ne pas les affichers en dehors du cadre


### 4. Séparation de l'état et de l'affichage

La logique de jeu vivait dans les fonctions d'affichage : `dessinerMonde`
déterminait si le personnage était sur l'eau ou en montagne, `dessinerObjets`
gérait le ramassage. Comme ces fonctions s'exécutaient après `deplacerPerso`
dans la boucle, le blocage se décidait sur un état vieux d'une image : le
personnage apparaissait brièvement sur le terrain interdit avant d'être
renvoyé au point de départ.

Une première tentative consistait à appeler `persobloquer()` depuis l'intérieur
de `dessinerMonde`, avec un `return` immédiat. Le décalage disparaissait, mais
la moitié de la carte n'était alors plus dessinée pour cette image.

La correction retenue est une fonction `majEtat()`, appelée avant tout
affichage, qui met à jour l'état du personnage et des objets. Elle calcule
directement la case occupée à partir de `debutcarte` et de la position du
personnage, au lieu de parcourir toute la zone visible pour la retrouver.
Les fonctions de dessin ne font plus que dessiner.

Un `screen.fill()` a été ajouté en début d'image. Il manquait depuis le début :
le programme ne fonctionnait que parce que les tuiles repeignaient par hasard
la totalité de la zone de jeu.

## Limites connues

La refonte de la section 4 a été écrite et relue, mais pas encore exécutée :
la bibliothèque pygame ne peut pas se charger sur la machine de développement
actuelle, une politique de sécurité du système bloquant ses fichiers compilés.
La vérification à l'exécution reste donc à faire.