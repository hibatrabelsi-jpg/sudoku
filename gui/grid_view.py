"""
Affichage de la grille de Sudoku dans Pygame.
"""

import pygame
from gui import constants as C
from gui.constants import CELL_SIZE, GRID_SIZE, CELL_NORMAL, GRID_LINE_THIN, GRID_LINE_THICK, TEXT_INITIAL, TEXT_SOLVED
from gui.fonts import fonts


class GridView:

    def __init__(self, surface):
        self.surface = surface
        self.highlight_cell = None
        self.highlight_color = None

    def draw(self, grid, initial_grid):
        self._draw_cells(grid, initial_grid)
        self._draw_lines()

    def _draw_cells(self, grid, initial_grid):
        for r in range(9):
            for c in range(9):
                x = C.GRID_OFFSET_X + c * CELL_SIZE
                y = C.GRID_OFFSET_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if self.highlight_cell == (r, c) and self.highlight_color:
                    pygame.draw.rect(self.surface, self.highlight_color, rect)
                else:
                    pygame.draw.rect(self.surface, CELL_NORMAL, rect)

                val = grid[r][c]
                if val != 0:
                    is_initial = initial_grid[r][c] != 0
                    if is_initial:
                        font = fonts.cell_bold
                        color = TEXT_INITIAL
                    else:
                        font = fonts.cell
                        color = TEXT_SOLVED

                    text = font.render(str(val), True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.surface.blit(text, text_rect)

    def _draw_lines(self):
        for i in range(10):
            is_thick = (i % 3 == 0)
            color = GRID_LINE_THICK if is_thick else GRID_LINE_THIN
            width = 3 if is_thick else 1

            y = C.GRID_OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(self.surface, color,
                             (C.GRID_OFFSET_X, y), (C.GRID_OFFSET_X + GRID_SIZE, y), width)

            x = C.GRID_OFFSET_X + i * CELL_SIZE
            pygame.draw.line(self.surface, color,
                             (x, C.GRID_OFFSET_Y), (x, C.GRID_OFFSET_Y + GRID_SIZE), width)

    def set_highlight(self, row, col, color):
        self.highlight_cell = (row, col)
        self.highlight_color = color

    def clear_highlight(self):
        self.highlight_cell = None
        self.highlight_color = None

    def get_cell_at(self, mouse_x, mouse_y):
        if (mouse_x < C.GRID_OFFSET_X or mouse_x >= C.GRID_OFFSET_X + GRID_SIZE or
                mouse_y < C.GRID_OFFSET_Y or mouse_y >= C.GRID_OFFSET_Y + GRID_SIZE):
            return None
        col = (mouse_x - C.GRID_OFFSET_X) // CELL_SIZE
        row = (mouse_y - C.GRID_OFFSET_Y) // CELL_SIZE
        return (row, col)
