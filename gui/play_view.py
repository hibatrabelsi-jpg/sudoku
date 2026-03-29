"""
Ecran de jeu : permet a l'utilisateur de jouer au Sudoku.
Selection de case au clic, saisie au clavier, verification en temps reel.
"""

import pygame
from gui.constants import *
from gui.grid_view import GridView
from gui.components import Button


class PlayView:
    """Mode jeu interactif"""

    def __init__(self, surface):
        self.surface = surface
        self.grid_view = GridView(surface)

        self.font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SUBTITLE, bold=True)
        self.font_body = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY)
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
        self.font_big = pygame.font.SysFont(FONT_NAME, 40, bold=True)

        # Boutons
        self.btn_clear = Button(PANEL_X, 400, PANEL_WIDTH, 40, "Effacer la case")
        self.btn_reset = Button(PANEL_X, 455, PANEL_WIDTH, 40, "Reinitialiser la grille")
        self.btn_solve = Button(PANEL_X, 510, PANEL_WIDTH, 40, "Voir la solution")
        self.btn_menu = Button(PANEL_X, 580, PANEL_WIDTH, 40, "Retour au menu")

        # Etat du jeu
        self.grid = [[0] * 9 for _ in range(9)]
        self.initial_grid = [[0] * 9 for _ in range(9)]
        self.selected = None         # (row, col) de la case selectionnee
        self.errors = set()          # set de (row, col) en erreur
        self.completed = False       # True quand la grille est finie et valide
        self.show_solution = False
        self.solution = [[0] * 9 for _ in range(9)]

    def setup(self, grid_obj):
        """Configure le jeu avec une grille"""
        self.grid = [row[:] for row in grid_obj.grid]
        self.initial_grid = [row[:] for row in grid_obj.initial_grid]
        self.selected = None
        self.errors = set()
        self.completed = False
        self.show_solution = False

        # Calculer la solution pour le bouton "Voir la solution"
        grid_obj.reset()
        grid_obj.solve_backtracking()
        self.solution = [row[:] for row in grid_obj.grid]
        grid_obj.reset()

    def draw(self):
        """Dessine l'ecran de jeu"""
        # Titre
        title = self.font_title.render("Mode jeu", True, TEXT_TITLE)
        self.surface.blit(title, (GRID_OFFSET_X, 30))

        if self.show_solution:
            note = self.font_small.render("Solution affichee", True, TEXT_SECONDARY)
            self.surface.blit(note, (GRID_OFFSET_X + 140, 36))

        # Grille
        grid_to_draw = self.solution if self.show_solution else self.grid
        self._draw_game_grid(grid_to_draw)

        # Panneau lateral
        self._draw_side_panel()

        # Message de victoire
        if self.completed:
            self._draw_victory()

        # Boutons
        self.btn_clear.draw(self.surface)
        self.btn_reset.draw(self.surface)
        self.btn_solve.draw(self.surface)
        self.btn_menu.draw(self.surface)

    def _draw_game_grid(self, grid):
        """Dessine la grille avec la selection et les erreurs"""
        for r in range(9):
            for c in range(9):
                x = GRID_OFFSET_X + c * CELL_SIZE
                y = GRID_OFFSET_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                # Fond de la case
                if (r, c) in self.errors:
                    pygame.draw.rect(self.surface, CELL_ERROR, rect)
                elif self.selected == (r, c):
                    pygame.draw.rect(self.surface, CELL_SELECTED, rect)
                elif self.selected and (r == self.selected[0] or c == self.selected[1]):
                    # Surligner la ligne et colonne de la case selectionnee
                    pygame.draw.rect(self.surface, (235, 240, 248), rect)
                else:
                    pygame.draw.rect(self.surface, CELL_NORMAL, rect)

                # Chiffre
                val = grid[r][c]
                if val != 0:
                    is_initial = self.initial_grid[r][c] != 0
                    if is_initial:
                        font = self.grid_view.font_cell_bold
                        color = TEXT_INITIAL
                    elif (r, c) in self.errors:
                        font = self.grid_view.font_cell
                        color = (200, 60, 60)
                    else:
                        font = self.grid_view.font_cell
                        color = TEXT_USER

                    text = font.render(str(val), True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.surface.blit(text, text_rect)

        # Lignes de la grille
        self.grid_view._draw_lines()

    def _draw_side_panel(self):
        """Dessine les informations a droite"""
        x = PANEL_X
        y = PANEL_Y

        # Compteur de cases remplies
        filled = sum(1 for r in range(9) for c in range(9) if self.grid[r][c] != 0)
        total = 81
        empty_initial = sum(1 for r in range(9) for c in range(9) if self.initial_grid[r][c] == 0)
        filled_by_player = filled - (total - empty_initial)

        progress = self.font_body.render(f"Progression", True, TEXT_PRIMARY)
        self.surface.blit(progress, (x, y))

        detail = self.font_small.render(
            f"{filled_by_player} / {empty_initial} cases remplies", True, TEXT_SECONDARY)
        self.surface.blit(detail, (x, y + 28))

        # Barre de progression
        bar_rect = pygame.Rect(x, y + 55, PANEL_WIDTH, 12)
        pygame.draw.rect(self.surface, REPLAY_BAR_BG, bar_rect, border_radius=6)
        if empty_initial > 0:
            fill_w = int((filled_by_player / empty_initial) * PANEL_WIDTH)
            if fill_w > 0:
                fill_rect = pygame.Rect(x, y + 55, fill_w, 12)
                color = (60, 150, 60) if not self.errors else (200, 80, 80)
                pygame.draw.rect(self.surface, color, fill_rect, border_radius=6)

        # Erreurs
        err_y = y + 90
        if self.errors:
            err_text = self.font_body.render(
                f"{len(self.errors)} erreur(s)", True, (200, 60, 60))
            self.surface.blit(err_text, (x, err_y))
        else:
            ok_text = self.font_body.render("Aucune erreur", True, (60, 150, 60))
            self.surface.blit(ok_text, (x, err_y))

        # Instructions
        inst_y = y + 150
        instructions = [
            "Cliquer sur une case vide",
            "Taper un chiffre (1-9)",
            "Suppr pour effacer",
            "Fleches pour naviguer",
        ]
        title_inst = self.font_body.render("Comment jouer", True, TEXT_PRIMARY)
        self.surface.blit(title_inst, (x, inst_y))
        for i, line in enumerate(instructions):
            txt = self.font_small.render(line, True, TEXT_SECONDARY)
            self.surface.blit(txt, (x, inst_y + 28 + i * 22))

    def _draw_victory(self):
        """Dessine le message de victoire"""
        # Fond semi-transparent
        overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.surface.blit(overlay, (GRID_OFFSET_X, GRID_OFFSET_Y))

        # Texte
        msg = self.font_big.render("Bravo !", True, (60, 150, 60))
        msg_rect = msg.get_rect(
            centerx=GRID_OFFSET_X + GRID_SIZE // 2,
            centery=GRID_OFFSET_Y + GRID_SIZE // 2 - 20)
        self.surface.blit(msg, msg_rect)

        sub = self.font_body.render("La grille est correctement remplie", True, TEXT_SECONDARY)
        sub_rect = sub.get_rect(
            centerx=GRID_OFFSET_X + GRID_SIZE // 2,
            centery=GRID_OFFSET_Y + GRID_SIZE // 2 + 25)
        self.surface.blit(sub, sub_rect)

    def handle_event(self, event):
        """
        Gere les evenements du mode jeu.
        Retourne "menu" pour revenir au menu, None sinon.
        """
        # Boutons
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

        # Clic sur la grille
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.grid_view.get_cell_at(*event.pos)
            if cell:
                r, c = cell
                # On ne peut selectionner que les cases non initiales
                if self.initial_grid[r][c] == 0:
                    self.selected = cell
                else:
                    self.selected = cell  # on peut selectionner pour voir mais pas modifier

        # Saisie clavier
        if event.type == pygame.KEYDOWN and self.selected:
            r, c = self.selected

            # Chiffre 1-9
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                if self.initial_grid[r][c] == 0:
                    num = event.key - pygame.K_0
                    self.grid[r][c] = num
                    self._check_errors()
                    self._check_completion()

            # Pave numerique 1-9
            elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
                if self.initial_grid[r][c] == 0:
                    num = event.key - pygame.K_KP0
                    self.grid[r][c] = num
                    self._check_errors()
                    self._check_completion()

            # Effacer
            elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
                self._clear_selected()

            # Navigation au clavier
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
        """Efface la case selectionnee si elle n'est pas initiale"""
        if self.selected:
            r, c = self.selected
            if self.initial_grid[r][c] == 0:
                self.grid[r][c] = 0
                self._check_errors()

    def _check_errors(self):
        """Verifie toutes les cases remplies par le joueur et marque les erreurs"""
        self.errors = set()
        for r in range(9):
            for c in range(9):
                val = self.grid[r][c]
                if val == 0 or self.initial_grid[r][c] != 0:
                    continue

                # Temporairement retirer la valeur pour verifier
                self.grid[r][c] = 0
                conflict = False

                # Verifier ligne
                if val in self.grid[r]:
                    conflict = True

                # Verifier colonne
                if not conflict:
                    for i in range(9):
                        if self.grid[i][c] == val:
                            conflict = True
                            break

                # Verifier carre 3x3
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
        """Verifie si la grille est completement remplie et valide"""
        # Verifier qu'il n'y a pas de case vide
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return

        # Verifier qu'il n'y a pas d'erreur
        self._check_errors()
        if not self.errors:
            self.completed = True
