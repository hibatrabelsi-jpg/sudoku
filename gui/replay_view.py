"""
Ecran de replay : visualisation etape par etape de la resolution.
Utilise les snapshots complets pour une navigation libre et instantanee.
"""

import pygame
from gui.constants import *
from gui.grid_view import GridView
from gui.components import Button


class ReplayScreen:
    """Replay interactif de la resolution"""

    def __init__(self, surface):
        self.surface = surface
        self.grid_view = GridView(surface)

        self.font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SUBTITLE, bold=True)
        self.font_info = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY)
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)

        # Controles de replay
        ctrl_y = GRID_OFFSET_Y + GRID_SIZE + 30
        self.btn_prev = Button(GRID_OFFSET_X, ctrl_y, 60, 38, "<<")
        self.btn_play = Button(GRID_OFFSET_X + 70, ctrl_y, 90, 38, "Lecture")
        self.btn_next = Button(GRID_OFFSET_X + 170, ctrl_y, 60, 38, ">>")
        self.btn_slow = Button(GRID_OFFSET_X + 250, ctrl_y, 50, 38, "-")
        self.btn_fast = Button(GRID_OFFSET_X + 310, ctrl_y, 50, 38, "+")
        self.btn_menu = Button(GRID_OFFSET_X + GRID_SIZE - 130, ctrl_y, 130, 38, "Retour")

        # Barre de progression
        self.progress_rect = pygame.Rect(GRID_OFFSET_X, ctrl_y + 55, GRID_SIZE, 12)

        # Etat du replay
        self.snapshots = []
        self.initial_grid = []
        self.current_step = 0
        self.playing = False
        self.speed = REPLAY_SPEED_DEFAULT
        self.timer = 0
        self.method_name = ""
        self.dragging_progress = False

    def setup(self, snapshots, initial_grid, method_name):
        """Configure le replay avec les snapshots d'une resolution"""
        self.snapshots = snapshots
        self.initial_grid = [row[:] for row in initial_grid]
        self.current_step = 0
        self.playing = False
        self.speed = REPLAY_SPEED_DEFAULT
        self.timer = 0
        self.method_name = method_name

    def update(self, dt):
        """Met a jour l'animation du replay (appele chaque frame)"""
        if not self.playing or not self.snapshots:
            return

        self.timer += dt
        step_duration = 1.0 / self.speed

        if self.timer >= step_duration:
            self.timer -= step_duration
            if self.current_step < len(self.snapshots) - 1:
                self.current_step += 1
            else:
                self.playing = False

    def draw(self):
        """Dessine l'ecran de replay"""
        if not self.snapshots:
            return

        snap = self.snapshots[self.current_step]

        # Titre
        title = self.font_title.render(f"Replay — {self.method_name}", True, TEXT_TITLE)
        self.surface.blit(title, (GRID_OFFSET_X, 30))

        # Grille avec surbrillance
        action = snap["action"]
        color = CELL_HIGHLIGHT_PLACE if action == "placement" else CELL_HIGHLIGHT_REMOVE
        self.grid_view.set_highlight(snap["ligne"], snap["colonne"], color)
        self.grid_view.draw(snap["grille"], self.initial_grid)

        # Info sur l'etape courante
        info_x = PANEL_X
        info_y = PANEL_Y

        step_text = self.font_info.render(
            f"Etape {self.current_step + 1} / {len(self.snapshots)}", True, TEXT_PRIMARY)
        self.surface.blit(step_text, (info_x, info_y))

        action_text = "Placement" if action == "placement" else "Retrait"
        action_color = (60, 150, 60) if action == "placement" else (200, 80, 80)
        detail = self.font_info.render(
            f"{action_text} du {snap['valeur']} en ({snap['ligne']},{snap['colonne']})",
            True, action_color)
        self.surface.blit(detail, (info_x, info_y + 30))

        # Vitesse
        speed_text = self.font_small.render(f"Vitesse : {self.speed} etapes/s", True, TEXT_SECONDARY)
        self.surface.blit(speed_text, (info_x, info_y + 65))

        # Compteurs en direct
        placements = sum(1 for s in self.snapshots[:self.current_step + 1] if s["action"] == "placement")
        retraits = sum(1 for s in self.snapshots[:self.current_step + 1] if s["action"] == "retrait")

        count_y = info_y + 110
        self.font_small.set_bold(False)
        p_text = self.font_small.render(f"Placements : {placements}", True, (60, 150, 60))
        r_text = self.font_small.render(f"Retraits : {retraits}", True, (200, 80, 80))
        self.surface.blit(p_text, (info_x, count_y))
        self.surface.blit(r_text, (info_x, count_y + 25))

        # Controles
        self.btn_play.text = "Pause" if self.playing else "Lecture"
        self.btn_prev.draw(self.surface)
        self.btn_play.draw(self.surface)
        self.btn_next.draw(self.surface)
        self.btn_slow.draw(self.surface)
        self.btn_fast.draw(self.surface)
        self.btn_menu.draw(self.surface)

        # Barre de progression
        self._draw_progress_bar()

    def _draw_progress_bar(self):
        """Dessine la barre de progression cliquable"""
        # Fond
        pygame.draw.rect(self.surface, REPLAY_BAR_BG, self.progress_rect, border_radius=6)

        # Remplissage
        if len(self.snapshots) > 1:
            progress = self.current_step / (len(self.snapshots) - 1)
        else:
            progress = 1

        fill_width = int(self.progress_rect.width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(
                self.progress_rect.x, self.progress_rect.y,
                fill_width, self.progress_rect.height)
            pygame.draw.rect(self.surface, REPLAY_BAR_FILL, fill_rect, border_radius=6)

        # Curseur
        cursor_x = self.progress_rect.x + fill_width
        cursor_y = self.progress_rect.centery
        pygame.draw.circle(self.surface, REPLAY_BAR_FILL, (cursor_x, cursor_y), 8)
        pygame.draw.circle(self.surface, (255, 255, 255), (cursor_x, cursor_y), 5)

    def _set_step_from_mouse(self, mouse_x):
        """Calcule l'etape correspondant a la position de la souris sur la barre"""
        relative_x = mouse_x - self.progress_rect.x
        relative_x = max(0, min(relative_x, self.progress_rect.width))
        ratio = relative_x / self.progress_rect.width
        self.current_step = int(ratio * (len(self.snapshots) - 1))

    def handle_event(self, event):
        """
        Gere les evenements. Retourne "menu" pour revenir au menu, None sinon.
        """
        if not self.snapshots:
            return None

        # Boutons
        if self.btn_play.handle_event(event):
            self.playing = not self.playing
            if self.playing and self.current_step >= len(self.snapshots) - 1:
                self.current_step = 0

        if self.btn_prev.handle_event(event):
            self.playing = False
            self.current_step = max(0, self.current_step - 1)

        if self.btn_next.handle_event(event):
            self.playing = False
            self.current_step = min(len(self.snapshots) - 1, self.current_step + 1)

        if self.btn_slow.handle_event(event):
            self.speed = max(REPLAY_SPEED_MIN, self.speed // 2)

        if self.btn_fast.handle_event(event):
            self.speed = min(REPLAY_SPEED_MAX, self.speed * 2)

        if self.btn_menu.handle_event(event):
            self.playing = False
            return "menu"

        # Barre de progression : clic et drag
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.progress_rect.collidepoint(event.pos):
                self.dragging_progress = True
                self.playing = False
                self._set_step_from_mouse(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_progress = False

        elif event.type == pygame.MOUSEMOTION and self.dragging_progress:
            self._set_step_from_mouse(event.pos[0])

        # Raccourcis clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.playing = not self.playing
            elif event.key == pygame.K_LEFT:
                self.playing = False
                self.current_step = max(0, self.current_step - 1)
            elif event.key == pygame.K_RIGHT:
                self.playing = False
                self.current_step = min(len(self.snapshots) - 1, self.current_step + 1)
            elif event.key == pygame.K_UP:
                self.speed = min(REPLAY_SPEED_MAX, self.speed * 2)
            elif event.key == pygame.K_DOWN:
                self.speed = max(REPLAY_SPEED_MIN, self.speed // 2)

        return None
