"""
Ecran de replay : grille + dashboard lateral + controles.
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
PASTEL_LAVENDER = (185, 175, 215)


class ReplayScreen:

    def __init__(self, surface):
        self.surface = surface
        self.grid_view = GridView(surface)

        self.btn_start = Button(0, 0, 44, 36, "|<")
        self.btn_prev = Button(0, 0, 44, 36, "<")
        self.btn_play = Button(0, 0, 90, 36, "Lecture")
        self.btn_next = Button(0, 0, 44, 36, ">")
        self.btn_end = Button(0, 0, 44, 36, ">|")
        self.btn_slow = Button(0, 0, 44, 36, "-")
        self.btn_fast = Button(0, 0, 44, 36, "+")
        self.btn_menu = Button(0, 0, 110, 36, "Retour")

        self.snapshots = []
        self.initial_grid = []
        self.current_step = 0
        self.playing = False
        self.speed = REPLAY_SPEED_DEFAULT
        self.timer = 0
        self.method_name = ""
        self.dragging_progress = False
        self.progress_rect = pygame.Rect(0, 0, 0, 8)

    def setup(self, snapshots, initial_grid, method_name):
        self.snapshots = snapshots
        self.initial_grid = [row[:] for row in initial_grid]
        self.current_step = 0
        self.playing = False
        self.speed = REPLAY_SPEED_DEFAULT
        self.timer = 0
        self.method_name = method_name

    def update(self, dt):
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
        if not self.snapshots:
            return

        snap = self.snapshots[self.current_step]
        total = len(self.snapshots)
        action = snap["action"]

        # Titre — en haut a gauche de la fenetre
        title = fonts.title.render("Replay", True, TEXT_TITLE)
        self.surface.blit(title, (SP_XXL, SP_L + SP_S))

        method_label = fonts.subtitle.render(
            f"—  {self.method_name}", True, TEXT_MUTED)
        self.surface.blit(method_label, (
            SP_XXL + title.get_width() + SP_M, SP_L + SP_M))

        # Grille
        highlight_color = CELL_HIGHLIGHT_PLACE if action == "placement" else CELL_HIGHLIGHT_REMOVE
        self.grid_view.set_highlight(snap["ligne"], snap["colonne"], highlight_color)
        self.grid_view.draw(snap["grille"], self.initial_grid)

        # Dashboard
        self._draw_dashboard(snap, total)

        # Controles
        ctrl_y = C.GRID_OFFSET_Y + GRID_SIZE + SP_XL
        self._draw_controls(ctrl_y)

        # Barre de progression
        bar_y = ctrl_y + 36 + SP_L
        self._draw_progress_bar(bar_y)

    def _draw_dashboard(self, snap, total):
        px = C.PANEL_X
        py = C.PANEL_Y
        pw = C.PANEL_WIDTH

        action = snap["action"]
        action_text = "Placement" if action == "placement" else "Retrait"
        action_color = PASTEL_MINT if action == "placement" else PASTEL_CORAL

        placements = sum(1 for s in self.snapshots[:self.current_step + 1] if s["action"] == "placement")
        retraits = sum(1 for s in self.snapshots[:self.current_step + 1] if s["action"] == "retrait")
        total_p = sum(1 for s in self.snapshots if s["action"] == "placement")
        total_r = sum(1 for s in self.snapshots if s["action"] == "retrait")

        y = py

        # Etape
        etape_label = fonts.small.render("ETAPE", True, TEXT_HINT)
        self.surface.blit(etape_label, (px, y))
        etape_val = fonts.big.render(str(self.current_step + 1), True, TEXT_LIGHT)
        self.surface.blit(etape_val, (px, y + SP_L))
        etape_total = fonts.body.render(f"/ {total}", True, TEXT_HINT)
        self.surface.blit(etape_total, (px + etape_val.get_width() + SP_S, y + SP_XL + SP_M))

        # Action
        y += SP_XXXL + SP_M
        indicator = pygame.Surface((3, SP_XL), pygame.SRCALPHA)
        indicator.fill((*action_color, 200))
        self.surface.blit(indicator, (px, y))
        a_label = fonts.body_bold.render(action_text, True, action_color)
        self.surface.blit(a_label, (px + SP_M, y))
        detail = fonts.small.render(
            f"Chiffre {snap['valeur']} en ({snap['ligne']}, {snap['colonne']})",
            True, TEXT_MUTED)
        self.surface.blit(detail, (px + SP_M, y + SP_L + SP_XS))

        # Placements
        y += SP_XXL + SP_XL
        p_label = fonts.small.render("PLACEMENTS", True, TEXT_HINT)
        self.surface.blit(p_label, (px, y))
        p_val = fonts.subtitle.render(str(placements), True, PASTEL_MINT)
        self.surface.blit(p_val, (px, y + SP_L))

        p_bar_y = y + SP_XXL
        bg = pygame.Surface((pw, 5), pygame.SRCALPHA)
        bg.fill((255, 255, 255, 15))
        self.surface.blit(bg, (px, p_bar_y))
        if total_p > 0:
            fw = int((placements / total_p) * pw)
            if fw > 0:
                fill = pygame.Surface((fw, 5), pygame.SRCALPHA)
                fill.fill((*PASTEL_MINT, 150))
                self.surface.blit(fill, (px, p_bar_y))

        # Retraits
        y = p_bar_y + SP_XL
        r_label = fonts.small.render("RETRAITS", True, TEXT_HINT)
        self.surface.blit(r_label, (px, y))
        r_val = fonts.subtitle.render(str(retraits), True, PASTEL_CORAL)
        self.surface.blit(r_val, (px, y + SP_L))

        r_bar_y = y + SP_XXL
        bg2 = pygame.Surface((pw, 5), pygame.SRCALPHA)
        bg2.fill((255, 255, 255, 15))
        self.surface.blit(bg2, (px, r_bar_y))
        if total_r > 0:
            fw2 = int((retraits / total_r) * pw)
            if fw2 > 0:
                fill2 = pygame.Surface((fw2, 5), pygame.SRCALPHA)
                fill2.fill((*PASTEL_CORAL, 150))
                self.surface.blit(fill2, (px, r_bar_y))

        # Vitesse
        y = r_bar_y + SP_XL
        sp_label = fonts.small.render("VITESSE", True, TEXT_HINT)
        self.surface.blit(sp_label, (px, y))
        sp_val = fonts.subtitle.render(f"{self.speed} etapes/s", True, PASTEL_BLUE)
        self.surface.blit(sp_val, (px, y + SP_L))

        # Progression
        y += SP_XXL + SP_M
        if total > 1:
            pct = int((self.current_step / (total - 1)) * 100)
        else:
            pct = 100
        prog_label = fonts.small.render("PROGRESSION", True, TEXT_HINT)
        self.surface.blit(prog_label, (px, y))
        prog_val = fonts.subtitle.render(f"{pct}%", True, PASTEL_LAVENDER)
        self.surface.blit(prog_val, (px, y + SP_L))

        prog_bar_y = y + SP_XXL
        bg3 = pygame.Surface((pw, 5), pygame.SRCALPHA)
        bg3.fill((255, 255, 255, 15))
        self.surface.blit(bg3, (px, prog_bar_y))
        pw_fill = int(pct / 100 * pw)
        if pw_fill > 0:
            fill3 = pygame.Surface((pw_fill, 5), pygame.SRCALPHA)
            fill3.fill((*PASTEL_LAVENDER, 150))
            self.surface.blit(fill3, (px, prog_bar_y))

    def _draw_controls(self, ctrl_y):
        btns = [self.btn_start, self.btn_prev, self.btn_play,
                self.btn_next, self.btn_end, self.btn_slow, self.btn_fast]
        total_btn_w = sum(b.rect.width for b in btns) + SP_M * (len(btns) - 1)
        start_x = C.GRID_OFFSET_X + (GRID_SIZE - total_btn_w) // 2

        x = start_x
        for btn in btns:
            btn.rect.topleft = (x, ctrl_y)
            x += btn.rect.width + SP_M

        self.btn_menu.rect.topleft = (C.WINDOW_WIDTH - self.btn_menu.rect.width - SP_XXL, ctrl_y)

        self.btn_play.text = "Pause" if self.playing else "Lecture"

        for btn in btns:
            btn.draw(self.surface)

        mr = self.btn_menu.rect
        bc = (55, 55, 58) if not self.btn_menu.hovered else (80, 80, 85)
        pygame.draw.rect(self.surface, BG_COLOR, mr, border_radius=BTN_RADIUS)
        pygame.draw.rect(self.surface, bc, mr, width=1, border_radius=BTN_RADIUS)
        mt = fonts.small.render(self.btn_menu.text, True, TEXT_HINT)
        self.surface.blit(mt, mt.get_rect(center=mr.center))

    def _draw_progress_bar(self, bar_y):
        self.progress_rect = pygame.Rect(C.GRID_OFFSET_X, bar_y, GRID_SIZE, 8)

        bg = pygame.Surface((GRID_SIZE, 8), pygame.SRCALPHA)
        bg.fill((255, 255, 255, 20))
        self.surface.blit(bg, (C.GRID_OFFSET_X, bar_y))

        if len(self.snapshots) > 1:
            progress = self.current_step / (len(self.snapshots) - 1)
        else:
            progress = 1
        fw = int(GRID_SIZE * progress)
        if fw > 0:
            fill = pygame.Surface((fw, 8), pygame.SRCALPHA)
            fill.fill((*PASTEL_BLUE, 170))
            self.surface.blit(fill, (C.GRID_OFFSET_X, bar_y))

        cx = C.GRID_OFFSET_X + fw
        cy = bar_y + 4
        pygame.draw.circle(self.surface, PASTEL_BLUE, (cx, cy), 6)
        pygame.draw.circle(self.surface, BG_COLOR, (cx, cy), 3)

    def _set_step_from_mouse(self, mouse_x):
        relative_x = mouse_x - self.progress_rect.x
        relative_x = max(0, min(relative_x, self.progress_rect.width))
        ratio = relative_x / self.progress_rect.width
        self.current_step = int(ratio * (len(self.snapshots) - 1))

    def handle_event(self, event):
        if not self.snapshots:
            return None

        if self.btn_play.handle_event(event):
            self.playing = not self.playing
            if self.playing and self.current_step >= len(self.snapshots) - 1:
                self.current_step = 0
        if self.btn_start.handle_event(event):
            self.playing = False
            self.current_step = 0
        if self.btn_prev.handle_event(event):
            self.playing = False
            self.current_step = max(0, self.current_step - 1)
        if self.btn_next.handle_event(event):
            self.playing = False
            self.current_step = min(len(self.snapshots) - 1, self.current_step + 1)
        if self.btn_end.handle_event(event):
            self.playing = False
            self.current_step = len(self.snapshots) - 1
        if self.btn_slow.handle_event(event):
            self.speed = max(REPLAY_SPEED_MIN, self.speed // 2)
        if self.btn_fast.handle_event(event):
            self.speed = min(REPLAY_SPEED_MAX, self.speed * 2)
        if self.btn_menu.handle_event(event):
            self.playing = False
            return "menu"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.progress_rect.collidepoint(event.pos):
                self.dragging_progress = True
                self.playing = False
                self._set_step_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_progress = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_progress:
            self._set_step_from_mouse(event.pos[0])

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
            elif event.key == pygame.K_HOME:
                self.playing = False
                self.current_step = 0
            elif event.key == pygame.K_END:
                self.playing = False
                self.current_step = len(self.snapshots) - 1

        return None
