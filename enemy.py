import random
import pygame
from auxiliar import *
from constantes import *
from pygame.locals import *

class Enemy:

    def iniciar_sprites(self):
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/enemies/mushroom/Run (32x32).png", 16, 1)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/enemies/mushroom/Run (32x32).png", 16, 1, True)
        self.idle_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/enemies/mushroom/Idle (32x32).png", 14, 1, True)
        self.idle_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/enemies/mushroom/Idle (32x32).png", 14, 1, True)
        self.hit = Auxiliar.getSurfaceFromSpriteSheet("recursos/enemies/mushroom/Hit.png", 5, 1)

    def __init__(self, x, y, velocidad):
        self.iniciar_sprites()
        self.frame = 0
        self.direccion = 1
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.animation = self.idle_r
        self.imagen = self.animation[self.frame]
        self.velocidad = velocidad
        self.proximo_movimiento = self.set_proximo_movimiento()
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_body_colision = pygame.Rect(x,y,self.rect.width, self.rect.height)
        self.rect_height_colision = pygame.Rect(self.rect.x + self.rect.width / 2, self.rect.y - 2, self.rect.width / 2, 3)
        
    
    def update(self, pauseState, lista_enemigos):
        if pauseState == True:
            return
        # if is_colision_player():
        #     lista_enemigos.remove(self)
        self.do_animation()

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, C_RED, self.rect_body_colision)
            pygame.draw.rect(screen, C_BLUE, self.rect_height_colision)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

    def do_animation(self):
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            self.frame = 0

    def set_proximo_movimiento(self):
        return pygame.time.get_ticks() - random.randint(1, 5)

    def set_ubicacion(self):
        pass