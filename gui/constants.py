"""
Direction artistique du projet.
Toutes les constantes visuelles sont centralisees ici.
Pour changer l'apparence, il suffit de modifier ce fichier.
"""

# =============================================================================
# DIMENSIONS DE LA FENETRE
# =============================================================================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Grille de Sudoku
GRID_SIZE = 540                     # taille totale de la grille (9x9)
CELL_SIZE = GRID_SIZE // 9          # taille d'une case (60px)
GRID_OFFSET_X = 40                  # marge gauche de la grille
GRID_OFFSET_Y = 80                  # marge haute de la grille (place pour le titre)

# Panneau lateral (stats, boutons)
PANEL_X = GRID_OFFSET_X + GRID_SIZE + 40
PANEL_Y = GRID_OFFSET_Y
PANEL_WIDTH = WINDOW_WIDTH - PANEL_X - 30

# =============================================================================
# PALETTE DE COULEURS (style epure et minimaliste)
# =============================================================================

# Fond
BG_COLOR = (245, 245, 240)          # blanc casse

# Grille
GRID_LINE_THIN = (200, 200, 195)    # lignes fines (entre les cases)
GRID_LINE_THICK = (50, 50, 48)      # lignes epaisses (entre les carres 3x3)

# Cases
CELL_NORMAL = (255, 255, 255)       # fond de case normal
CELL_SELECTED = (220, 235, 250)     # case selectionnee (bleu tres leger)
CELL_HIGHLIGHT_PLACE = (200, 235, 200)  # case replay : placement (vert leger)
CELL_HIGHLIGHT_REMOVE = (245, 210, 210) # case replay : retrait (rouge leger)
CELL_ERROR = (250, 200, 200)        # case en erreur

# Texte
TEXT_INITIAL = (30, 30, 28)         # chiffres d'origine (noir/gras)
TEXT_SOLVED = (50, 100, 200)        # chiffres trouves par l'algo (bleu)
TEXT_USER = (80, 80, 180)           # chiffres entres par le joueur
TEXT_PRIMARY = (30, 30, 28)         # texte principal
TEXT_SECONDARY = (120, 120, 115)    # texte secondaire (labels, etc.)
TEXT_TITLE = (50, 100, 200)         # titres

# Boutons
BTN_BG = (255, 255, 255)           # fond du bouton
BTN_BG_HOVER = (235, 240, 250)     # fond du bouton au survol
BTN_BORDER = (180, 180, 175)       # bordure du bouton
BTN_BORDER_HOVER = (50, 100, 200)  # bordure au survol
BTN_TEXT = (30, 30, 28)            # texte du bouton

# Panneau stats
STAT_BG = (250, 250, 247)          # fond du panneau stats
STAT_BORDER = (220, 220, 215)      # bordure du panneau

# Menu
MENU_ITEM_BG = (255, 255, 255)
MENU_ITEM_HOVER = (240, 245, 255)

# Replay
REPLAY_BAR_BG = (230, 230, 225)    # fond de la barre de progression
REPLAY_BAR_FILL = (50, 100, 200)   # remplissage de la progression

# =============================================================================
# POLICES
# =============================================================================

FONT_NAME = None                    # None = police systeme par defaut
FONT_SIZE_TITLE = 28
FONT_SIZE_SUBTITLE = 20
FONT_SIZE_CELL = 28                 # chiffres dans les cases
FONT_SIZE_BODY = 16
FONT_SIZE_SMALL = 14
FONT_SIZE_BUTTON = 16

# =============================================================================
# TIMING
# =============================================================================

FPS = 60
REPLAY_SPEED_DEFAULT = 10           # etapes par seconde
REPLAY_SPEED_MIN = 1
REPLAY_SPEED_MAX = 100
REPLAY_SPEED_FAST = 50

# =============================================================================
# ECRANS
# =============================================================================

SCREEN_MENU = "menu"
SCREEN_RESOLVE = "resolve"
SCREEN_REPLAY = "replay"
SCREEN_COMPARE = "compare"
SCREEN_PLAY = "play"
