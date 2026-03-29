import copy
import time
import tracemalloc


class SudokuGrid:
    """
    Classe principale pour la gestion et la resolution d'une grille de Sudoku.
    Contient le parsing, l'affichage, les algorithmes de resolution,
    la collecte de metriques et l'enregistrement de snapshots pour le replay.
    """

    def __init__(self, filename=None):
        self.grid = [[0] * 9 for _ in range(9)]
        self.initial_grid = [[0] * 9 for _ in range(9)]
        self.snapshots = []
        self.stats = {}
        self._reset_stats()

        if filename:
            self.load_file(filename)

    # =========================================================================
    # PARSING & GESTION DE LA GRILLE
    # =========================================================================

    def load_file(self, filename):
        """Importe et parse la grille depuis un fichier .txt"""
        self.grid = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = []
                for c in line:
                    if c == '_':
                        row.append(0)
                    elif c.isdigit() and c != '0':
                        row.append(int(c))
                if len(row) == 9:
                    self.grid.append(row)

        if len(self.grid) != 9:
            raise ValueError(f"La grille doit avoir 9 lignes, {len(self.grid)} trouvees.")

        self.initial_grid = copy.deepcopy(self.grid)
        self.snapshots = []
        self._reset_stats()

    def reset(self):
        """Remet la grille a son etat initial pour pouvoir relancer une autre methode"""
        self.grid = copy.deepcopy(self.initial_grid)
        self.snapshots = []
        self._reset_stats()

    def _reset_stats(self):
        """Reinitialise les compteurs de metriques"""
        self.stats = {
            "iterations": 0,
            "backtracks": 0,
            "verifications": 0,
            "temps_execution": 0.0,
            "memoire_max": 0,
            "cases_vides_initiales": self._count_empty(),
            "methode": ""
        }

    def _count_empty(self):
        """Compte le nombre de cases vides dans la grille actuelle"""
        count = 0
        for row in self.grid:
            for val in row:
                if val == 0:
                    count += 1
        return count

    def _find_empty_cells(self):
        """Retourne la liste des positions (row, col) des cases vides"""
        cells = []
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    cells.append((r, c))
        return cells

    def _record_snapshot(self, row, col, value, action):
        """
        Enregistre un snapshot complet pour le replay.
        Chaque snapshot contient une copie de la grille entiere,
        ce qui permet de naviguer librement dans le replay
        (avancer, reculer, sauter a n'importe quelle etape)
        sans avoir a recalculer depuis le debut.

        On limite a 50 000 snapshots max pour eviter de saturer
        la memoire (surtout avec la force brute qui fait des millions d'etapes).
        Pour le replay, 50 000 etapes c'est deja largement suffisant.
        """
        if len(self.snapshots) >= 50000:
            return

        self.snapshots.append({
            "etape": len(self.snapshots),
            "action": action,
            "ligne": row,
            "colonne": col,
            "valeur": value,
            "grille": copy.deepcopy(self.grid)
        })

    # =========================================================================
    # VERIFICATION
    # =========================================================================

    def is_valid(self, row, col, n):
        """
        Verifie si le chiffre n peut etre place a la position (row, col)
        sans violer les contraintes de ligne, colonne et carre 3x3.
        Incremente le compteur de verifications.
        """
        self.stats["verifications"] += 1

        # Verification de la ligne et de la colonne en un seul passage
        for i in range(9):
            if self.grid[row][i] == n:
                return False
            if self.grid[i][col] == n:
                return False

        # Verification du carre 3x3
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == n:
                    return False

        return True

    def is_grid_valid(self):
        """
        Verifie si la grille complete est valide.
        Utilisee par la force brute pour verifier une combinaison entiere.
        """
        self.stats["verifications"] += 1

        for i in range(9):
            row_set = set()
            col_set = set()
            for j in range(9):
                # Verification ligne
                val_row = self.grid[i][j]
                if val_row == 0:
                    return False
                if val_row in row_set:
                    return False
                row_set.add(val_row)

                # Verification colonne
                val_col = self.grid[j][i]
                if val_col in col_set:
                    return False
                col_set.add(val_col)

        # Verification des 9 carres 3x3
        for box_row in range(3):
            for box_col in range(3):
                box_set = set()
                for i in range(3):
                    for j in range(3):
                        val = self.grid[box_row * 3 + i][box_col * 3 + j]
                        if val in box_set:
                            return False
                        box_set.add(val)

        return True

    # =========================================================================
    # ALGORITHME 1 : FORCE BRUTE
    # =========================================================================

    def solve_brute_force(self, max_iterations=500000):
        """
        Resolution par force brute.

        Principe : on remplit les cases vides une par une avec des chiffres
        de 1 a 9 SANS verifier la validite a chaque placement.
        On verifie la grille complete seulement quand toutes les cases
        sont remplies. Si c'est invalide, on passe a la combinaison suivante.

        C'est volontairement "bete" et lent : c'est le but.
        La force brute ne reflechit pas, elle teste tout.
        """
        self.reset()
        self.stats["methode"] = "force_brute"
        empty_cells = self._find_empty_cells()
        self.stats["cases_vides_initiales"] = len(empty_cells)

        tracemalloc.start()
        start = time.perf_counter()
        success = self._brute_force_recursive(empty_cells, 0, max_iterations)
        self.stats["temps_execution"] = time.perf_counter() - start
        _, self.stats["memoire_max"] = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return success

    def _brute_force_recursive(self, empty_cells, index, max_iterations):
        """
        Parcours recursif pour la force brute.

        Difference fondamentale avec le backtracking :
        - On ne verifie JAMAIS is_valid pendant le remplissage
        - On verifie is_grid_valid seulement quand TOUTES les cases sont remplies
        - Si la grille complete est invalide, on revient et on essaye la combinaison suivante

        C'est ce qui la rend enormement plus lente que le backtracking :
        elle ne detecte les erreurs qu'a la fin, jamais en cours de route.
        """
        if self.stats["iterations"] >= max_iterations:
            return False

        # Toutes les cases sont remplies : on verifie la grille ENTIERE
        if index == len(empty_cells):
            return self.is_grid_valid()

        row, col = empty_cells[index]

        for n in range(1, 10):
            self.stats["iterations"] += 1

            # On place le chiffre SANS verifier (c'est ca la force brute)
            self.grid[row][col] = n
            self._record_snapshot(row, col, n, "placement")

            # On passe a la case suivante
            if self._brute_force_recursive(empty_cells, index + 1, max_iterations):
                return True

            # Cette combinaison n'a pas marche, on remet a zero
            self.grid[row][col] = 0
            self._record_snapshot(row, col, n, "retrait")

        return False

    # =========================================================================
    # ALGORITHME 2 : BACKTRACKING
    # =========================================================================

    def solve_backtracking(self):
        """
        Resolution par backtracking.

        Principe : on avance case par case, et a chaque placement on verifie
        IMMEDIATEMENT si le chiffre est valide. Si aucun chiffre ne marche,
        on revient en arriere (backtrack) et on essaye le chiffre suivant
        dans la case precedente.

        C'est beaucoup plus intelligent que la force brute car on detecte
        les erreurs tout de suite au lieu de remplir toute la grille pour rien.
        """
        self.reset()
        self.stats["methode"] = "backtracking"
        self.stats["cases_vides_initiales"] = self._count_empty()

        tracemalloc.start()
        start = time.perf_counter()
        success = self._backtracking_recursive()
        self.stats["temps_execution"] = time.perf_counter() - start
        _, self.stats["memoire_max"] = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return success

    def _backtracking_recursive(self):
        """
        Parcours recursif pour le backtracking.

        Difference fondamentale avec la force brute :
        - On verifie is_valid AVANT de placer un chiffre
        - Si le chiffre est invalide, on ne le place meme pas
        - On detecte les impasses immediatement au lieu de remplir toute la grille
        """
        # Trouver la prochaine case vide
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    # Essayer chaque chiffre de 1 a 9
                    for n in range(1, 10):
                        self.stats["iterations"] += 1

                        # Verification AVANT placement (c'est ca le backtracking)
                        if self.is_valid(r, c, n):
                            self.grid[r][c] = n
                            self._record_snapshot(r, c, n, "placement")

                            # Appel recursif pour la case suivante
                            if self._backtracking_recursive():
                                return True

                            # Ca n'a pas marche plus loin : on revient en arriere
                            self.stats["backtracks"] += 1
                            self.grid[r][c] = 0
                            self._record_snapshot(r, c, n, "retrait")

                    # Aucun chiffre ne marche pour cette case : impasse
                    return False

        # Plus de case vide : la grille est resolue
        return True

    # =========================================================================
    # AFFICHAGE
    # =========================================================================

    def display_terminal(self):
        """Affiche la grille dans la console avec distinction originaux/resolus"""
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("-" * 21)
            line = ""
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    line += "| "
                val = self.grid[r][c]
                if val == 0:
                    line += ". "
                elif self.initial_grid[r][c] != 0:
                    # Gras pour les chiffres de depart
                    line += f"\033[1m{val}\033[0m "
                else:
                    # Bleu pour les chiffres trouves par l'algorithme
                    line += f"\033[94m{val}\033[0m "
            print(line)

    # =========================================================================
    # METRIQUES & SNAPSHOTS
    # =========================================================================

    def get_stats(self):
        """Retourne une copie des statistiques de la derniere resolution"""
        return dict(self.stats)

    def get_snapshots(self):
        """Retourne la liste des snapshots pour le replay"""
        return list(self.snapshots)

    def display_stats(self):
        """Affiche les statistiques de la derniere resolution dans le terminal"""
        s = self.stats
        mem_kb = s['memoire_max'] / 1024
        mem_str = f"{mem_kb:.1f} Ko" if mem_kb < 1024 else f"{mem_kb/1024:.2f} Mo"

        print(f"\n--- Statistiques ({s['methode']}) ---")
        print(f"  Cases vides initiales : {s['cases_vides_initiales']}")
        print(f"  Iterations            : {s['iterations']}")
        print(f"  Verifications         : {s['verifications']}")
        if s['methode'] == 'backtracking':
            print(f"  Retours en arriere    : {s['backtracks']}")
        print(f"  Temps d'execution     : {s['temps_execution']:.6f} s")
        print(f"  Memoire max utilisee  : {mem_str}")
        print(f"  Snapshots enregistres : {len(self.snapshots)}")
