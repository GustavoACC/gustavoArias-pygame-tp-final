import pygame
from constantes import *
from auxiliar import *

class Plataforma:
    def __init__(self, x, y, w, h, coll_w, coll_h, type=0) -> None:
        self.image = Auxiliar.getSurfaceFromSpriteSheet("recursos/terrain/terrain22x11.png", 22, 11)[type]
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collider = pygame.Rect(x, y, coll_w, coll_h)

    def draw(self, screen):
        if(DEBUG):
            pygame.draw.rect(screen, BLUE, self.collider)
        screen.blit(self.image, self.rect)
        