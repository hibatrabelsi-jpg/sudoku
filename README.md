# Sudoku Solver

Outil de resolution de Sudoku developpé en Python, comparant deux approches algorithmiques : la **force brute** et le **backtracking**. Le projet inclut une interface graphique Pygame avec visualisation en temps réel, un mode jeu interactif, et une persistance MySQL.

## Contexte du projet

Le Sudoku est un jeu de réflexion sur une grille 9x9 divisee en neuf sous-grilles 3x3. L'objectif est de remplir chaque case avec un chiffre de 1 à 9, sans répétition dans une même ligne, colonne ou sous-grille. Ce projet explore deux stratégies de résolution pour étudier la complexité algorithmique et comparer leurs performances.

## Algorithmes implementes

### Force Brute

La force brute génere systematiquement toutes les combinaisons possibles de chiffres pour les cases vides. Elle ne verifie la validité de la grille qu'une fois toutes les cases remplies. Si la combinaison est invalide, elle passe à la suivante.

**Complexité théorique : O(9^n)** ou n est le nombre de cases vides. Pour une grille avec 45 cases vides, cela represente potentiellement 9^45 combinaisons, soit environ 10^42 possibilites. En pratique, l'algorithme atteint sa limite d'iterations bien avant de trouver une solution.

### Backtracking

Le backtracking procède case par case. Pour chaque case vide, il essaie les chiffres de 1 à 9 et vérifie immédiatement si le chiffre respecte les règles du Sudoku (ligne, colonne et carre 3x3). Si un chiffre est valide, il passe à la case suivante. Si aucun chiffre ne convient, il revient a la case precedente et essaie le chiffre suivant. Ce processus de retour en arriere (backtrack) est répeté jusqu'à la résolution complete.

**Complexité théorique : O(9^n)** dans le pire cas, mais en pratique bien inferieure grâce à l'élagage. Chaque vérification immédiate élimine des branches entieres de l'arbre de recherche, reduisant considerablement l'espace exploré.

### Différence fondamentale

La force brute remplit d'abord, vérifie ensuite. Le backtracking vérifie d'abord, remplit ensuite. Cette difference dans l'ordre des opérations est ce qui rend le backtracking exponentiellement plus rapide en pratique.

## Analyse comparative

### Tableau comparatif sur les 5 grilles

| Grille | Cases vides | Méthode | Resultat | Itérations | Vérifications | Backtracks | Temps | Mémoire |
|--------|-------------|---------|----------|------------|---------------|------------|-------|---------|
| Grille 1 | 45 | Backtracking | Résolu | 2 099 | 2 099 | 209 | 104.1 ms | 968.4 Ko |
| Grille 1 | 45 | Force Brute | Limite atteinte | 500 328 | 444 408 | — | 18.970 s | 102.46 Mo |
| Grille 2 | 52 | Backtracking | Résolu | 12 123 | 12 123 | 1 316 | 882.2 ms | 5.50 Mo |
| Grille 2 | 52 | Force Brute | Limite atteinte | 500 382 | 444 402 | — | 19.581 s | 102.45 Mo |
| Grille 3 | 43 | Backtracking | Résolu | 866 | 866 | 74 | 49.0 ms | 391.4 Ko |
| Grille 3 | 43 | Force Brute | Limite atteinte | 500 310 | 444 410 | — | 19.202 s | 102.45 Mo |
| Grille 4 | 57 | Backtracking | Résolu | 64 503 | 64 503 | 7 134 | 3.859 s | 29.34 Mo |
| Grille 4 | 57 | Force Brute | Limite atteinte | 500 427 | 444 397 | — | 20.823 s | 102.45 Mo |
| Grille 5 | 58 | Backtracking | Résolu | 38 133 | 38 133 | 4 204 | 2.227 s | 17.34 Mo |
| Grille 5 | 58 | Force Brute | Limite atteinte | 500 436 | 444 396 | — | 20.401 s | 102.45 Mo |

### Ratios de performance (Force Brute / Backtracking)

| Grille | Cases vides | Itérations | Vérifications | Temps | Memoire |
|--------|-------------|------------|---------------|-------|---------|
| Grille 1 | 45 | x238.4 | x211.7 | x182.3 | x108.3 |
| Grille 2 | 52 | x41.3 | x36.7 | x22.2 | x18.6 |
| Grille 3 | 43 | x577.7 | x513.2 | x391.6 | x268.1 |
| Grille 4 | 57 | x7.8 | x6.9 | x5.4 | x3.5 |
| Grille 5 | 58 | x13.1 | x11.7 | x9.2 | x5.9 |

### Etude de la complexité

#### Complexité temporelle

Les deux algorithmes ont une complexité théorique de **O(9^n)**, mais leurs comportements pratiques sont radicalement differents.

La force brute atteint systematiquement la limite de 500 000 iterations sur les 5 grilles testees, sans jamais trouver de solution. Son temps d'exécution est quasi constant autour de 19-20 secondes, independamment de la difficulte de la grille. Cela s'explique par le fait qu'elle explore aveuglément l'espace de recherche sans aucune strategie d'élagage.

Le backtracking, en revanche, montre une variation significative selon la difficulté : de 49 ms (Grille 3, 43 cases vides) a 3.8 secondes (Grille 4, 57 cases vides). Cette variation illustre l'impact de l'elagage : chaque verification immediate élimine des branches entières, et l'éfficacite de cet élagage dépend de la structure de la grille.

#### Complexité spatiale

La force brute consomme systematiquement environ 102 Mo de memoire, quelle que soit la grille. Le backtracking va de 391 Ko (Grille 3) à 29 Mo (Grille 4), soit un ratio de x3.5 a x268 selon les cas.

### Observations

1. **La force brute est inutilisable en pratique.** Sur les 5 grilles testees, elle n'a jamais trouvé de solution dans la limite de 500 000 iterations. Pour une grille avec 45 cases vides, il faudrait potentiellement explorer 9^45 combinaisons, ce qui est physiquement impossible.

2. **Le backtracking resout toutes les grilles.** Même la Grille 4 (57 cases vides, la plus difficile) est résolue en 3.8 secondes avec 64 503 itérations. La Grille 3 (43 cases vides) est résolue en seulement 49 ms avec 866 itérations.

3. **Le nombre de cases vides n'est pas le seul facteur de difficulté.** La Grille 3 (43 cases vides) est résolue plus vite que la Grille 1 (45 cases vides), et la Grille 5 (58 cases vides) est résolue plus vite que la Grille 4 (57 cases vides). La disposition des chiffres dans la grille influence fortement le nombre de backtracks necessaires.

4. **Les ratios varient enormement.** De x5.4 (temps, Grille 4) a x577.7 (iterations, Grille 3). Plus la grille est facile pour le backtracking, plus l'écart avec la force brute se creuse.

5. **La mémoire suit la même tendance.** Le backtracking utilise la mémoire de maniere proportionnelle à sa progression (snapshots de la grille à chaque étape), tandis que la force brute sature la mémoire de maniere constante.

### Conclusion sur l'algorithme le plus performant

Le **backtracking** est indiscutablement l'algorithme le plus performant pour la resolution de Sudoku. Il surpasse la force brute sur tous les criteres mesures : itérations, vérifications, temps d'exécution et mémoire.

La clé de sa superiorite réside dans la verification immédiate à chaque placement. En detectant les conflits dès qu'un chiffre est placé, le backtracking évite d'explorer des millions de combinaisons vouées à l'echec. La force brute, en remplissant d'abord et en vérifiant ensuite, gaspille la quasi-totalité de son temps de calcul sur des combinaisons invalides.

En resumé : la verification précoce et le retour en arriere (backtrack) transforment un problème theoriquement exponentiel en un probleme résolvable en quelques millisecondes.

## Technologies et outils utilises

- **Python 3** — langage principal
- **Pygame** — interface graphique (menu, replay, mode jeu, comparaison)
- **MySQL** — persistance des résultats et historique des résolutions
- **tracemalloc** — mesure de la consommation memoire
- **time** — mesure du temps d'execution
- **copy (deepcopy)** — snapshots de la grille pour le replay

## Structure du projet

```
sudoku-solver/
    sudoku_grid.py        # Classe SudokuGrid (parsing, algos, metriques)
    main.py               # Point d'entrée terminal + lancement Pygame
    database.py           # Persistance MySQL et export Markdown
    test_mvp1.py          # Tests de verification
    data/                 # 5 grilles de Sudoku du sujet
        grille1.txt ... grille5.txt
        setup_db.sql
    assets/fonts/         # Polices personnalisées
    gui/                  # Interface Pygame
        app.py            # Boucle principale et navigation
        constants.py      # Design system (couleurs, spacing, polices)
        fonts.py          # Chargement des polices
        components.py     # Boutons, labels
        grid_view.py      # Affichage de la grille
        menu.py           # Menu principal avec apercu
        resolve_screen.py # Ecran de résolution
        replay_view.py    # Replay avec dashboard en direct
        stats_view.py     # Comparaison avec ratios animés
        play_view.py      # Mode jeu interactif
```

## Utilisation

```bash
# Installer les dependances
pip install pygame mysql-connector-python

# Lancer avec une grille
python main.py data/grille1.txt

# Lancer directement l'interface
python -c "from gui.app import launch; launch()"
```

## Veille technologique

La recherche effectuee pour ce projet a couvert plusieurs domaines :

**Algorithmique et complexite** : etude des notations Big O (O(1), O(log n), O(n), O(n^2), O(2^n)), comprehension du comptage d'operations (affectation, comparaison, acces memoire), et application au cas specifique du Sudoku ou la complexite depend du probleme et non du developpeur.

**Strategies de resolution de Sudoku** : au-dela de la force brute et du backtracking, il existe des approches comme l'elimination par contraintes (approche humaine), la propagation de contraintes (algorithme de Peter Norvig), et les algorithmes de type Dancing Links (DLX) de Donald Knuth. Ces approches n'ont pas ete implementees mais ont nourri notre comprehension du probleme.

**Sources consultees** :
- Backtracking — Wikipedia : principes generaux de l'algorithme de retour sur trace
- Brute Force Algorithms : introduction aux algorithmes exhaustifs et leurs limites
- Calcul de complexite, pour quoi faire ? : pedagogie sur la notation Big O et son utilite pratique
- Pygame — Getting Started : documentation officielle pour l'interface graphique
- Peter Norvig — Solving Every Sudoku Puzzle : approche par propagation de contraintes

## [![Réalisé par](https://img.shields.io/badge/R%C3%89ALIS%C3%89-PAR-orange?style=for-the-badge)](https://forthebadge.com)

**Assmine AHAMADA** | **Hiba Trabelsi** | **Noémie FERAUD**