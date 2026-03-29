"""
Ecran de resolution : affiche la grille resolue et les statistiques.
Permet de lancer le replay.
"""

import pygame
from gui.constants import *
from gui.grid_view import GridView
from gui.components import Button, StatPanel


class ResolveScreen:
    """Ecran affichant le resultat d'une resolution"""

    def __init__(self, surface):
        self.surface = surface
        self.grid_view = GridView(surface)
        self.stat_panel = StatPanel(PANEL_X, PANEL_Y, PANEL_WIDTH)

        self.font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SUBTITLE, bold=True)
        self.font_info = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)

        # Boutons
        btn_x = PANEL_X
        btn_w = PANEL_WIDTH
        self.btn_replay = Button(btn_x, 500, btn_w, 40, "Voir le replay")
        self.btn_menu = Button(btn_x, 555, btn_w, 40, "Retour au menu")

        # Donnees
        self.grid = None
        self.initial_grid = None
        self.stats = {}
        self.method_name = ""
        self.success = False

    def setup(self, grid_obj, method_name, success):
        """Configure l'ecran avec les resultats d'une resolution"""
        self.grid = [row[:] for row in grid_obj.grid]
        self.initial_grid = [row[:] for row in grid_obj.initial_grid]
        self.stats = grid_obj.get_stats()
        self.stat_panel.update(self.stats)
        self.method_name = method_name
        self.success = success

    def draw(self):
        """Dessine l'ecran de resolution"""
        # Titre
        status = "Resolu" if self.success else "Non resolu (limite atteinte)"
        color = TEXT_TITLE if self.success else (200, 80, 80)
        title = self.font_title.render(f"{self.method_name} — {status}", True, color)
        self.surface.blit(title, (GRID_OFFSET_X, 30))

        # Grille
        self.grid_view.draw(self.grid, self.initial_grid)

        # Stats
        self.stat_panel.draw(self.surface)

        # Boutons
        self.btn_replay.draw(self.surface)
        self.btn_menu.draw(self.surface)

    def handle_event(self, event):
        """
        Retourne "replay" ou "menu" selon le bouton clique, ou None.
        """
        if self.btn_replay.handle_event(event):
            return "replay"
        if self.btn_menu.handle_event(event):
            return "menu"
        return None
