"""
Ecran du menu principal.
"""

import pygame
import os
import shutil
from gui.constants import *
from gui.components import Button, Label


class MenuScreen:
    """Menu principal avec selection de grille et choix de methode"""

    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE, bold=True)
        self.font_sub = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SUBTITLE)
        self.font_body = pygame.font.SysFont(FONT_NAME, FONT_SIZE_BODY)
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)

        # Detecter les grilles disponibles
        self.grids = self._find_grids()
        self.selected_grid = 0

        # Boutons de grille
        self.grid_buttons = []
        self._build_grid_buttons()

        # Bouton d'import
        self.btn_import = Button(
            WINDOW_WIDTH // 2 - 100, 370, 200, 36, "Importer une grille", font_size=FONT_SIZE_SMALL)

        # Boutons d'action
        btn_y = 430
        btn_w = 280
        btn_h = 45
        btn_x = (WINDOW_WIDTH - btn_w) // 2

        self.btn_backtracking = Button(btn_x, btn_y, btn_w, btn_h, "Resoudre (Backtracking)")
        self.btn_brute_force = Button(btn_x, btn_y + 60, btn_w, btn_h, "Resoudre (Force Brute)")
        self.btn_compare = Button(btn_x, btn_y + 120, btn_w, btn_h, "Comparer les deux")
        self.btn_play = Button(btn_x, btn_y + 180, btn_w, btn_h, "Jouer")

        # Message d'import (temporaire)
        self.import_message = ""
        self.import_message_timer = 0

    def _find_grids(self):
        """Trouve les fichiers de grilles dans data/"""
        grid_dir = "data"
        if not os.path.exists(grid_dir):
            os.makedirs(grid_dir)
            return []
        files = sorted([f for f in os.listdir(grid_dir) if f.endswith(".txt")])
        return [os.path.join(grid_dir, f) for f in files]

    def _build_grid_buttons(self):
        """Cree les boutons de selection de grille"""
        self.grid_buttons = []
        total = len(self.grids)
        if total == 0:
            return

        btn_w = 80
        gap = 10
        total_w = total * btn_w + (total - 1) * gap
        start_x = (WINDOW_WIDTH - total_w) // 2

        for i, path in enumerate(self.grids):
            name = os.path.basename(path).replace(".txt", "").replace("grille", "Grille ")
            btn = Button(start_x + i * (btn_w + gap), 320, btn_w, 40, name, font_size=FONT_SIZE_SMALL)
            self.grid_buttons.append(btn)

    def _import_grid(self):
        """Ouvre un explorateur de fichiers pour importer une grille"""
        try:
            import tkinter as tk
            from tkinter import filedialog

            # Creer une fenetre tkinter cachee pour le dialogue
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)

            filepath = filedialog.askopenfilename(
                title="Importer une grille de Sudoku",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
            )

            root.destroy()

            if filepath and os.path.exists(filepath):
                # Lire le contenu du fichier importe
                with open(filepath, 'r') as f:
                    new_content = f.read().strip()

                # Verifier si une grille identique existe deja dans data/
                for existing in self.grids:
                    with open(existing, 'r') as f:
                        if f.read().strip() == new_content:
                            self.import_message = "Cette grille existe deja"
                            self.import_message_timer = 180
                            return

                # Copier le fichier dans data/
                filename = os.path.basename(filepath)
                dest = os.path.join("data", filename)

                # Si le nom existe mais le contenu est different, renommer
                if os.path.exists(dest):
                    name, ext = os.path.splitext(filename)
                    i = 1
                    while os.path.exists(dest):
                        dest = os.path.join("data", f"{name}_{i}{ext}")
                        i += 1

                shutil.copy2(filepath, dest)

                # Rafraichir la liste
                self.grids = self._find_grids()
                self.selected_grid = len(self.grids) - 1
                self._build_grid_buttons()

                self.import_message = f"Grille importee : {os.path.basename(dest)}"
                self.import_message_timer = 180  # 3 secondes a 60fps

        except Exception as e:
            self.import_message = f"Erreur : {str(e)}"
            self.import_message_timer = 180

    def draw(self):
        """Dessine le menu"""
        # Titre
        title = self.font_title.render("Sudoku Solver", True, TEXT_TITLE)
        title_rect = title.get_rect(centerx=WINDOW_WIDTH // 2, y=60)
        self.surface.blit(title, title_rect)

        # Sous-titre
        sub = self.font_sub.render("Analyse comparative : Force Brute vs Backtracking", True, TEXT_SECONDARY)
        sub_rect = sub.get_rect(centerx=WINDOW_WIDTH // 2, y=110)
        self.surface.blit(sub, sub_rect)

        # Ligne decorative
        line_y = 155
        line_w = 300
        pygame.draw.line(self.surface, GRID_LINE_THIN,
                         (WINDOW_WIDTH // 2 - line_w // 2, line_y),
                         (WINDOW_WIDTH // 2 + line_w // 2, line_y), 1)

        # Section selection de grille
        label = self.font_body.render("Choisir une grille :", True, TEXT_PRIMARY)
        label_rect = label.get_rect(centerx=WINDOW_WIDTH // 2, y=280)
        self.surface.blit(label, label_rect)

        # Boutons de grille
        for i, btn in enumerate(self.grid_buttons):
            if i == self.selected_grid:
                pygame.draw.rect(self.surface, CELL_SELECTED, btn.rect, border_radius=8)
                pygame.draw.rect(self.surface, BTN_BORDER_HOVER, btn.rect, width=2, border_radius=8)
                text_surf = btn.font.render(btn.text, True, BTN_TEXT)
                text_rect = text_surf.get_rect(center=btn.rect.center)
                self.surface.blit(text_surf, text_rect)
            else:
                btn.draw(self.surface)

        # Bouton d'import
        self.btn_import.draw(self.surface)

        # Message d'import
        if self.import_message_timer > 0:
            self.import_message_timer -= 1
            is_warning = "existe deja" in self.import_message or "Erreur" in self.import_message
            color = (200, 130, 30) if is_warning else (60, 150, 60)
            msg = self.font_small.render(self.import_message, True, color)
            msg_rect = msg.get_rect(centerx=WINDOW_WIDTH // 2, y=410)
            self.surface.blit(msg, msg_rect)

        # Boutons d'action
        self.btn_backtracking.draw(self.surface)
        self.btn_brute_force.draw(self.surface)
        self.btn_compare.draw(self.surface)
        self.btn_play.draw(self.surface)

    def handle_event(self, event):
        """
        Gere les evenements.
        Retourne un tuple (action, grid_path) ou None.
        Actions possibles : "backtracking", "brute_force", "compare", "play"
        """
        # Import de grille
        if self.btn_import.handle_event(event):
            self._import_grid()
            return None

        # Selection de grille
        for i, btn in enumerate(self.grid_buttons):
            if btn.handle_event(event):
                self.selected_grid = i

        # Boutons d'action
        grid_path = self.grids[self.selected_grid] if self.grids else None

        if self.btn_backtracking.handle_event(event):
            return ("backtracking", grid_path)
        if self.btn_brute_force.handle_event(event):
            return ("brute_force", grid_path)
        if self.btn_compare.handle_event(event):
            return ("compare", grid_path)
        if self.btn_play.handle_event(event):
            return ("play", grid_path)

        return None
