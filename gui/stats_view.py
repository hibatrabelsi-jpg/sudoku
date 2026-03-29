"""
Ecran de comparaison des deux methodes.
Layout centre avec conteneur principal et deux colonnes equilibrees.
"""

import pygame
import os
import time
from gui import constants as C
from gui.constants import *
from gui.fonts import fonts
from gui.components import Button


PASTEL_BLUE = (160, 190, 220)
PASTEL_MINT = (160, 210, 190)
PASTEL_LAVENDER = (185, 175, 215)
PASTEL_PEACH = (215, 185, 170)
RATIO_PASTELS = [PASTEL_BLUE, PASTEL_MINT, PASTEL_LAVENDER, PASTEL_PEACH]


class StatsView:

    def __init__(self, surface):
        self.surface = surface

        self.btn_view_bt = Button(0, 0, 200, BTN_HEIGHT, "Grille Backtracking")
        self.btn_view_bf = Button(0, 0, 200, BTN_HEIGHT, "Grille Force Brute")
        self.btn_replay_bt = Button(0, 0, 180, BTN_HEIGHT, "Replay Backtracking")
        self.btn_menu = Button(0, 0, 140, BTN_HEIGHT, "Retour au menu")

        self.stats_bt = {}
        self.stats_bf = {}
        self.success_bt = False
        self.success_bf = False
        self.grid_name = ""
        self.setup_time = 0
        self.anim_duration = 1.2

    def setup(self, stats_bt, stats_bf, success_bt, success_bf, grid_path):
        self.stats_bt = stats_bt
        self.stats_bf = stats_bf
        self.success_bt = success_bt
        self.success_bf = success_bf
        self.grid_name = os.path.basename(grid_path).replace(".txt", "").replace("grille", "Grille ")
        self.setup_time = time.time()

    def _anim_progress(self):
        elapsed = time.time() - self.setup_time
        if elapsed >= self.anim_duration:
            return 1.0
        t = elapsed / self.anim_duration
        return 1.0 - (1.0 - t) ** 3

    def _container(self):
        """
        Conteneur principal centre.
        Tout le contenu est positionne relativement a ce conteneur.
        """
        max_w = 1300
        cw = min(max_w, C.WINDOW_WIDTH - 120)
        cx = (C.WINDOW_WIDTH - cw) // 2

        # Vertical
        header_y = SP_XXL + SP_M
        col_gap = 80
        col_top = header_y + SP_XXXL

        # Deux colonnes egales
        col_w = (cw - col_gap) // 2
        left_x = cx
        right_x = cx + col_w + col_gap

        # Lignes du tableau
        row_h = SP_XXL
        table_rows = 6
        table_bottom = col_top + SP_XL + table_rows * row_h

        # Insight sous les colonnes
        insight_y = table_bottom + SP_XXL

        # Boutons en bas
        buttons_y = C.WINDOW_HEIGHT - SP_XXL - BTN_HEIGHT

        return {
            "cx": cx, "cw": cw,
            "header_y": header_y,
            "col_top": col_top,
            "left_x": left_x, "right_x": right_x, "col_w": col_w,
            "row_h": row_h,
            "insight_y": insight_y,
            "buttons_y": buttons_y,
        }

    def draw(self):
        C = self._container()
        self._draw_header(C)
        self._draw_table(C)
        self._draw_ratios(C)
        self._draw_insight(C)
        self._draw_buttons(C)

    # =========================================================================
    # HEADER — aligne sur le bord gauche du conteneur
    # =========================================================================

    def _draw_header(self, C):
        title = fonts.title.render("Comparaison", True, TEXT_TITLE)
        self.surface.blit(title, (C["cx"], C["header_y"]))

        sep = fonts.subtitle.render(f"—  {self.grid_name}", True, TEXT_MUTED)
        self.surface.blit(sep, (C["cx"] + title.get_width() + SP_M, C["header_y"] + SP_S))

        cases = fonts.body.render(
            f"{self.stats_bt.get('cases_vides_initiales', 0)} cases vides", True, TEXT_HINT)
        self.surface.blit(cases, (C["cx"], C["header_y"] + SP_XL + SP_L))

    # =========================================================================
    # TABLEAU — colonne gauche, occupe toute la largeur de la colonne
    # =========================================================================

    def _draw_table(self, C):
        tx = C["left_x"]
        ty = C["col_top"]
        tw = C["col_w"]
        row_h = C["row_h"]

        col_label_w = int(tw * 0.34)
        col_bt_w = int(tw * 0.33)
        col_bf_w = tw - col_label_w - col_bt_w

        # En-tete
        h_bt = fonts.body_bold.render("BACKTRACKING", True, PASTEL_BLUE)
        h_bf = fonts.body_bold.render("FORCE BRUTE", True, (170, 170, 170))
        self.surface.blit(h_bt, (tx + col_label_w + col_bt_w - h_bt.get_width(), ty))
        self.surface.blit(h_bf, (tx + col_label_w + col_bt_w + col_bf_w - h_bf.get_width(), ty))

        # Separateur en-tete
        sep_y = ty + SP_XL
        sep_surf = pygame.Surface((tw, 1), pygame.SRCALPHA)
        sep_surf.fill((255, 255, 255, 35))
        self.surface.blit(sep_surf, (tx, sep_y))

        # Lignes
        rows = self._get_table_rows()
        for i, (label, val_bt, val_bf) in enumerate(rows):
            ry = sep_y + SP_M + i * row_h

            lbl = fonts.body.render(label, True, TEXT_MUTED)
            self.surface.blit(lbl, (tx, ry + SP_XS))

            vbt = fonts.body_bold.render(val_bt, True, (225, 228, 238))
            self.surface.blit(vbt, (tx + col_label_w + col_bt_w - vbt.get_width(), ry + SP_XS))

            vbf = fonts.body.render(val_bf, True, TEXT_MUTED)
            self.surface.blit(vbf, (tx + col_label_w + col_bt_w + col_bf_w - vbf.get_width(), ry + SP_XS))

            if i < len(rows) - 1:
                line_y = ry + row_h - SP_XS
                line_surf = pygame.Surface((tw, 1), pygame.SRCALPHA)
                line_surf.fill((255, 255, 255, 12))
                self.surface.blit(line_surf, (tx, line_y))

    def _get_table_rows(self):
        bt = self.stats_bt
        bf = self.stats_bf

        def fmt_time(t):
            return f"{t*1000:.1f} ms" if t < 1 else f"{t:.3f} s"

        def fmt_mem(b):
            kb = b / 1024
            return f"{kb:.1f} Ko" if kb < 1024 else f"{kb/1024:.2f} Mo"

        return [
            ("Resultat", "Resolu" if self.success_bt else "Echec",
             "Resolu" if self.success_bf else "Limite atteinte"),
            ("Iterations",
             f"{bt.get('iterations', 0):,}".replace(",", " "),
             f"{bf.get('iterations', 0):,}".replace(",", " ")),
            ("Verifications",
             f"{bt.get('verifications', 0):,}".replace(",", " "),
             f"{bf.get('verifications', 0):,}".replace(",", " ")),
            ("Backtracks",
             f"{bt.get('backtracks', 0):,}".replace(",", " "), "\u2014"),
            ("Temps",
             fmt_time(bt.get("temps_execution", 0)),
             fmt_time(bf.get("temps_execution", 0))),
            ("Memoire",
             fmt_mem(bt.get("memoire_max", 0)),
             fmt_mem(bf.get("memoire_max", 0))),
        ]

    # =========================================================================
    # RATIOS — colonne droite, barres sur toute la largeur de la colonne
    # =========================================================================

    def _draw_ratios(self, C):
        rx = C["right_x"]
        ry = C["col_top"]
        rw = C["col_w"]

        title = fonts.subtitle.render("Ratios", True, TEXT_LIGHT)
        self.surface.blit(title, (rx, ry - SP_S))

        sub = fonts.body.render("Force Brute / Backtracking", True, TEXT_HINT)
        self.surface.blit(sub, (rx, ry + SP_XL))

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

        bar_start_y = ry + SP_XXL + SP_XL + SP_M
        bar_max_w = rw
        bar_h = 10
        max_ratio = max((r for _, r in ratios), default=1)
        anim = self._anim_progress()

        spacing = C["row_h"] * 6 // max(len(ratios), 1)
        spacing = min(spacing, SP_XXXL + SP_S)

        for i, (label, ratio) in enumerate(ratios):
            cy = bar_start_y + i * spacing
            pastel = RATIO_PASTELS[i % len(RATIO_PASTELS)]

            lbl = fonts.body_bold.render(label, True, (190, 190, 190))
            self.surface.blit(lbl, (rx, cy))

            val_text = f"x{ratio:.1f}"
            val_surf = fonts.subtitle.render(val_text, True, pastel)
            self.surface.blit(val_surf, (rx + rw - val_surf.get_width(), cy))

            bar_y = cy + SP_L + SP_M
            bg_surf = pygame.Surface((bar_max_w, bar_h), pygame.SRCALPHA)
            bg_surf.fill((255, 255, 255, 15))
            self.surface.blit(bg_surf, (rx, bar_y))

            target_w = max(2, int((ratio / max_ratio) * bar_max_w))
            current_w = int(target_w * anim)
            if current_w > 0:
                fill_surf = pygame.Surface((current_w, bar_h), pygame.SRCALPHA)
                fill_surf.fill((*pastel, 160))
                self.surface.blit(fill_surf, (rx, bar_y))

    # =========================================================================
    # INSIGHT — pleine largeur du conteneur
    # =========================================================================

    def _draw_insight(self, C):
        iy = C["insight_y"]
        ix = C["cx"]

        border_surf = pygame.Surface((2, SP_XXL + SP_L), pygame.SRCALPHA)
        border_surf.fill((*PASTEL_BLUE, 100))
        self.surface.blit(border_surf, (ix, iy))

        text_x = ix + SP_L
        line1 = fonts.body.render(
            "Le backtracking detecte les erreurs immediatement, ce qui lui permet d'elaguer",
            True, TEXT_MUTED)
        line2 = fonts.body.render(
            "des branches entieres et de resoudre la grille en quelques millisecondes.",
            True, TEXT_MUTED)
        line3 = fonts.body.render(
            "La force brute explore toutes les combinaisons sans verification intermediaire.",
            True, TEXT_MUTED)

        self.surface.blit(line1, (text_x, iy))
        self.surface.blit(line2, (text_x, iy + SP_XL))
        self.surface.blit(line3, (text_x, iy + SP_XL * 2))

    # =========================================================================
    # BOUTONS — centres horizontalement dans le conteneur
    # =========================================================================

    def _draw_buttons(self, C):
        by = C["buttons_y"]
        total_w = 200 + SP_M + 200 + SP_M + 180 + SP_XL + 140
        start_x = C["cx"] + (C["cw"] - total_w) // 2

        self.btn_view_bt.rect.topleft = (start_x, by)
        self.btn_view_bf.rect.topleft = (start_x + 200 + SP_M, by)
        self.btn_replay_bt.rect.topleft = (start_x + 400 + SP_M * 2, by)
        self.btn_menu.rect.topleft = (start_x + 580 + SP_M * 2 + SP_XL, by)

        self.btn_view_bt.draw(self.surface)
        self.btn_view_bf.draw(self.surface)
        self.btn_replay_bt.draw(self.surface)

        menu_rect = self.btn_menu.rect
        border_color = (55, 55, 58) if not self.btn_menu.hovered else (80, 80, 85)
        pygame.draw.rect(self.surface, BG_COLOR, menu_rect, border_radius=BTN_RADIUS)
        pygame.draw.rect(self.surface, border_color, menu_rect, width=1, border_radius=BTN_RADIUS)
        menu_text = fonts.small.render(self.btn_menu.text, True, TEXT_HINT)
        self.surface.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

    def handle_event(self, event):
        if self.btn_view_bt.handle_event(event):
            return "view_bt"
        if self.btn_view_bf.handle_event(event):
            return "view_bf"
        if self.btn_replay_bt.handle_event(event):
            return "replay_bt"
        if self.btn_menu.handle_event(event):
            return "menu"
        return None
