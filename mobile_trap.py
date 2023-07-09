import pygame
from constantes import *
from pygame.locals import *
from auxiliar import *

class Trap:
    def iniciar_sprites(self):
        match(self.type):
            case 0:
                if self.sub_type == 0:
                    self.init_animation = Auxiliar.getSurfaceFromSpriteSheet("recursos/traps/saw/On (38x38).png", 8, 1)
                else:
                    self.init_animation = Auxiliar.getSurfaceFromSpriteSheet("recursos/traps/saw/On (38x38).png", 8, 1,flip = True)
        

    def __init__(self, init_x = 0, init_y = 0, min_x = 0, max_x = 0, min_y = 0, max_y = 0, velocidad = 0, movimiento = 'n', type = 0, sub_type = 0, col_rest = 0) -> None:
        self.type = type
        self.sub_type = sub_type
        self.iniciar_sprites()
        self.frame = 0
        self.movimiento = movimiento
        self.direccion = 0
        self.velocidad = velocidad
        self.max_x = init_x + max_x
        self.min_x = init_x - min_x
        self.max_y = init_y + max_y
        self.min_y = init_y - min_y
        self.animation = self.init_animation
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.collider = pygame.Rect(self.rect.x + col_rest / 2, self.rect.y + col_rest / 2, self.rect.w - col_rest, self.rect.h - col_rest)
    
    def update(self, pauseState):
        if pauseState == True:
            return
        self.do_move()
        self.do_animation()
    
    def draw(self, screen):
        if(DEBUG):
            pygame.draw.rect(screen, C_RED, self.collider)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

    def do_animation(self):
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            self.frame = 0
    
    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.collider.x += delta_x

    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.collider.y += delta_y
    
    def do_move(self):
        match(self.movimiento):
            case 'r':
                self.add_x(self.velocidad)
                if self.rect.x >= self.max_x:
                    self.movimiento = 'l'
            case 'l':
                self.add_x(self.velocidad * -1)
                if self.rect.x <= self.min_x:
                    self.movimiento = 'r'
            case 'u':
                self.add_y(self.velocidad * -1)
                if self.rect.y <= self.min_x:
                    self.movimiento = 'd'
            case 'd':
                self.add_y(self.velocidad)
                if self.rect.y >= self.max_y:
                    self.movimiento = 'u'
            case _:
                pass