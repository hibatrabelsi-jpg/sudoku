"""
Direction artistique du projet.
Theme noir et blanc avec accents bleu et pastels.
Proportions basees sur le nombre d'or (phi = 1.618).
Polices : Comucan (titres), Creato Display (contenu).
"""

import os

# =============================================================================
# NOMBRE D'OR
# =============================================================================

PHI = 1.618

# Echelle de spacing basee sur phi (approximation de Fibonacci)
SP_XS = 5
SP_S = 8
SP_M = 13
SP_L = 21
SP_XL = 34
SP_XXL = 55
SP_XXXL = 89

# =============================================================================
# DIMENSIONS DE LA FENETRE (quasi plein ecran, adapte dans app.py)
# =============================================================================

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900

# Grille de Sudoku
CELL_SIZE = 64
GRID_SIZE = CELL_SIZE * 9                   # 576px
GRID_OFFSET_X = SP_XXL                      # 55px
GRID_OFFSET_Y = SP_XXXL + SP_M              # 102px

# Panneau lateral
PANEL_X = GRID_OFFSET_X + GRID_SIZE + SP_XL
PANEL_Y = GRID_OFFSET_Y
PANEL_WIDTH = 400

# Boutons
BTN_HEIGHT = 44
BTN_RADIUS = SP_S

# =============================================================================
# PALETTE
# =============================================================================

# Fonds
BG_COLOR = (17, 17, 17)                     # fond principal (quasi noir)
SURFACE_COLOR = (26, 26, 26)                 # surface/panneaux
SURFACE_LIGHT = (38, 38, 38)                 # surface sureleve

# Grille
CELL_NORMAL = (250, 250, 250)                # fond de case (quasi blanc)
CELL_SELECTED = (210, 225, 245)              # case selectionnee (bleu pastel)
CELL_HIGHLIGHT_PLACE = (210, 235, 210)       # placement (vert pastel)
CELL_HIGHLIGHT_REMOVE = (240, 210, 210)      # retrait (rose pastel)
CELL_ERROR = (240, 200, 200)                 # erreur
CELL_ROW_COL = (235, 240, 248)              # surlignage ligne/colonne (bleu tres leger)

GRID_LINE_THIN = (200, 200, 200)             # lignes fines
GRID_LINE_THICK = (40, 40, 40)              # lignes epaisses (carres 3x3)

# Accent bleu
ACCENT_BLUE = (70, 130, 210)                # bleu principal
ACCENT_BLUE_LIGHT = (180, 205, 240)          # bleu pastel
ACCENT_BLUE_DARK = (45, 90, 160)             # bleu fonce

# Texte sur fond sombre
TEXT_LIGHT = (245, 245, 245)                 # texte principal
TEXT_MUTED = (160, 160, 160)                 # texte secondaire
TEXT_HINT = (100, 100, 100)                  # texte discret

# Texte sur fond clair (dans les cases)
TEXT_INITIAL = (20, 20, 20)                  # chiffres d'origine (noir gras)
TEXT_SOLVED = (70, 130, 210)                 # chiffres resolus (bleu)
TEXT_USER = (70, 130, 210)                   # chiffres du joueur (bleu)
TEXT_ERROR = (200, 90, 90)                   # erreurs

# Titre
TEXT_TITLE = (255, 255, 255)                 # blanc pur

# Boutons
BTN_BG = (32, 32, 32)
BTN_BG_HOVER = (50, 65, 90)                 # hover bleu sombre
BTN_BORDER = (70, 70, 70)
BTN_BORDER_HOVER = ACCENT_BLUE
BTN_TEXT = (220, 220, 220)

# Stats
STAT_BG = (25, 25, 28)
STAT_BORDER = (45, 45, 50)

# Menu
MENU_ITEM_BG = (30, 30, 30)
MENU_ITEM_HOVER = (40, 50, 65)
MENU_ITEM_SELECTED_BORDER = ACCENT_BLUE

# Replay
REPLAY_BAR_BG = (45, 45, 50)
REPLAY_BAR_FILL = ACCENT_BLUE

# Pastels pour indicateurs
COLOR_SUCCESS = (120, 200, 140)              # vert pastel
COLOR_WARNING = (220, 180, 100)              # jaune pastel
COLOR_DANGER = (210, 110, 110)               # rose/rouge pastel
COLOR_INFO = ACCENT_BLUE

# =============================================================================
# POLICES
# =============================================================================

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")

FONT_TITLE_PATH = os.path.join(FONTS_DIR, "Comucan.otf")
FONT_REGULAR_PATH = os.path.join(FONTS_DIR, "CreatoDisplay-Regular.otf")
FONT_MEDIUM_PATH = os.path.join(FONTS_DIR, "CreatoDisplay-Medium.otf")
FONT_BOLD_PATH = os.path.join(FONTS_DIR, "CreatoDisplay-Bold.otf")
FONT_LIGHT_PATH = os.path.join(FONTS_DIR, "CreatoDisplay-Light.otf")

FONT_SIZE_HERO = 48
FONT_SIZE_TITLE = 32
FONT_SIZE_SUBTITLE = 22
FONT_SIZE_BODY = 16
FONT_SIZE_CELL = 28
FONT_SIZE_SMALL = 13
FONT_SIZE_BUTTON = 15

FONT_FALLBACK = None

# =============================================================================
# TIMING
# =============================================================================

FPS = 60
REPLAY_SPEED_DEFAULT = 10
REPLAY_SPEED_MIN = 1
REPLAY_SPEED_MAX = 100

# =============================================================================
# ECRANS
# =============================================================================

SCREEN_MENU = "menu"
SCREEN_RESOLVE = "resolve"
SCREEN_REPLAY = "replay"
SCREEN_COMPARE = "compare"
SCREEN_PLAY = "play"
