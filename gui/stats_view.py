"""
Ecran de statistiques et comparaison : affiche les resultats des deux methodes
cote a cote avec les ratios de performance.
Permet de naviguer vers le detail de chaque methode.
"""

import pygame
import os
from gui.constants import *
from gui.components import Button


class StatsView:
    """Ecran comparatif des deux methodes de resolution"""

    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SUBTITLE, bold=True)
        self.font_body = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY)
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
        self.font_value = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY, bold=True)
        self.font_ratio = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL, bold=True)

        # Boutons
        btn_y = 620
        self.btn_view_bt = Button(40, btn_y, 220, 40, "Voir grille Backtracking")
        self.btn_view_bf = Button(280, btn_y, 220, 40, "Voir grille Force Brute")
        self.btn_replay_bt = Button(520, btn_y, 200, 40, "Replay Backtracking")
        self.btn_menu = Button(WINDOW_WIDTH - 170, btn_y, 140, 40, "Retour au menu")

        # Donnees
        self.stats_bt = {}
        self.stats_bf = {}
        self.success_bt = False
        self.success_bf = False
        self.grid_name = ""

    def setup(self, stats_bt, stats_bf, success_bt, success_bf, grid_path):
        """Configure l'ecran avec les resultats des deux methodes"""
        self.stats_bt = stats_bt
        self.stats_bf = stats_bf
        self.success_bt = success_bt
        self.success_bf = success_bf
        self.grid_name = os.path.basename(grid_path).replace(".txt", "").replace("grille", "Grille ")

    def draw(self):
        """Dessine l'ecran de comparaison"""
        # Titre avec nom de la grille
        title = self.font_title.render(
            f"Comparaison — {self.grid_name}", True, TEXT_TITLE)
        self.surface.blit(title, (40, 30))

        subtitle = self.font_small.render(
            f"{self.stats_bt.get('cases_vides_initiales', 0)} cases vides",
            True, TEXT_SECONDARY)
        self.surface.blit(subtitle, (40, 60))

        # Tableau comparatif
        self._draw_table()

        # Ratios
        self._draw_ratios()

        # Conclusion
        self._draw_conclusion()

        # Boutons
        self.btn_view_bt.draw(self.surface)
        self.btn_view_bf.draw(self.surface)
        self.btn_replay_bt.draw(self.surface)
        self.btn_menu.draw(self.surface)

    def _draw_table(self):
        """Dessine le tableau comparatif"""
        table_x = 40
        table_y = 100
        col_label_w = 220
        col_val_w = 180
        row_h = 38
        table_w = col_label_w + col_val_w * 2

        # En-tete
        header_rect = pygame.Rect(table_x, table_y, table_w, row_h)
        pygame.draw.rect(self.surface, (235, 240, 250), header_rect)
        pygame.draw.rect(self.surface, STAT_BORDER, header_rect, width=1)

        h_label = self.font_value.render("Critere", True, TEXT_PRIMARY)
        h_bt = self.font_value.render("Backtracking", True, TEXT_TITLE)
        h_bf = self.font_value.render("Force Brute", True, (200, 80, 80))

        self.surface.blit(h_label, (table_x + 15, table_y + 10))
        self.surface.blit(h_bt, (table_x + col_label_w + (col_val_w - h_bt.get_width()) // 2, table_y + 10))
        self.surface.blit(h_bf, (table_x + col_label_w + col_val_w + (col_val_w - h_bf.get_width()) // 2, table_y + 10))

        # Lignes du tableau
        rows = self._get_table_rows()
        for i, (label, val_bt, val_bf) in enumerate(rows):
            y = table_y + row_h * (i + 1)
            row_rect = pygame.Rect(table_x, y, table_w, row_h)

            # Fond alterne
            if i % 2 == 0:
                pygame.draw.rect(self.surface, CELL_NORMAL, row_rect)
            else:
                pygame.draw.rect(self.surface, STAT_BG, row_rect)
            pygame.draw.rect(self.surface, STAT_BORDER, row_rect, width=1)

            # Label
            lbl = self.font_body.render(label, True, TEXT_PRIMARY)
            self.surface.blit(lbl, (table_x + 15, y + 10))

            # Valeur backtracking
            vbt = self.font_body.render(val_bt, True, TEXT_PRIMARY)
            self.surface.blit(vbt, (table_x + col_label_w + (col_val_w - vbt.get_width()) // 2, y + 10))

            # Valeur force brute
            vbf = self.font_body.render(val_bf, True, TEXT_PRIMARY)
            self.surface.blit(vbf, (table_x + col_label_w + col_val_w + (col_val_w - vbf.get_width()) // 2, y + 10))

    def _get_table_rows(self):
        """Prepare les lignes du tableau"""
        bt = self.stats_bt
        bf = self.stats_bf

        def fmt_num(n):
            return f"{n:,}".replace(",", " ")

        def fmt_time(t):
            if t < 1:
                return f"{t*1000:.1f} ms"
            return f"{t:.3f} s"

        def fmt_mem(b):
            kb = b / 1024
            if kb < 1024:
                return f"{kb:.1f} Ko"
            return f"{kb/1024:.2f} Mo"

        status_bt = "Resolu" if self.success_bt else "Echec"
        status_bf = "Resolu" if self.success_bf else "Limite atteinte"

        rows = [
            ("Resultat", status_bt, status_bf),
            ("Iterations", fmt_num(bt.get("iterations", 0)), fmt_num(bf.get("iterations", 0))),
            ("Verifications", fmt_num(bt.get("verifications", 0)), fmt_num(bf.get("verifications", 0))),
            ("Backtracks", fmt_num(bt.get("backtracks", 0)), "-"),
            ("Temps", fmt_time(bt.get("temps_execution", 0)), fmt_time(bf.get("temps_execution", 0))),
            ("Memoire max", fmt_mem(bt.get("memoire_max", 0)), fmt_mem(bf.get("memoire_max", 0))),
        ]
        return rows

    def _draw_ratios(self):
        """Dessine les ratios de performance avec barres visuelles"""
        x = 40
        y = 360

        title = self.font_value.render("Ratios (Force Brute / Backtracking)", True, TEXT_PRIMARY)
        self.surface.blit(title, (x, y))

        bt = self.stats_bt
        bf = self.stats_bf

        ratios = []
        if bt.get("iterations", 0) > 0:
            ratios.append(("Iterations", bf["iterations"] / bt["iterations"]))
        if bt.get("verifications", 0) > 0:
            ratios.append(("Verifications", bf["verifications"] / bt["verifications"]))
        if bt.get("temps_execution", 0) > 0:
            ratios.append(("Temps", bf["temps_execution"] / bt["temps_execution"]))
        if bt.get("memoire_max", 0) > 0:
            ratios.append(("Memoire", bf["memoire_max"] / bt["memoire_max"]))

        bar_x = x
        bar_y = y + 35
        bar_max_w = 500
        max_ratio = max((r for _, r in ratios), default=1)

        for i, (label, ratio) in enumerate(ratios):
            cy = bar_y + i * 40

            # Label
            lbl = self.font_body.render(label, True, TEXT_PRIMARY)
            self.surface.blit(lbl, (bar_x, cy + 2))

            # Barre
            bx = bar_x + 130
            bar_w = int((ratio / max_ratio) * bar_max_w)
            bar_w = max(bar_w, 4)

            bar_rect = pygame.Rect(bx, cy + 2, bar_w, 22)
            pygame.draw.rect(self.surface, (200, 80, 80, 150), bar_rect, border_radius=4)

            # Valeur
            val = self.font_ratio.render(f"x{ratio:.1f}", True, (200, 80, 80))
            self.surface.blit(val, (bx + bar_w + 10, cy + 3))

    def _draw_conclusion(self):
        """Dessine la conclusion"""
        y = 530

        pygame.draw.line(self.surface, STAT_BORDER, (40, y), (WINDOW_WIDTH - 40, y), 1)

        conclusion = self.font_body.render(
            "Le backtracking est plus performant sur tous les criteres car il detecte",
            True, TEXT_PRIMARY)
        conclusion2 = self.font_body.render(
            "les erreurs immediatement au lieu de remplir toute la grille pour rien.",
            True, TEXT_PRIMARY)
        self.surface.blit(conclusion, (40, y + 15))
        self.surface.blit(conclusion2, (40, y + 38))

        if not self.success_bf:
            note = self.font_small.render(
                f"Note : la force brute a atteint la limite de {self.stats_bf.get('iterations', 0):,} iterations sans resoudre la grille.".replace(",", " "),
                True, TEXT_SECONDARY)
            self.surface.blit(note, (40, y + 68))

    def handle_event(self, event):
        """
        Retourne l'action choisie :
        - "view_bt" : voir la grille backtracking
        - "view_bf" : voir la grille force brute
        - "replay_bt" : replay du backtracking
        - "menu" : retour au menu
        """
        if self.btn_view_bt.handle_event(event):
            return "view_bt"
        if self.btn_view_bf.handle_event(event):
            return "view_bf"
        if self.btn_replay_bt.handle_event(event):
            return "replay_bt"
        if self.btn_menu.handle_event(event):
            return "menu"
        return None
