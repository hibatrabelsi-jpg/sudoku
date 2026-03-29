"""
Composants UI reutilisables : boutons, labels, panneaux.
"""

import pygame
from gui.constants import *


class Button:
    """Bouton cliquable avec effet de survol"""

    def __init__(self, x, y, width, height, text, font_size=FONT_SIZE_BUTTON):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, font_size)
        self.hovered = False

    def draw(self, surface):
        """Dessine le bouton"""
        bg = BTN_BG_HOVER if self.hovered else BTN_BG
        border = BTN_BORDER_HOVER if self.hovered else BTN_BORDER

        # Fond avec coins arrondis
        pygame.draw.rect(surface, bg, self.rect, border_radius=8)
        pygame.draw.rect(surface, border, self.rect, width=1, border_radius=8)

        # Texte centre
        text_surf = self.font.render(self.text, True, BTN_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        """Gere les evenements souris. Retourne True si clique."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Label:
    """Texte simple affiche a une position donnee"""

    def __init__(self, x, y, text, color=TEXT_PRIMARY, font_size=FONT_SIZE_BODY, bold=False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(FONT_NAME, font_size, bold=bold)

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, (self.x, self.y))

    def update_text(self, new_text):
        self.text = new_text


class StatPanel:
    """Panneau d'affichage des statistiques"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.font_label = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
        self.font_value = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY, bold=True)
        self.stats = {}

    def update(self, stats):
        """Met a jour les stats affichees"""
        self.stats = stats

    def draw(self, surface):
        """Dessine le panneau avec les stats"""
        if not self.stats:
            return

        # Fond du panneau
        panel_height = 30 + len(self._get_lines()) * 28
        rect = pygame.Rect(self.x, self.y, self.width, panel_height)
        pygame.draw.rect(surface, STAT_BG, rect, border_radius=10)
        pygame.draw.rect(surface, STAT_BORDER, rect, width=1, border_radius=10)

        # Titre
        methode = self.stats.get("methode", "").replace("_", " ").title()
        title = self.font_value.render(methode, True, TEXT_TITLE)
        surface.blit(title, (self.x + 15, self.y + 10))

        # Lignes de stats
        y = self.y + 40
        for label, value in self._get_lines():
            label_surf = self.font_label.render(label, True, TEXT_SECONDARY)
            value_surf = self.font_value.render(str(value), True, TEXT_PRIMARY)
            surface.blit(label_surf, (self.x + 15, y))
            surface.blit(value_surf, (self.x + self.width - 15 - value_surf.get_width(), y))
            y += 28

    def _get_lines(self):
        """Prepare les lignes a afficher"""
        s = self.stats
        lines = [
            ("Cases vides", str(s.get("cases_vides_initiales", 0))),
            ("Iterations", f"{s.get('iterations', 0):,}".replace(",", " ")),
            ("Verifications", f"{s.get('verifications', 0):,}".replace(",", " ")),
        ]
        if s.get("methode") == "backtracking":
            lines.append(("Backtracks", f"{s.get('backtracks', 0):,}".replace(",", " ")))

        temps = s.get("temps_execution", 0)
        if temps < 1:
            lines.append(("Temps", f"{temps*1000:.1f} ms"))
        else:
            lines.append(("Temps", f"{temps:.3f} s"))

        mem = s.get("memoire_max", 0)
        if mem > 0:
            kb = mem / 1024
            mem_str = f"{kb:.1f} Ko" if kb < 1024 else f"{kb/1024:.2f} Mo"
            lines.append(("Memoire max", mem_str))

        return lines
