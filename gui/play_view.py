"""
Ecran de jeu : permet a l'utilisateur de jouer au Sudoku.
"""

import pygame
from gui import constants as C
from gui.constants import *
from gui.fonts import fonts
from gui.grid_view import GridView
from gui.components import Button


PASTEL_MINT = (170, 220, 200)
PASTEL_CORAL = (220, 170, 165)
PASTEL_BLUE = (160, 190, 220)


class PlayView:

    def __init__(self, surface):
        self.surface = surface
        self.grid_view = GridView(surface)

        self.btn_clear = Button(0, 0, 0, BTN_HEIGHT, "Effacer la case")
        self.btn_reset = Button(0, 0, 0, BTN_HEIGHT, "Reinitialiser")
        self.btn_solve = Button(0, 0, 0, BTN_HEIGHT, "Voir la solution")
        self.btn_menu = Button(0, 0, 0, BTN_HEIGHT, "Retour au menu")

        self.grid = [[0] * 9 for _ in range(9)]
        self.initial_grid = [[0] * 9 for _ in range(9)]
        self.selected = None
        self.errors = set()
        self.completed = False
        self.show_solution = False
        self.solution = [[0] * 9 for _ in range(9)]

    def setup(self, grid_obj):
        self.grid = [row[:] for row in grid_obj.grid]
        self.initial_grid = [row[:] for row in grid_obj.initial_grid]
        self.selected = None
        self.errors = set()
        self.completed = False
        self.show_solution = False
        grid_obj.reset()
        grid_obj.solve_backtracking()
        self.solution = [row[:] for row in grid_obj.grid]
        grid_obj.reset()

    def draw(self):
        # Titre — en haut a gauche de la fenetre
        title = fonts.title.render("Mode jeu", True, TEXT_TITLE)
        self.surface.blit(title, (SP_XXL, SP_L + SP_S))

        if self.show_solution:
            note = fonts.body.render("Solution affichee", True, TEXT_MUTED)
            self.surface.blit(note, (SP_XXL + title.get_width() + SP_M, SP_L + SP_M))

        grid_to_draw = self.solution if self.show_solution else self.grid
        self._draw_game_grid(grid_to_draw)
        self._draw_side_panel()

        if self.completed:
            self._draw_victory()

        # Boutons — panneau droit, alignes depuis le bas de la grille
        grid_bottom = C.GRID_OFFSET_Y + GRID_SIZE
        pw = C.PANEL_WIDTH
        btn_gap = SP_M

        self.btn_menu.rect = pygame.Rect(C.PANEL_X, grid_bottom - BTN_HEIGHT, pw, BTN_HEIGHT)
        self.btn_solve.rect = pygame.Rect(C.PANEL_X, grid_bottom - BTN_HEIGHT * 2 - btn_gap, pw, BTN_HEIGHT)
        self.btn_reset.rect = pygame.Rect(C.PANEL_X, grid_bottom - BTN_HEIGHT * 3 - btn_gap * 2, pw, BTN_HEIGHT)
        self.btn_clear.rect = pygame.Rect(C.PANEL_X, grid_bottom - BTN_HEIGHT * 4 - btn_gap * 3, pw, BTN_HEIGHT)

        self.btn_clear.draw(self.surface)
        self.btn_reset.draw(self.surface)
        self.btn_solve.draw(self.surface)

        # Retour efface
        mr = self.btn_menu.rect
        bc = (55, 55, 58) if not self.btn_menu.hovered else (80, 80, 85)
        pygame.draw.rect(self.surface, BG_COLOR, mr, border_radius=BTN_RADIUS)
        pygame.draw.rect(self.surface, bc, mr, width=1, border_radius=BTN_RADIUS)
        mt = fonts.small.render(self.btn_menu.text, True, TEXT_HINT)
        self.surface.blit(mt, mt.get_rect(center=mr.center))

    def _draw_game_grid(self, grid):
        for r in range(9):
            for c in range(9):
                x = C.GRID_OFFSET_X + c * CELL_SIZE
                y = C.GRID_OFFSET_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if (r, c) in self.errors:
                    pygame.draw.rect(self.surface, CELL_ERROR, rect)
                elif self.selected == (r, c):
                    pygame.draw.rect(self.surface, CELL_SELECTED, rect)
                elif self.selected and (r == self.selected[0] or c == self.selected[1]):
                    pygame.draw.rect(self.surface, CELL_ROW_COL, rect)
                else:
                    pygame.draw.rect(self.surface, CELL_NORMAL, rect)

                val = grid[r][c]
                if val != 0:
                    is_initial = self.initial_grid[r][c] != 0
                    if is_initial:
                        font = fonts.cell_bold
                        color = TEXT_INITIAL
                    elif (r, c) in self.errors:
                        font = fonts.cell
                        color = TEXT_ERROR
                    else:
                        font = fonts.cell
                        color = TEXT_USER

                    text = font.render(str(val), True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.surface.blit(text, text_rect)

        self.grid_view._draw_lines()

    def _draw_side_panel(self):
        px = C.PANEL_X
        py = C.PANEL_Y
        pw = C.PANEL_WIDTH

        filled = sum(1 for r in range(9) for c in range(9) if self.grid[r][c] != 0)
        empty_initial = sum(1 for r in range(9) for c in range(9) if self.initial_grid[r][c] == 0)
        filled_by_player = filled - (81 - empty_initial)

        y = py

        # Progression
        p_label = fonts.small.render("PROGRESSION", True, TEXT_HINT)
        self.surface.blit(p_label, (px, y))
        p_val = fonts.big.render(f"{filled_by_player}", True, TEXT_LIGHT)
        self.surface.blit(p_val, (px, y + SP_L))
        p_total = fonts.body.render(f"/ {empty_initial} cases", True, TEXT_HINT)
        self.surface.blit(p_total, (px + p_val.get_width() + SP_S, y + SP_XL + SP_M))

        # Barre
        bar_y = y + SP_XXXL
        bg = pygame.Surface((pw, 6), pygame.SRCALPHA)
        bg.fill((255, 255, 255, 15))
        self.surface.blit(bg, (px, bar_y))
        if empty_initial > 0:
            fill_w = int((filled_by_player / empty_initial) * pw)
            if fill_w > 0:
                color = PASTEL_MINT if not self.errors else PASTEL_CORAL
                fill = pygame.Surface((fill_w, 6), pygame.SRCALPHA)
                fill.fill((*color, 160))
                self.surface.blit(fill, (px, bar_y))

        # Separateur
        sep_y = bar_y + SP_L
        sep = pygame.Surface((pw, 1), pygame.SRCALPHA)
        sep.fill((255, 255, 255, 20))
        self.surface.blit(sep, (px, sep_y))

        # Erreurs
        y = sep_y + SP_L
        err_label = fonts.small.render("STATUT", True, TEXT_HINT)
        self.surface.blit(err_label, (px, y))
        if self.errors:
            err_val = fonts.subtitle.render(f"{len(self.errors)} erreur(s)", True, PASTEL_CORAL)
        else:
            err_val = fonts.subtitle.render("Aucune erreur", True, PASTEL_MINT)
        self.surface.blit(err_val, (px, y + SP_L))

        # Separateur
        sep2_y = y + SP_XXL + SP_S
        sep2 = pygame.Surface((pw, 1), pygame.SRCALPHA)
        sep2.fill((255, 255, 255, 20))
        self.surface.blit(sep2, (px, sep2_y))

        # Instructions
        y = sep2_y + SP_L
        inst_label = fonts.small.render("COMMENT JOUER", True, TEXT_HINT)
        self.surface.blit(inst_label, (px, y))
        instructions = [
            "Cliquer sur une case vide",
            "Taper un chiffre (1-9)",
            "Suppr pour effacer",
            "Fleches pour naviguer",
        ]
        for i, line in enumerate(instructions):
            txt = fonts.body.render(line, True, TEXT_MUTED)
            self.surface.blit(txt, (px, y + SP_XL + i * (SP_L + SP_S)))

    def _draw_victory(self):
        overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        overlay.fill((17, 17, 17, 200))
        self.surface.blit(overlay, (C.GRID_OFFSET_X, C.GRID_OFFSET_Y))

        msg = fonts.hero.render("Bravo !", True, TEXT_TITLE)
        msg_rect = msg.get_rect(
            centerx=C.GRID_OFFSET_X + GRID_SIZE // 2,
            centery=C.GRID_OFFSET_Y + GRID_SIZE // 2 - SP_L)
        self.surface.blit(msg, msg_rect)

        sub = fonts.body.render("La grille est correctement remplie", True, TEXT_MUTED)
        sub_rect = sub.get_rect(
            centerx=C.GRID_OFFSET_X + GRID_SIZE // 2,
            centery=C.GRID_OFFSET_Y + GRID_SIZE // 2 + SP_XL)
        self.surface.blit(sub, sub_rect)

    def handle_event(self, event):
        if self.btn_menu.handle_event(event):
            return "menu"
        if self.btn_clear.handle_event(event):
            self._clear_selected()
        if self.btn_reset.handle_event(event):
            self.grid = [row[:] for row in self.initial_grid]
            self.selected = None
            self.errors = set()
            self.completed = False
            self.show_solution = False
        if self.btn_solve.handle_event(event):
            self.show_solution = not self.show_solution

        if self.show_solution or self.completed:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.grid_view.get_cell_at(*event.pos)
            if cell:
                self.selected = cell

        if event.type == pygame.KEYDOWN and self.selected:
            r, c = self.selected
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                if self.initial_grid[r][c] == 0:
                    self.grid[r][c] = event.key - pygame.K_0
                    self._check_errors()
                    self._check_completion()
            elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
                if self.initial_grid[r][c] == 0:
                    self.grid[r][c] = event.key - pygame.K_KP0
                    self._check_errors()
                    self._check_completion()
            elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
                self._clear_selected()
            elif event.key == pygame.K_UP and r > 0:
                self.selected = (r - 1, c)
            elif event.key == pygame.K_DOWN and r < 8:
                self.selected = (r + 1, c)
            elif event.key == pygame.K_LEFT and c > 0:
                self.selected = (r, c - 1)
            elif event.key == pygame.K_RIGHT and c < 8:
                self.selected = (r, c + 1)

        return None

    def _clear_selected(self):
        if self.selected:
            r, c = self.selected
            if self.initial_grid[r][c] == 0:
                self.grid[r][c] = 0
                self._check_errors()

    def _check_errors(self):
        self.errors = set()
        for r in range(9):
            for c in range(9):
                val = self.grid[r][c]
                if val == 0 or self.initial_grid[r][c] != 0:
                    continue
                self.grid[r][c] = 0
                conflict = False
                if val in self.grid[r]:
                    conflict = True
                if not conflict:
                    for i in range(9):
                        if self.grid[i][c] == val:
                            conflict = True
                            break
                if not conflict:
                    sr, sc = (r // 3) * 3, (c // 3) * 3
                    for i in range(3):
                        for j in range(3):
                            if self.grid[sr + i][sc + j] == val:
                                conflict = True
                                break
                        if conflict:
                            break
                self.grid[r][c] = val
                if conflict:
                    self.errors.add((r, c))

    def _check_completion(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return
        self._check_errors()
        if not self.errors:
            self.completed = True
