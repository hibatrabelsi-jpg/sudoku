import sys
from sudoku_grid import SudokuGrid


def main():
    # Verification des arguments
    if len(sys.argv) < 2:
        print("Usage : python main.py <fichier_grille>")
        print("Exemple : python main.py data/grille1.txt")
        sys.exit(1)

    filename = sys.argv[1]

    # Chargement de la grille
    print("=" * 50)
    print("         SUDOKU SOLVER")
    print("=" * 50)

    grid = SudokuGrid(filename)
    print(f"\nGrille chargee depuis : {filename}")
    print(f"Cases vides : {grid.stats['cases_vides_initiales']}\n")
    grid.display_terminal()

    # =====================================================================
    # Resolution par BACKTRACKING
    # =====================================================================
    print("\n" + "=" * 50)
    print("  METHODE 1 : BACKTRACKING")
    print("=" * 50)

    success_bt = grid.solve_backtracking()

    if success_bt:
        print("\nGrille resolue !\n")
        grid.display_terminal()
    else:
        print("\nEchec de la resolution.")

    grid.display_stats()
    stats_bt = grid.get_stats()
    snapshots_bt = len(grid.get_snapshots())

    # =====================================================================
    # Resolution par FORCE BRUTE
    # =====================================================================
    print("\n" + "=" * 50)
    print("  METHODE 2 : FORCE BRUTE")
    print("=" * 50)

    success_bf = grid.solve_brute_force(max_iterations=500000)

    if success_bf:
        print("\nGrille resolue !\n")
        grid.display_terminal()
    else:
        print(f"\nArret apres {grid.stats['iterations']} iterations (limite atteinte).")

    grid.display_stats()
    stats_bf = grid.get_stats()

    # =====================================================================
    # TABLEAU COMPARATIF
    # =====================================================================
    print("\n" + "=" * 50)
    print("  TABLEAU COMPARATIF")
    print("=" * 50)

    def format_mem(bytes_val):
        kb = bytes_val / 1024
        return f"{kb:.1f} Ko" if kb < 1024 else f"{kb/1024:.2f} Mo"

    print(f"\n{'Critere':<30} {'Backtracking':>15} {'Force Brute':>15}")
    print("-" * 62)
    print(f"{'Resultat':<30} {'Resolu' if success_bt else 'Echec':>15} {'Resolu' if success_bf else 'Limite atteinte':>15}")
    print(f"{'Iterations':<30} {stats_bt['iterations']:>15} {stats_bf['iterations']:>15}")
    print(f"{'Verifications':<30} {stats_bt['verifications']:>15} {stats_bf['verifications']:>15}")
    print(f"{'Backtracks':<30} {stats_bt['backtracks']:>15} {'-':>15}")
    print(f"{'Temps (s)':<30} {stats_bt['temps_execution']:>15.6f} {stats_bf['temps_execution']:>15.6f}")
    print(f"{'Memoire max':<30} {format_mem(stats_bt['memoire_max']):>15} {format_mem(stats_bf['memoire_max']):>15}")
    print(f"{'Snapshots (replay)':<30} {snapshots_bt:>15} {len(grid.get_snapshots()):>15}")

    # Ratios de performance
    print(f"\n{'RATIOS (Force Brute / Backtracking)':<30}")
    print("-" * 62)

    if stats_bt['iterations'] > 0:
        ratio_iter = stats_bf['iterations'] / stats_bt['iterations']
        print(f"  Iterations            : x{ratio_iter:.1f}")

    if stats_bt['verifications'] > 0:
        ratio_verif = stats_bf['verifications'] / stats_bt['verifications']
        print(f"  Verifications         : x{ratio_verif:.1f}")

    if stats_bt['temps_execution'] > 0:
        ratio_temps = stats_bf['temps_execution'] / stats_bt['temps_execution']
        print(f"  Temps                 : x{ratio_temps:.1f}")

    if stats_bt['memoire_max'] > 0:
        ratio_mem = stats_bf['memoire_max'] / stats_bt['memoire_max']
        print(f"  Memoire               : x{ratio_mem:.1f}")

    if not success_bf:
        print(f"\n-> La force brute n'a pas pu resoudre cette grille en {stats_bf['iterations']} iterations.")
        print("   C'est normal : sans verification intermediaire, elle explore trop de combinaisons.")

    print(f"\n-> Conclusion : le backtracking est largement plus performant sur tous")
    print(f"   les criteres car il detecte les erreurs immediatement au lieu de")
    print(f"   remplir toute la grille pour rien.")

    # Lancement de l'interface Pygame
    print(f"\nLancement de l'interface graphique...")
    from gui.app import launch
    launch()


if __name__ == "__main__":
    main()
