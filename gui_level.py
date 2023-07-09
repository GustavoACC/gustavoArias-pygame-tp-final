import pygame
from constantes import *
from pygame.locals import *
from auxiliar import *
pygame.init()
font_vidas = pygame.font.SysFont("Arial", 15)

class Gui_Level:

    def __init__(self, x, y, vidas) -> None:
        self.vidas = vidas
        self.x = x
        self.y = y

    def update(self, vidas):
        self.vidas = vidas
    
    def draw(self, screen):
        texto_vidas = font_vidas.render(
            "Vidas: {0}".format(self.vidas), True, (255,255,255)
        )
        screen.blit(texto_vidas, (self.x, self.y))