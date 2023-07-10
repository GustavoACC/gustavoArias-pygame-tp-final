import pygame
from player import *
from constantes import *
from auxiliar import *

class Item():
    def __init__(self, screen, x, y, puntos, type):
        self.screen = screen
        self.puntos = puntos
        self.frame = 0
        self.animation = self.iniciar_sprites(type)
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collider = pygame.Rect(x, y, self.rect.w, self.rect.h)
        

    def update(self, player, puntaje, lista_items):
        self.do_animation()
        self.is_colision(player, puntaje, lista_items)

    def draw(self):
        self.image = self.animation[self.frame]
        self.screen.blit(self.image, self.rect)
        if(DEBUG):
            pygame.draw.rect(self.screen, C_PINK, self.collider)

    def do_animation(self):
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            self.frame = 0

    def iniciar_sprites(self, type):
        match type:
            case 0:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Apple.png", 17, 1)
            case 1:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Bananas.png", 17, 1)
            case 10:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Checkpoints/End/End (Pressed) (64x64).png", 8, 1)
            case _:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Apple.png", 17, 1)
                
    def is_colision(self, player, form, lista_items):
        if self.rect.colliderect(player.rect):
            general_config = Auxiliar.getJsonValues(GENERAL_CONFIG_JSON)
            TAKE_ITEM.set_volume(general_config["volume"])
            TAKE_ITEM.play()
            form.puntaje_total += self.puntos
            lista_items.remove(self)
            
