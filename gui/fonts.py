"""
Chargement des polices personnalisees.
Comucan pour les titres, Creato Display pour le contenu.
Fallback sur la police systeme si les fichiers ne sont pas trouves.
"""

import os
import pygame
from gui.constants import *


class Fonts:
    """Gestionnaire de polices pour toute l'application"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def load(self):
        """Charge toutes les polices (a appeler apres pygame.init)"""
        if self._loaded:
            return
        self._loaded = True

        # Titres — Comucan
        self.hero = self._load(FONT_TITLE_PATH, FONT_SIZE_HERO)
        self.title = self._load(FONT_TITLE_PATH, FONT_SIZE_TITLE)

        # Contenu — Creato Display
        self.subtitle = self._load(FONT_MEDIUM_PATH, FONT_SIZE_SUBTITLE)
        self.body = self._load(FONT_REGULAR_PATH, FONT_SIZE_BODY)
        self.body_bold = self._load(FONT_BOLD_PATH, FONT_SIZE_BODY)
        self.small = self._load(FONT_REGULAR_PATH, FONT_SIZE_SMALL)
        self.small_bold = self._load(FONT_BOLD_PATH, FONT_SIZE_SMALL)
        self.light = self._load(FONT_LIGHT_PATH, FONT_SIZE_BODY)
        self.button = self._load(FONT_MEDIUM_PATH, FONT_SIZE_BUTTON)
        self.big = self._load(FONT_BOLD_PATH, FONT_SIZE_HERO)  # gros chiffres

        # Cases de la grille
        self.cell = self._load(FONT_MEDIUM_PATH, FONT_SIZE_CELL)
        self.cell_bold = self._load(FONT_BOLD_PATH, FONT_SIZE_CELL)

    def _load(self, path, size):
        """Charge une police avec fallback"""
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except Exception as e:
                print(f"[FONTS] Erreur chargement {path}: {e}")

        return pygame.font.SysFont(FONT_FALLBACK, size)


# Instance globale
fonts = Fonts()
