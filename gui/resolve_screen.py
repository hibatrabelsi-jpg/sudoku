"""
Ecran de resolution : grille resolue + statistiques.
"""

import pygame
from gui import constants as C
from gui.constants import *
from gui.fonts import fonts
from gui.grid_view import GridView
from gui.components import Button


PASTEL_BLUE = (160, 190, 220)
PASTEL_MINT = (170, 220, 200)
PASTEL_CORAL = (220, 170, 165)


class ResolveScreen:

    def __init__(self, surface):
        self.surface = surface
        self.grid_view = GridView(surface)

        self.btn_replay = Button(0, 0, 0, BTN_HEIGHT, "Voir le replay")
        self.btn_menu = Button(0, 0, 0, BTN_HEIGHT, "Retour au menu")

        self.grid = None
        self.initial_grid = None
        self.stats = {}
        self.method_name = ""
        self.success = False

    def setup(self, grid_obj, method_name, success):
        self.grid = [row[:] for row in grid_obj.grid]
        self.initial_grid = [row[:] for row in grid_obj.initial_grid]
        self.stats = grid_obj.get_stats()
        self.method_name = method_name
        self.success = success

    def draw(self):
        # Titre — en haut a gauche de la fenetre
        title = fonts.title.render(self.method_name, True, TEXT_TITLE)
        self.surface.blit(title, (SP_XXL, SP_L + SP_S))

        status = "Resolu" if self.success else "Non resolu (limite atteinte)"
        color = PASTEL_MINT if self.success else PASTEL_CORAL
        status_surf = fonts.body.render(status, True, color)
        self.surface.blit(status_surf, (SP_XXL + title.get_width() + SP_M, SP_L + SP_M))

        # Grille
        self.grid_view.clear_highlight()
        self.grid_view.draw(self.grid, self.initial_grid)

        # Stats panel
        self._draw_stats_panel()

        # Boutons
        grid_bottom = C.GRID_OFFSET_Y + GRID_SIZE
        self.btn_replay.rect = pygame.Rect(C.PANEL_X, grid_bottom - BTN_HEIGHT * 2 - SP_L, C.PANEL_WIDTH, BTN_HEIGHT)
        self.btn_menu.rect = pygame.Rect(C.PANEL_X, grid_bottom - BTN_HEIGHT, C.PANEL_WIDTH, BTN_HEIGHT)

        self.btn_replay.draw(self.surface)

        # Retour efface
        mr = self.btn_menu.rect
        bc = (55, 55, 58) if not self.btn_menu.hovered else (80, 80, 85)
        pygame.draw.rect(self.surface, BG_COLOR, mr, border_radius=BTN_RADIUS)
        pygame.draw.rect(self.surface, bc, mr, width=1, border_radius=BTN_RADIUS)
        mt = fonts.small.render(self.btn_menu.text, True, TEXT_HINT)
        self.surface.blit(mt, mt.get_rect(center=mr.center))

    def _draw_stats_panel(self):
        px = C.PANEL_X
        py = C.PANEL_Y
        pw = C.PANEL_WIDTH
        s = self.stats

        methode = s.get("methode", "").replace("_", " ").title()
        m_label = fonts.small.render("METHODE", True, TEXT_HINT)
        self.surface.blit(m_label, (px, py))
        m_val = fonts.subtitle.render(methode, True, TEXT_LIGHT)
        self.surface.blit(m_val, (px, py + SP_L))

        sep_y = py + SP_XXL + SP_S
        sep = pygame.Surface((pw, 1), pygame.SRCALPHA)
        sep.fill((255, 255, 255, 20))
        self.surface.blit(sep, (px, sep_y))

        lines = self._get_lines()
        y = sep_y + SP_L
        for label, value, color in lines:
            lbl = fonts.small.render(label, True, TEXT_HINT)
            self.surface.blit(lbl, (px, y))
            val = fonts.body_bold.render(str(value), True, color)
            self.surface.blit(val, (px + pw - val.get_width(), y))
            y += SP_XL

    def _get_lines(self):
        s = self.stats
        lines = [
            ("CASES VIDES", str(s.get("cases_vides_initiales", 0)), TEXT_LIGHT),
            ("ITERATIONS", f"{s.get('iterations', 0):,}".replace(",", " "), PASTEL_BLUE),
            ("VERIFICATIONS", f"{s.get('verifications', 0):,}".replace(",", " "), PASTEL_BLUE),
        ]
        if s.get("methode") == "backtracking":
            lines.append(("BACKTRACKS", f"{s.get('backtracks', 0):,}".replace(",", " "), PASTEL_CORAL))

        temps = s.get("temps_execution", 0)
        t_str = f"{temps*1000:.1f} ms" if temps < 1 else f"{temps:.3f} s"
        lines.append(("TEMPS", t_str, PASTEL_MINT))

        mem = s.get("memoire_max", 0)
        if mem > 0:
            kb = mem / 1024
            m_str = f"{kb:.1f} Ko" if kb < 1024 else f"{kb/1024:.2f} Mo"
            lines.append(("MEMOIRE", m_str, (185, 175, 215)))

        return lines

    def handle_event(self, event):
        if self.btn_replay.handle_event(event):
            return "replay"
        if self.btn_menu.handle_event(event):
            return "menu"
        return None
