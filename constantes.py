import pygame
pygame.mixer.init()

DEBUG = False
ALTO_PANTALLA = 768
ANCHO_PANTALLA = 1088
PATH_IMAGE = "recursos/"
PATH_GUI = "recursos/gui/"
FPS = 30
VELOCIDAD_X = 6
VELOCIDAD_Y = 14
GRAVEDAD = 4
MAX_HEIGHT_JUMP = 70
GROUND_LEVEL = 704
HIGH_LEVEL = 110
LEFT_LEVEL = 32
RIGHT_LEVEL = 1040
GENERAL_CONFIG_JSON = "general_config.json"

# Sonidos
TAKE_ITEM = pygame.mixer.Sound("sounds/mixkit-arcade-retro-changing-tab-206.wav")
VICTORY_ITEM = pygame.mixer.Sound("sounds/mixkit-arcade-game-complete-or-approved-mission-205.wav")
LOSE = pygame.mixer.Sound("sounds/mixkit-player-losing-or-failing-2042.wav")
HIT = pygame.mixer.Sound("sounds/mixkit-small-hit-in-a-game-2072.wav")
ACHIVEMENT = pygame.mixer.Sound("sounds/mixkit-quick-positive-video-game-notification-interface-265.wav")
ENEMY_DEAD = pygame.mixer.Sound("sounds\mixkit-arcade-game-jump-coin-216.wav")

# Colores fijos
C_RED = (255,0,0)
C_GREEN = (0,255,0)
C_BLUE = (0,0,255)
C_BLACK = (0,0,0)
C_WHITE = (255,255,255)
C_PINK = (255, 0, 160)
C_PEACH = (255, 118, 95)
C_BLUE_2 = (38, 0, 160)
C_YELLOW_2 = (255, 174, 0)
C_GREEEN_2 = (38, 137, 0)
C_ORANGE = (255, 81, 0)

# MOUSE CONSTANTS
M_STATE_NORMAL = 0
M_STATE_HOVER = 1
M_STATE_CLICK = 3
M_BRIGHT_HOVER = (32,32,32)
M_BRIGHT_CLICK = (32,32,32)
