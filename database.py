"""
Module de persistance MySQL.
Gere la connexion, l'insertion des resultats, la consultation
de l'historique et l'export en Markdown.
"""

import mysql.connector
import os
from datetime import datetime


# =============================================================================
# CONFIGURATION (a adapter selon ton installation)
# =============================================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Kennyserpin2003!",
    "database": "sudoku_solver"
}


class Database:
    """Gestion de la base de donnees MySQL pour le Sudoku Solver"""

    def __init__(self):
        self.connection = None
        self.available = False
        self._connect()

    def _connect(self):
        """Tente de se connecter a la base de donnees"""
        try:
            # D'abord creer la base si elle n'existe pas
            init_conn = mysql.connector.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"]
            )
            cursor = init_conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS sudoku_solver")
            cursor.close()
            init_conn.close()

            # Connexion a la base
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self._create_tables()
            self.available = True
            print("[DB] Connexion MySQL etablie")

        except mysql.connector.Error as e:
            print(f"[DB] MySQL non disponible : {e}")
            print("[DB] Le programme fonctionne sans base de donnees")
            self.available = False

    def _ensure_connected(self):
        """Verifie que la connexion est toujours active, reconnecte si besoin"""
        if not self.available:
            return False
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=1)
            return True
        except mysql.connector.Error:
            try:
                self.connection = mysql.connector.connect(**DB_CONFIG)
                return True
            except mysql.connector.Error:
                return False

    def _ensure_connection(self):
        """Verifie que la connexion est active, reconnecte si besoin"""
        if not self.available:
            return False
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=1)
            return True
        except mysql.connector.Error:
            try:
                self.connection = mysql.connector.connect(**DB_CONFIG)
                return True
            except mysql.connector.Error:
                return False

    def _create_tables(self):
        """Cree les tables si elles n'existent pas"""
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grilles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                grille_initiale TEXT NOT NULL,
                cases_vides INT NOT NULL,
                date_import DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resolutions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                grille_id INT NOT NULL,
                methode VARCHAR(50) NOT NULL,
                grille_resolue TEXT,
                temps_execution FLOAT NOT NULL,
                iterations INT NOT NULL,
                backtracks INT DEFAULT 0,
                verifications INT NOT NULL,
                memoire_max BIGINT DEFAULT 0,
                nb_snapshots INT DEFAULT 0,
                succes BOOLEAN DEFAULT TRUE,
                date_resolution DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (grille_id) REFERENCES grilles(id)
            )
        """)

        self.connection.commit()
        cursor.close()

    # =========================================================================
    # INSERTION
    # =========================================================================

    def _grid_to_string(self, grid):
        """Convertit un tableau 2D en chaine de 81 caracteres"""
        result = ""
        for row in grid:
            for val in row:
                result += str(val) if val != 0 else "_"
        return result

    def _find_or_create_grid(self, initial_grid, cases_vides):
        """Trouve une grille existante ou en cree une nouvelle"""
        grid_str = self._grid_to_string(initial_grid)
        cursor = self.connection.cursor()

        # Chercher si la grille existe deja
        cursor.execute(
            "SELECT id FROM grilles WHERE grille_initiale = %s", (grid_str,))
        result = cursor.fetchone()

        if result:
            cursor.close()
            return result[0]

        # Creer la grille
        cursor.execute(
            "INSERT INTO grilles (grille_initiale, cases_vides) VALUES (%s, %s)",
            (grid_str, cases_vides))
        self.connection.commit()
        grid_id = cursor.lastrowid
        cursor.close()
        return grid_id

    def save_resolution(self, grid_obj, success):
        """
        Sauvegarde le resultat d'une resolution en base.
        Appelee automatiquement apres chaque resolution.
        """
        if not self.available:
            return

        if not self._ensure_connected():
            return

        try:
            stats = grid_obj.get_stats()
            grid_id = self._find_or_create_grid(
                grid_obj.initial_grid,
                stats["cases_vides_initiales"]
            )

            solved_str = self._grid_to_string(grid_obj.grid) if success else ""

            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO resolutions
                (grille_id, methode, grille_resolue, temps_execution,
                 iterations, backtracks, verifications, memoire_max,
                 nb_snapshots, succes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                grid_id,
                stats["methode"],
                solved_str,
                stats["temps_execution"],
                stats["iterations"],
                stats["backtracks"],
                stats["verifications"],
                stats["memoire_max"],
                len(grid_obj.get_snapshots()),
                success
            ))

            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as e:
            print(f"[DB] Erreur lors de la sauvegarde : {e}")

    # =========================================================================
    # CONSULTATION
    # =========================================================================

    def get_history(self, limit=50):
        """
        Retourne l'historique des resolutions.
        Chaque entree contient les infos de la resolution + la grille associee.
        """
        if not self.available or not self._ensure_connected():
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    r.id,
                    r.methode,
                    r.temps_execution,
                    r.iterations,
                    r.backtracks,
                    r.verifications,
                    r.memoire_max,
                    r.nb_snapshots,
                    r.succes,
                    r.date_resolution,
                    g.cases_vides,
                    g.grille_initiale
                FROM resolutions r
                JOIN grilles g ON r.grille_id = g.id
                ORDER BY r.date_resolution DESC
                LIMIT %s
            """, (limit,))

            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as e:
            print(f"[DB] Erreur lors de la consultation : {e}")
            return []

    def get_comparisons(self):
        """
        Retourne les resolutions groupees par grille pour la comparaison.
        Pour chaque grille, on recupere les resultats des deux methodes.
        """
        if not self.available or not self._ensure_connected():
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    g.id as grille_id,
                    g.cases_vides,
                    g.grille_initiale,
                    r.methode,
                    r.temps_execution,
                    r.iterations,
                    r.backtracks,
                    r.verifications,
                    r.memoire_max,
                    r.succes,
                    r.date_resolution
                FROM resolutions r
                JOIN grilles g ON r.grille_id = g.id
                ORDER BY g.id, r.methode
            """)

            results = cursor.fetchall()
            cursor.close()

            # Grouper par grille
            grids = {}
            for row in results:
                gid = row["grille_id"]
                if gid not in grids:
                    grids[gid] = {
                        "cases_vides": row["cases_vides"],
                        "grille_initiale": row["grille_initiale"],
                        "resolutions": {}
                    }
                grids[gid]["resolutions"][row["methode"]] = row

            return list(grids.values())

        except mysql.connector.Error as e:
            print(f"[DB] Erreur lors de la consultation : {e}")
            return []

    # =========================================================================
    # EXPORT MARKDOWN
    # =========================================================================

    def export_markdown(self, filepath="exports/rapport_comparatif.md"):
        """
        Genere le rapport comparatif en Markdown depuis les donnees en base.
        """
        if not self.available or not self._ensure_connected():
            return False

        comparisons = self.get_comparisons()
        if not comparisons:
            return False

        # Creer le dossier exports si besoin
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        def fmt_time(t):
            if t < 1:
                return f"{t*1000:.1f}ms"
            return f"{t:.3f}s"

        def fmt_mem(b):
            kb = b / 1024
            if kb < 1024:
                return f"{kb:.1f}Ko"
            return f"{kb/1024:.2f}Mo"

        lines = []
        lines.append("# Rapport comparatif - Sudoku Solver")
        lines.append("")
        lines.append(f"*Genere le {datetime.now().strftime('%d/%m/%Y a %H:%M')}*")
        lines.append("")

        # Tableau comparatif
        lines.append("## Tableau comparatif")
        lines.append("")
        lines.append("| Grille | Methode | Resultat | Iterations | Verifications | Backtracks |  Temps  | Memoire |")
        lines.append("|--------|---------|----------|------------|---------------|------------|---------|---------|")

        for i, comp in enumerate(comparisons):
            cv = comp["cases_vides"]
            label = f"Grille {i+1} ({cv} vides)"

            for methode in ["backtracking", "force_brute"]:
                if methode in comp["resolutions"]:
                    r = comp["resolutions"][methode]
                    resultat = "Resolu" if r["succes"] else "Limite"
                    m_name = "BT" if methode == "backtracking" else "BF"
                    bt = str(r["backtracks"]) if methode == "backtracking" else "-"
                    iters = str(r["iterations"])
                    verifs = str(r["verifications"])
                    temps = fmt_time(r["temps_execution"])
                    mem = fmt_mem(r["memoire_max"])

                    lines.append(f"| {label} | {m_name} | {resultat} | {iters} | {verifs} | {bt} | {temps} | {mem} |")

        # Ratios
        lines.append("")
        lines.append("## Ratios de performance (Force Brute / Backtracking)")
        lines.append("")
        lines.append("| Grille | Iterations | Verifications |  Temps  | Memoire |")
        lines.append("|--------|------------|---------------|---------|---------|")

        for i, comp in enumerate(comparisons):
            bt = comp["resolutions"].get("backtracking")
            bf = comp["resolutions"].get("force_brute")

            if bt and bf:
                cv = comp["cases_vides"]
                label = f"Grille {i+1} ({cv} vides)"

                r_iter = f"x{bf['iterations'] / max(bt['iterations'], 1):.1f}"
                r_verif = f"x{bf['verifications'] / max(bt['verifications'], 1):.1f}"
                r_temps = f"x{bf['temps_execution'] / max(bt['temps_execution'], 0.0001):.1f}"
                r_mem = f"x{bf['memoire_max'] / max(bt['memoire_max'], 1):.1f}"

                lines.append(f"| {label} | {r_iter} | {r_verif} | {r_temps} | {r_mem} |")

        # Conclusion
        lines.append("")
        lines.append("## Conclusion")
        lines.append("")
        lines.append("Le backtracking est largement plus performant que la force brute sur tous les criteres mesures. La force brute genere toutes les combinaisons possibles sans verifier la validite en cours de route, ce qui la rend inutilisable sur les grilles avec beaucoup de cases vides. Le backtracking, en detectant les erreurs immediatement et en revenant en arriere, elague des branches entieres de l'arbre de recherche et trouve la solution en quelques millisecondes.")
        lines.append("")

        with open(filepath, 'w') as f:
            f.write("\n".join(lines))

        return True

    # =========================================================================
    # FERMETURE
    # =========================================================================

    def close(self):
        """Ferme la connexion"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("[DB] Connexion MySQL fermee")
