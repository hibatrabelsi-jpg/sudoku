"""
Application Pygame principale.
Gere la boucle principale, les transitions entre ecrans,
et la connexion avec la classe SudokuGrid.
"""

import pygame
from gui.constants import *
from gui.menu import MenuScreen
from gui.resolve_screen import ResolveScreen
from gui.replay_view import ReplayScreen
from gui.stats_view import StatsView
from gui.play_view import PlayView
from sudoku_grid import SudokuGrid


class App:
    """Application Pygame du Sudoku Solver"""

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()

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

        # Donnees conservees entre ecrans pour la navigation
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

        pygame.quit()

    def _handle_event(self, event):
        """Dispatch les evenements vers l'ecran actif"""
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
        """Met a jour l'ecran actif"""
        if self.current_screen == SCREEN_REPLAY:
            self.replay_screen.update(dt)

    def _draw(self):
        """Dessine l'ecran actif"""
        self.surface.fill(BG_COLOR)

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
        """Reagit a une action du menu"""
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
        """Lance une seule methode et affiche le resultat"""
        if method == "backtracking":
            success = self.grid.solve_backtracking()
            method_name = "Backtracking"
        else:
            success = self.grid.solve_brute_force(max_iterations=500000)
            method_name = "Force Brute"

        # Sauvegarder les donnees
        self._save_result(method, success)

        # Afficher le resultat
        self.resolve_screen.setup(self.grid, method_name, success)
        self.current_screen = SCREEN_RESOLVE

    def _solve_compare(self):
        """Lance les deux methodes et affiche la comparaison"""
        # Backtracking
        self.grid.solve_backtracking()
        self._save_result("backtracking", True)

        # Force brute
        self.grid.solve_brute_force(max_iterations=500000)
        bf_success = self.grid.get_stats()["iterations"] < 500000
        self._save_result("force_brute", bf_success)

        # Afficher la comparaison
        self.stats_view.setup(
            self.bt_stats, self.bf_stats,
            self.bt_success, self.bf_success,
            self.current_grid_path
        )
        self.current_screen = SCREEN_COMPARE

    def _save_result(self, method, success):
        """Sauvegarde les resultats d'une resolution pour navigation ulterieure"""
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
        """Affiche l'ecran de resolution pour une methode depuis la comparaison"""
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
        """Lance le replay pour une methode specifique"""
        if method == "backtracking" and self.bt_snapshots:
            self.replay_screen.setup(
                self.bt_snapshots, self.bt_initial_grid, "Backtracking")
            self.current_screen = SCREEN_REPLAY
        elif method == "force_brute" and self.bf_snapshots:
            self.replay_screen.setup(
                self.bf_snapshots, self.bf_initial_grid, "Force Brute")
            self.current_screen = SCREEN_REPLAY

    def _start_replay_current(self):
        """Lance le replay depuis l'ecran de resolution"""
        if self.grid.snapshots:
            method_name = self.grid.stats.get("methode", "").replace("_", " ").title()
            self.replay_screen.setup(
                self.grid.get_snapshots(),
                [row[:] for row in self.grid.initial_grid],
                method_name
            )
            self.current_screen = SCREEN_REPLAY


def launch():
    """Point d'entree pour lancer l'interface Pygame"""
    app = App()
    app.run()


if __name__ == "__main__":
    launch()
