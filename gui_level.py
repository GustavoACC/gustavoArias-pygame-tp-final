import pygame
from constantes import *
from pygame.locals import *
from auxiliar import *
pygame.init()
pygame.mixer.init()

font_40 = pygame.font.Font("fonts/Minecraft.ttf", 40)
font_20 = pygame.font.Font("fonts/Minecraft.ttf", 20)

class Gui_Level:

    def __init__(self, vidas, puntaje, tiempo_restante):
        self.vidas = vidas
        self.puntaje = puntaje
        self.tiempo_restante = tiempo_restante

    def update(self, vidas, puntaje, tiempo_transcurrido):
        self.vidas = vidas
        self.puntaje = puntaje
        self.tiempo_restante = str((tiempo_transcurrido)).split(".")[0]
    
    def draw(self, screen):
        texto_vidas = font_20.render(
            "Vidas: {0}".format(self.vidas), True, (255,255,255)
        )
        texto_puntaje = font_20.render(
            "Puntaje: {0}".format(self.puntaje), True, (255,255,255)
        )
        texto_tiempo_restante = font_40.render(
            "{0}".format(self.tiempo_restante), True, (255,255,255)
        )
        screen.blit(texto_vidas, (31, 21))
        screen.blit(texto_puntaje, (834, 21))
        screen.blit(texto_tiempo_restante, (438, 21))