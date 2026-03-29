"""
Ecran du menu principal.
"""

import pygame
import os
from gui.constants import *
from gui.components import Button, Label


class MenuScreen:
    """Menu principal avec selection de grille et choix de methode"""

    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE, bold=True)
        self.font_sub = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SUBTITLE)
        self.font_body = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY)

        # Detecter les grilles disponibles
        self.grids = self._find_grids()
        self.selected_grid = 0  # index de la grille selectionnee

        # Boutons de grille
        self.grid_buttons = []
        self._build_grid_buttons()

        # Boutons d'action
        btn_y = 420
        btn_w = 280
        btn_h = 45
        btn_x = (WINDOW_WIDTH - btn_w) // 2

        self.btn_backtracking = Button(btn_x, btn_y, btn_w, btn_h, "Resoudre (Backtracking)")
        self.btn_brute_force = Button(btn_x, btn_y + 60, btn_w, btn_h, "Resoudre (Force Brute)")
        self.btn_compare = Button(btn_x, btn_y + 120, btn_w, btn_h, "Comparer les deux")
        self.btn_play = Button(btn_x, btn_y + 180, btn_w, btn_h, "Jouer")

    def _find_grids(self):
        """Trouve les fichiers de grilles dans data/"""
        grid_dir = "data"
        if not os.path.exists(grid_dir):
            return []
        files = sorted([f for f in os.listdir(grid_dir) if f.endswith(".txt")])
        return [os.path.join(grid_dir, f) for f in files]

    def _build_grid_buttons(self):
        """Cree les boutons de selection de grille"""
        self.grid_buttons = []
        start_x = (WINDOW_WIDTH - (len(self.grids) * 80 + (len(self.grids) - 1) * 10)) // 2
        for i, path in enumerate(self.grids):
            name = os.path.basename(path).replace(".txt", "").replace("grille", "Grille ")
            btn = Button(start_x + i * 90, 320, 80, 40, name, font_size=FONT_SIZE_SMALL)
            self.grid_buttons.append(btn)

    def draw(self):
        """Dessine le menu"""
        # Titre
        title = self.font_title.render("Sudoku Solver", True, TEXT_TITLE)
        title_rect = title.get_rect(centerx=WINDOW_WIDTH // 2, y=60)
        self.surface.blit(title, title_rect)

        # Sous-titre
        sub = self.font_sub.render("Analyse comparative : Force Brute vs Backtracking", True, TEXT_SECONDARY)
        sub_rect = sub.get_rect(centerx=WINDOW_WIDTH // 2, y=110)
        self.surface.blit(sub, sub_rect)

        # Ligne decorative
        line_y = 155
        line_w = 300
        pygame.draw.line(self.surface, GRID_LINE_THIN,
                         (WINDOW_WIDTH // 2 - line_w // 2, line_y),
                         (WINDOW_WIDTH // 2 + line_w // 2, line_y), 1)

        # Section selection de grille
        label = self.font_body.render("Choisir une grille :", True, TEXT_PRIMARY)
        label_rect = label.get_rect(centerx=WINDOW_WIDTH // 2, y=280)
        self.surface.blit(label, label_rect)

        # Boutons de grille
        for i, btn in enumerate(self.grid_buttons):
            if i == self.selected_grid:
                # Bouton selectionne : fond bleu leger
                pygame.draw.rect(self.surface, CELL_SELECTED, btn.rect, border_radius=8)
                pygame.draw.rect(self.surface, BTN_BORDER_HOVER, btn.rect, width=2, border_radius=8)
                text_surf = btn.font.render(btn.text, True, BTN_TEXT)
                text_rect = text_surf.get_rect(center=btn.rect.center)
                self.surface.blit(text_surf, text_rect)
            else:
                btn.draw(self.surface)

        # Boutons d'action
        self.btn_backtracking.draw(self.surface)
        self.btn_brute_force.draw(self.surface)
        self.btn_compare.draw(self.surface)
        self.btn_play.draw(self.surface)

    def handle_event(self, event):
        """
        Gere les evenements.
        Retourne un tuple (action, grid_path) ou None.
        Actions possibles : "backtracking", "brute_force", "compare", "play"
        """
        # Selection de grille
        for i, btn in enumerate(self.grid_buttons):
            if btn.handle_event(event):
                self.selected_grid = i

        # Boutons d'action
        grid_path = self.grids[self.selected_grid] if self.grids else None

        if self.btn_backtracking.handle_event(event):
            return ("backtracking", grid_path)
        if self.btn_brute_force.handle_event(event):
            return ("brute_force", grid_path)
        if self.btn_compare.handle_event(event):
            return ("compare", grid_path)
        if self.btn_play.handle_event(event):
            return ("play", grid_path)

        return None
