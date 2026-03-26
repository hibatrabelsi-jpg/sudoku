import copy

class SudokuGrid:
    def __init__(self, filename):
        self.grid = []
        self.initial_grid = [] 
        self.load_file(filename)

    def load_file(self, filename):
        """Importe et parse la grille [cite: 323]"""
        with open(filename, 'r') as f:
            for line in f:
                # On transforme '_' en 0 [cite: 39]
                row = [int(c) if c.isdigit() else 0 for c in line.strip() if c in "_123456789"]
                if row:
                    self.grid.append(row)
        self.initial_grid = copy.deepcopy(self.grid)

    def is_valid(self, row, col, n):
        """Vérifie les contraintes de ligne, colonne et carré [cite: 7, 55]"""
        for i in range(9):
            if self.grid[row][i] == n or self.grid[i][col] == n:
                return False
        # Calcul du carré 3x3 [cite: 53]
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == n:
                    return False
        return True

    def display_terminal(self):
        """Affiche la grille avec distinction visuelle """
        for r in range(9):
            if r % 3 == 0 and r != 0: print("-" * 21)
            line = ""
            for c in range(9):
                if c % 3 == 0 and c != 0: line += "| "
                val = self.grid[r][c]
                if val == 0: line += ". "
                elif self.initial_grid[r][c] != 0: line += f"\033[1m{val}\033[0m " # Gras (origine)
                else: line += f"\033[94m{val}\033[0m " # Bleu (ajouté)
            print(line)

    def solve_logic_elimination(self):
        """Bonus : Technique d'élimination simple [cite: 253]"""
        changed = False
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    candidates = [n for n in range(1, 10) if self.is_valid(r, c, n)]
                    if len(candidates) == 1:
                        self.grid[r][c] = candidates[0]
                        changed = True
        return changed

    def solve_brute_force(self, index=0, counter=0):
        """Algorithme de Force Brute avec compteur [cite: 64, 75, 108]"""
        if counter > 500000: # Limite pour la démo [cite: 75]
            return False, counter
        if index == 81: 
            return True, counter

        row, col = index // 9, index % 9
        if self.grid[row][col] != 0:
            return self.solve_brute_force(index + 1, counter)

        for n in range(1, 10):
            if self.is_valid(row, col, n):
                self.grid[row][col] = n
                success, final_counter = self.solve_brute_force(index + 1, counter + 1)
                if success: return True, final_counter
                self.grid[row][col] = 0
            counter += 1
        return False, counter