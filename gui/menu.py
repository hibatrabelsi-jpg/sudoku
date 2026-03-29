"""
Ecran du menu principal.
Colonne gauche : actions. Colonne droite : liste de grilles + apercu.
"""

import pygame
import os
import shutil
from gui import constants as C
from gui.constants import *
from gui.fonts import fonts
from gui.components import Button


PASTEL_BLUE = (160, 190, 220)
PASTEL_MINT = (170, 220, 200)


class MenuScreen:

    def __init__(self, surface):
        self.surface = surface
        self.grids = self._find_grids()
        self.selected_grid = 0

        # Boutons d'action
        self.btn_backtracking = Button(0, 0, 280, BTN_HEIGHT, "Resoudre (Backtracking)")
        self.btn_brute_force = Button(0, 0, 280, BTN_HEIGHT, "Resoudre (Force Brute)")
        self.btn_compare = Button(0, 0, 280, BTN_HEIGHT, "Comparer les deux")
        self.btn_play = Button(0, 0, 280, BTN_HEIGHT, "Jouer")
        self.btn_export = Button(0, 0, 280, BTN_HEIGHT, "Exporter le rapport")

        # Bouton import
        self.btn_import = Button(0, 0, 0, 36, "Importer une grille")

        # Scroll
        self.scroll_offset = 0
        self.max_visible_grids = 8
        self.btn_scroll_up = Button(0, 0, 110, 30, "^")
        self.btn_scroll_down = Button(0, 0, 110, 30, "v")

        self.import_message = ""
        self.import_message_timer = 0

        # Apercu
        self.preview_grid = None
        self._load_preview()

    def _find_grids(self):
        grid_dir = "data"
        if not os.path.exists(grid_dir):
            os.makedirs(grid_dir)
            return []
        files = sorted([f for f in os.listdir(grid_dir) if f.endswith(".txt")])
        return [os.path.join(grid_dir, f) for f in files]

    def _load_preview(self):
        if not self.grids:
            self.preview_grid = None
            return
        try:
            from sudoku_grid import SudokuGrid
            g = SudokuGrid(self.grids[self.selected_grid])
            self.preview_grid = [row[:] for row in g.grid]
        except Exception:
            self.preview_grid = None

    def _import_grid(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            filepath = filedialog.askopenfilename(
                title="Importer une grille de Sudoku",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
            root.destroy()

            if filepath and os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    new_content = f.read().strip()
                for existing in self.grids:
                    with open(existing, 'r') as f:
                        if f.read().strip() == new_content:
                            self.import_message = "Cette grille existe deja"
                            self.import_message_timer = 180
                            return

                filename = os.path.basename(filepath)
                dest = os.path.join("data", filename)
                if os.path.exists(dest):
                    name, ext = os.path.splitext(filename)
                    i = 1
                    while os.path.exists(dest):
                        dest = os.path.join("data", f"{name}_{i}{ext}")
                        i += 1
                shutil.copy2(filepath, dest)
                self.grids = self._find_grids()
                self.selected_grid = len(self.grids) - 1
                self._load_preview()
                self.import_message = f"Importee : {os.path.basename(dest)}"
                self.import_message_timer = 180
        except Exception as e:
            self.import_message = f"Erreur : {str(e)}"
            self.import_message_timer = 180

    def draw(self):
        ww = C.WINDOW_WIDTH
        wh = C.WINDOW_HEIGHT

        # Layout
        gap = SP_XXXL
        left_w = 300
        list_w = 120
        preview_cell = 36
        preview_size = preview_cell * 9  # 324px
        right_w = list_w + SP_XL + preview_size
        total_w = left_w + gap + right_w
        start_x = (ww - total_w) // 2

        left_x = start_x
        list_x = start_x + left_w + gap
        preview_x = list_x + list_w + SP_XL
        top_y = wh // 2 - 260

        # =================================================================
        # COLONNE GAUCHE — titre + actions
        # =================================================================

        title = fonts.hero.render("Sudoku Solver", True, TEXT_TITLE)
        self.surface.blit(title, (left_x, top_y))

        sub = fonts.small.render("Analyse comparative", True, TEXT_MUTED)
        self.surface.blit(sub, (left_x, top_y + SP_XXL + SP_S))
        sub2 = fonts.small.render("Force Brute vs Backtracking", True, TEXT_HINT)
        self.surface.blit(sub2, (left_x, top_y + SP_XXL + SP_XL))

        sep_y = top_y + SP_XXXL + SP_L
        sep = pygame.Surface((left_w, 1), pygame.SRCALPHA)
        sep.fill((255, 255, 255, 25))
        self.surface.blit(sep, (left_x, sep_y))

        actions_label = fonts.small.render("ACTIONS", True, TEXT_HINT)
        self.surface.blit(actions_label, (left_x, sep_y + SP_L))

        btn_start_y = sep_y + SP_XXL
        btn_gap = SP_XXL
        action_btns = [self.btn_backtracking, self.btn_brute_force,
                       self.btn_compare, self.btn_play, self.btn_export]
        for i, btn in enumerate(action_btns):
            btn.rect.x = left_x
            btn.rect.y = btn_start_y + i * btn_gap
            btn.rect.width = left_w
            btn.draw(self.surface)

        # =================================================================
        # COLONNE DROITE — liste de grilles (scrollable) + apercu
        # =================================================================

        # Label liste
        grids_label = fonts.small.render("GRILLES", True, TEXT_HINT)
        self.surface.blit(grids_label, (list_x, top_y))

        # Liste scrollable
        list_y = top_y + SP_XL
        item_h = BTN_HEIGHT + SP_S
        visible_start = self.scroll_offset
        visible_end = min(len(self.grids), self.scroll_offset + self.max_visible_grids)
        can_scroll_up = self.scroll_offset > 0
        can_scroll_down = visible_end < len(self.grids)

        # Fleche haut
        if can_scroll_up:
            self.btn_scroll_up.rect = pygame.Rect(list_x, list_y - 30 - SP_XS, list_w, 26)
            self.btn_scroll_up.draw(self.surface)

        # Boutons de grille
        self.grid_buttons = []
        for idx in range(visible_start, visible_end):
            i_vis = idx - visible_start
            name = os.path.basename(self.grids[idx]).replace(".txt", "").replace("grille", "Grille ")
            btn_rect = pygame.Rect(list_x, list_y + i_vis * item_h, list_w, BTN_HEIGHT)

            if idx == self.selected_grid:
                pygame.draw.rect(self.surface, SURFACE_LIGHT, btn_rect, border_radius=BTN_RADIUS)
                pygame.draw.rect(self.surface, PASTEL_BLUE, btn_rect, width=2, border_radius=BTN_RADIUS)
                text_surf = fonts.button.render(name, True, TEXT_LIGHT)
                self.surface.blit(text_surf, text_surf.get_rect(center=btn_rect.center))
            else:
                pygame.draw.rect(self.surface, BTN_BG, btn_rect, border_radius=BTN_RADIUS)
                pygame.draw.rect(self.surface, BTN_BORDER, btn_rect, width=1, border_radius=BTN_RADIUS)
                text_surf = fonts.button.render(name, True, BTN_TEXT)
                self.surface.blit(text_surf, text_surf.get_rect(center=btn_rect.center))

            self.grid_buttons.append((btn_rect, idx))

        # Fleche bas
        if can_scroll_down:
            arrow_y = list_y + (visible_end - visible_start) * item_h + SP_XS
            self.btn_scroll_down.rect = pygame.Rect(list_x, arrow_y, list_w, 26)
            self.btn_scroll_down.draw(self.surface)

        # =================================================================
        # APERCU — a droite de la liste
        # =================================================================

        preview_label = fonts.small.render("APERCU", True, TEXT_HINT)
        self.surface.blit(preview_label, (preview_x, top_y))

        self._draw_preview(preview_x, top_y + SP_XL, preview_cell)

        # Bouton import — sous l'apercu
        import_y = top_y + SP_XL + preview_size + SP_L + SP_XL
        self.btn_import.rect = pygame.Rect(preview_x, import_y, preview_size, 36)
        self.btn_import.draw(self.surface)

        # Message d'import
        if self.import_message_timer > 0:
            self.import_message_timer -= 1
            is_warn = "existe deja" in self.import_message or "Erreur" in self.import_message
            color = (220, 180, 100) if is_warn else PASTEL_MINT
            msg = fonts.small.render(self.import_message, True, color)
            self.surface.blit(msg, (preview_x, import_y + 36 + SP_S))

    # =====================================================================
    # APERCU
    # =====================================================================

    def _draw_preview(self, px, py, cell):
        if not self.preview_grid:
            no_grid = fonts.body.render("Aucune grille", True, TEXT_HINT)
            self.surface.blit(no_grid, (px, py + SP_XXL))
            return

        grid_size = cell * 9

        # Nom + infos
        name = os.path.basename(self.grids[self.selected_grid]).replace(".txt", "").replace("grille", "Grille ")
        vides = sum(1 for r in self.preview_grid for v in r if v == 0)
        info = fonts.small.render(f"{name}  —  {vides} cases vides", True, TEXT_MUTED)
        self.surface.blit(info, (px, py))

        gy = py + SP_L + SP_S

        # Cases
        for r in range(9):
            for c in range(9):
                x = px + c * cell
                y = gy + r * cell
                rect = pygame.Rect(x, y, cell, cell)
                pygame.draw.rect(self.surface, (245, 245, 245), rect)

                val = self.preview_grid[r][c]
                if val != 0:
                    text = fonts.button.render(str(val), True, (30, 30, 30))
                    self.surface.blit(text, text.get_rect(center=rect.center))

        # Lignes
        for i in range(10):
            is_block = (i % 3 == 0)
            color = (100, 100, 105) if is_block else (200, 200, 200)
            width = 2 if is_block else 1
            pygame.draw.line(self.surface, color,
                             (px, gy + i * cell), (px + grid_size, gy + i * cell), width)
            pygame.draw.line(self.surface, color,
                             (px + i * cell, gy), (px + i * cell, gy + grid_size), width)

    # =====================================================================
    # EVENTS
    # =====================================================================

    def handle_event(self, event):
        if self.btn_import.handle_event(event):
            self._import_grid()
            return None

        # Scroll
        if self.btn_scroll_up.handle_event(event):
            self.scroll_offset = max(0, self.scroll_offset - 1)
        if self.btn_scroll_down.handle_event(event):
            if self.scroll_offset + self.max_visible_grids < len(self.grids):
                self.scroll_offset += 1

        # Molette souris
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.y < 0:
                if self.scroll_offset + self.max_visible_grids < len(self.grids):
                    self.scroll_offset += 1

        # Clic sur un bouton de grille
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn_rect, idx in self.grid_buttons:
                if btn_rect.collidepoint(event.pos):
                    if idx != self.selected_grid:
                        self.selected_grid = idx
                        self._load_preview()

        grid_path = self.grids[self.selected_grid] if self.grids else None

        if self.btn_backtracking.handle_event(event):
            return ("backtracking", grid_path)
        if self.btn_brute_force.handle_event(event):
            return ("brute_force", grid_path)
        if self.btn_compare.handle_event(event):
            return ("compare", grid_path)
        if self.btn_play.handle_event(event):
            return ("play", grid_path)
        if self.btn_export.handle_event(event):
            return ("export", grid_path)
        return None
