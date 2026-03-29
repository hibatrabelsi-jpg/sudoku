"""
Application Pygame principale.
Gere la boucle principale, les transitions entre ecrans,
et la connexion avec la classe SudokuGrid.
"""

import pygame
import gui.constants as const
from gui.constants import *
from gui.fonts import fonts
from gui.menu import MenuScreen
from gui.resolve_screen import ResolveScreen
from gui.replay_view import ReplayScreen
from gui.stats_view import StatsView
from gui.play_view import PlayView
from sudoku_grid import SudokuGrid
from database import Database


class App:
    """Application Pygame du Sudoku Solver"""

    def __init__(self):
        pygame.init()

        # Detecter la resolution de l'ecran — fenetre reduite de 20%
        info = pygame.display.Info()
        const.WINDOW_WIDTH = int(info.current_w * 0.8)
        const.WINDOW_HEIGHT = int(info.current_h * 0.8)

        # Centrer le bloc (grille + gap + panneau) horizontalement
        gap = SP_XL
        panel_w = 300
        total_content_w = const.GRID_SIZE + gap + panel_w
        const.GRID_OFFSET_X = (const.WINDOW_WIDTH - total_content_w) // 2
        const.PANEL_X = const.GRID_OFFSET_X + const.GRID_SIZE + gap
        const.PANEL_WIDTH = panel_w

        # Vertical — titre en haut, grille en dessous, espace pour controles en bas
        const.GRID_OFFSET_Y = SP_XXXL + SP_M
        const.PANEL_Y = const.GRID_OFFSET_Y

        self.surface = pygame.display.set_mode(
            (const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()

        # Fond degrade noir -> gris fonce (genere une seule fois)
        self.bg_gradient = self._create_gradient(
            const.WINDOW_WIDTH, const.WINDOW_HEIGHT,
            (30, 30, 35),    # gris fonce en haut
            (12, 12, 14)     # quasi noir en bas
        )

        # Charger les polices
        fonts.load()

        # Ecrans
        self.menu = MenuScreen(self.surface)
        self.resolve_screen = ResolveScreen(self.surface)
        self.replay_screen = ReplayScreen(self.surface)
        self.stats_view = StatsView(self.surface)
        self.play_view = PlayView(self.surface)

        # Etat
        self.current_screen = SCREEN_MENU
        self.grid = None
        self.running = True
        self.current_grid_path = ""

        # Base de donnees
        self.db = Database()

        # Donnees conservees entre ecrans
        self.bt_grid = None
        self.bt_initial_grid = None
        self.bt_snapshots = []
        self.bt_stats = {}
        self.bt_success = False

        self.bf_grid = None
        self.bf_initial_grid = None
        self.bf_snapshots = []
        self.bf_stats = {}
        self.bf_success = False

    @staticmethod
    def _create_gradient(width, height, color_top, color_bottom):
        """Cree une surface avec un degrade vertical"""
        surface = pygame.Surface((width, height))
        for y in range(height):
            t = y / height
            r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
            g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
            b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        return surface

    def run(self):
        """Boucle principale"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.current_screen == SCREEN_MENU:
                        self.running = False
                    else:
                        self.current_screen = SCREEN_MENU
                else:
                    self._handle_event(event)

            self._update(dt)
            self._draw()
            pygame.display.flip()

        self.db.close()
        pygame.quit()

    def _handle_event(self, event):
        if self.current_screen == SCREEN_MENU:
            result = self.menu.handle_event(event)
            if result:
                action, grid_path = result
                if grid_path:
                    self._on_menu_action(action, grid_path)

        elif self.current_screen == SCREEN_RESOLVE:
            result = self.resolve_screen.handle_event(event)
            if result == "replay":
                self._start_replay_current()
            elif result == "menu":
                self.current_screen = SCREEN_MENU

        elif self.current_screen == SCREEN_REPLAY:
            result = self.replay_screen.handle_event(event)
            if result == "menu":
                self.current_screen = SCREEN_MENU

        elif self.current_screen == SCREEN_COMPARE:
            result = self.stats_view.handle_event(event)
            if result == "view_bt":
                self._show_resolve("backtracking")
            elif result == "view_bf":
                self._show_resolve("force_brute")
            elif result == "replay_bt":
                self._start_replay("backtracking")
            elif result == "menu":
                self.current_screen = SCREEN_MENU

        elif self.current_screen == SCREEN_PLAY:
            result = self.play_view.handle_event(event)
            if result == "menu":
                self.current_screen = SCREEN_MENU

    def _update(self, dt):
        if self.current_screen == SCREEN_REPLAY:
            self.replay_screen.update(dt)

    def _draw(self):
        self.surface.blit(self.bg_gradient, (0, 0))

        if self.current_screen == SCREEN_MENU:
            self.menu.draw()
        elif self.current_screen == SCREEN_RESOLVE:
            self.resolve_screen.draw()
        elif self.current_screen == SCREEN_REPLAY:
            self.replay_screen.draw()
        elif self.current_screen == SCREEN_COMPARE:
            self.stats_view.draw()
        elif self.current_screen == SCREEN_PLAY:
            self.play_view.draw()

    # =========================================================================
    # ACTIONS
    # =========================================================================

    def _on_menu_action(self, action, grid_path):
        if action == "export":
            self._export_markdown()
            return

        self.current_grid_path = grid_path
        self.grid = SudokuGrid(grid_path)

        if action == "backtracking":
            self._solve_single("backtracking")
        elif action == "brute_force":
            self._solve_single("force_brute")
        elif action == "compare":
            self._solve_compare()
        elif action == "play":
            self.play_view.setup(self.grid)
            self.current_screen = SCREEN_PLAY

    def _solve_single(self, method):
        if method == "backtracking":
            success = self.grid.solve_backtracking()
            method_name = "Backtracking"
        else:
            success = self.grid.solve_brute_force(max_iterations=500000)
            method_name = "Force Brute"

        self._save_result(method, success)
        self.db.save_resolution(self.grid, success)

        self.resolve_screen.setup(self.grid, method_name, success)
        self.current_screen = SCREEN_RESOLVE

    def _solve_compare(self):
        self.grid.solve_backtracking()
        self._save_result("backtracking", True)
        self.db.save_resolution(self.grid, True)

        self.grid.solve_brute_force(max_iterations=500000)
        bf_success = self.grid.get_stats()["iterations"] < 500000
        self._save_result("force_brute", bf_success)
        self.db.save_resolution(self.grid, bf_success)

        self.stats_view.setup(
            self.bt_stats, self.bf_stats,
            self.bt_success, self.bf_success,
            self.current_grid_path)
        self.current_screen = SCREEN_COMPARE

    def _save_result(self, method, success):
        if method == "backtracking":
            self.bt_grid = [row[:] for row in self.grid.grid]
            self.bt_initial_grid = [row[:] for row in self.grid.initial_grid]
            self.bt_snapshots = self.grid.get_snapshots()
            self.bt_stats = self.grid.get_stats()
            self.bt_success = success
        else:
            self.bf_grid = [row[:] for row in self.grid.grid]
            self.bf_initial_grid = [row[:] for row in self.grid.initial_grid]
            self.bf_snapshots = self.grid.get_snapshots()
            self.bf_stats = self.grid.get_stats()
            self.bf_success = success

    def _show_resolve(self, method):
        if method == "backtracking" and self.bt_grid:
            self.grid.grid = [row[:] for row in self.bt_grid]
            self.grid.initial_grid = [row[:] for row in self.bt_initial_grid]
            self.grid.stats = dict(self.bt_stats)
            self.grid.snapshots = list(self.bt_snapshots)
            self.resolve_screen.setup(self.grid, "Backtracking", self.bt_success)
            self.current_screen = SCREEN_RESOLVE
        elif method == "force_brute" and self.bf_grid:
            self.grid.grid = [row[:] for row in self.bf_grid]
            self.grid.initial_grid = [row[:] for row in self.bf_initial_grid]
            self.grid.stats = dict(self.bf_stats)
            self.grid.snapshots = list(self.bf_snapshots)
            self.resolve_screen.setup(self.grid, "Force Brute", self.bf_success)
            self.current_screen = SCREEN_RESOLVE

    def _start_replay(self, method):
        if method == "backtracking" and self.bt_snapshots:
            self.replay_screen.setup(
                self.bt_snapshots, self.bt_initial_grid, "Backtracking")
            self.current_screen = SCREEN_REPLAY
        elif method == "force_brute" and self.bf_snapshots:
            self.replay_screen.setup(
                self.bf_snapshots, self.bf_initial_grid, "Force Brute")
            self.current_screen = SCREEN_REPLAY

    def _start_replay_current(self):
        if self.grid.snapshots:
            method_name = self.grid.stats.get("methode", "").replace("_", " ").title()
            self.replay_screen.setup(
                self.grid.get_snapshots(),
                [row[:] for row in self.grid.initial_grid],
                method_name)
            self.current_screen = SCREEN_REPLAY

    def _export_markdown(self):
        success = self.db.export_markdown()
        if success:
            self.menu.import_message = "Rapport exporte dans exports/rapport_comparatif.md"
            self.menu.import_message_timer = 240
        else:
            self.menu.import_message = "Aucune donnee a exporter (lancez des resolutions d'abord)"
            self.menu.import_message_timer = 240


def launch():
    app = App()
    app.run()


if __name__ == "__main__":
    launch()
