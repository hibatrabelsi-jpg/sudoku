"""
Composants UI reutilisables : boutons, labels, panneaux.
"""

import pygame
from gui.constants import *
from gui.fonts import fonts


class Button:

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self, surface):
        bg = BTN_BG_HOVER if self.hovered else BTN_BG
        border = BTN_BORDER_HOVER if self.hovered else BTN_BORDER
        pygame.draw.rect(surface, bg, self.rect, border_radius=BTN_RADIUS)
        pygame.draw.rect(surface, border, self.rect, width=1, border_radius=BTN_RADIUS)
        text_surf = fonts.button.render(self.text, True, BTN_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Label:

    def __init__(self, x, y, text, color=TEXT_LIGHT, font_type="body"):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_type = font_type

    def draw(self, surface):
        font = getattr(fonts, self.font_type, fonts.body)
        text_surf = font.render(self.text, True, self.color)
        surface.blit(text_surf, (self.x, self.y))

    def update_text(self, new_text):
        self.text = new_text
