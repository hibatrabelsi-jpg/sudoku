from sudoku_grid import SudokuGrid
import time

# 1. Chargement
grid = SudokuGrid('grille1.txt')
print("--- Grille Initiale ---")
grid.display_terminal()

# 2. Tentative d'élimination logique (Bonus Personne A)
print("\n--- Nettoyage par élimination logique ---")
while grid.solve_logic_elimination():
    print("Une case remplie logiquement...")
grid.display_terminal()

# 3. Résolution par Force Brute (Sujet Personne A)
print("\n--- Résolution par Force Brute ---")
start = time.time()
success, total_tries = grid.solve_brute_force()
end = time.time()

if success:
    print(f"Réussi en {total_tries} itérations ({end-start:.2f}s) !")
    grid.display_terminal()
else:
    print("La force brute a échoué ou a atteint la limite.")