"""
Affichage de la grille de Sudoku dans Pygame.
Gere le dessin de la grille, des chiffres et des surbrillances.
"""

import pygame
from gui.constants import *


class GridView:
    """Composant visuel pour afficher une grille de Sudoku"""

    def __init__(self, surface):
        self.surface = surface
        self.font_cell = pygame.font.SysFont(FONT_NAME, FONT_SIZE_CELL)
        self.font_cell_bold = pygame.font.SysFont(FONT_NAME, FONT_SIZE_CELL, bold=True)

        # Case actuellement mise en surbrillance (pour le replay ou la selection)
        self.highlight_cell = None       # (row, col)
        self.highlight_color = None      # couleur de surbrillance

    def draw(self, grid, initial_grid):
        """
        Dessine la grille complete.
        grid : tableau 2D des valeurs actuelles
        initial_grid : tableau 2D des valeurs d'origine (pour la distinction visuelle)
        """
        self._draw_cells(grid, initial_grid)
        self._draw_lines()

    def _draw_cells(self, grid, initial_grid):
        """Dessine le fond des cases et les chiffres"""
        for r in range(9):
            for c in range(9):
                x = GRID_OFFSET_X + c * CELL_SIZE
                y = GRID_OFFSET_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                # Fond de la case
                if self.highlight_cell == (r, c) and self.highlight_color:
                    pygame.draw.rect(self.surface, self.highlight_color, rect)
                else:
                    pygame.draw.rect(self.surface, CELL_NORMAL, rect)

                # Chiffre
                val = grid[r][c]
                if val != 0:
                    is_initial = initial_grid[r][c] != 0
                    if is_initial:
                        font = self.font_cell_bold
                        color = TEXT_INITIAL
                    else:
                        font = self.font_cell
                        color = TEXT_SOLVED

                    text = font.render(str(val), True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.surface.blit(text, text_rect)

    def _draw_lines(self):
        """Dessine les lignes de la grille"""
        for i in range(10):
            # Lignes epaisses pour les carres 3x3
            is_thick = (i % 3 == 0)
            color = GRID_LINE_THICK if is_thick else GRID_LINE_THIN
            width = 3 if is_thick else 1

            # Lignes horizontales
            start_x = GRID_OFFSET_X
            end_x = GRID_OFFSET_X + GRID_SIZE
            y = GRID_OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(self.surface, color, (start_x, y), (end_x, y), width)

            # Lignes verticales
            x = GRID_OFFSET_X + i * CELL_SIZE
            start_y = GRID_OFFSET_Y
            end_y = GRID_OFFSET_Y + GRID_SIZE
            pygame.draw.line(self.surface, color, (x, start_y), (x, end_y), width)

    def set_highlight(self, row, col, color):
        """Met une case en surbrillance"""
        self.highlight_cell = (row, col)
        self.highlight_color = color

    def clear_highlight(self):
        """Retire la surbrillance"""
        self.highlight_cell = None
        self.highlight_color = None

    def get_cell_at(self, mouse_x, mouse_y):
        """
        Retourne (row, col) de la case cliquee, ou None si hors grille.
        Utile pour le mode jeu.
        """
        if (mouse_x < GRID_OFFSET_X or mouse_x >= GRID_OFFSET_X + GRID_SIZE or
                mouse_y < GRID_OFFSET_Y or mouse_y >= GRID_OFFSET_Y + GRID_SIZE):
            return None

        col = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
        row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE
        return (row, col)
