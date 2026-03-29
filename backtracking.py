import copy

def trouver_case_vide(grille):
    for row in range(9):
        for col in range(9):
            if grille[row][col] == 0:
                return (row, col)
    return None

def backtracking(grille, compteur, snapshots):
    case = trouver_case_vide(grille)
    
    if case is None:
        return True
    
    row, col = case
    
    for chiffre in range(1, 10):
        if grille.is_valid(row, col, chiffre):
            grille.grid[row][col] = chiffre
            snapshots.append({
                "grille": copy.deepcopy(grille.grid),
                "case": case,
                "chiffre": chiffre,
                "action": "placement"
            })
            
            if backtracking(grille, compteur, snapshots):
                return True
            
            grille.grid[row][col] = 0
            compteur[0] += 1
            snapshots.append({
                "grille": copy.deepcopy(grille.grid),
                "case": case,
                "chiffre": 0,
                "action": "retrait"
            })
    
    return False

def resoudre(grille):
    compteur = [0]
    snapshots = []
    backtracking(grille, compteur, snapshots)
    return {
        "compteur": compteur[0],
        "snapshots": snapshots
    }