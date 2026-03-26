# Projet Sudoku - Groupe [Ton Groupe]

## Force Brute et Élimination
Dans cette partie, nous avons mis en place la structure de base (POO) et deux méthodes de résolution :

1. Élimination Logique (Bonus) : Analyse chaque case et remplit celles qui n'ont qu'une seule possibilité. Très rapide mais limitée aux grilles simples.
2. Force Brute (Naïve)** : 
   - Principe : Teste chaque chiffre de 1 à 9 pour chaque case vide.
   - Complexité : $O(9^N)$ où $N$ est le nombre de cases vides.
   - Limites : Sur des grilles complexes, le nombre de combinaisons est trop élevé pour un ordinateur standard. C'est pourquoi nous avons implémenté un compteur d'itérations limité à 500 000.

Résultats sur grille1.txt : [Note ici le nombre d'itérations affiché par ton terminal]