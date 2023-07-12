import pygame
from player import *
from constantes import *
from auxiliar import *

class Item():
    def __init__(self, x, y, puntos, type):
        '''
        Constructor de la clase y seteo inicial de valores
        '''
        self.puntos = puntos
        self.type = type
        self.frame = 0
        self.animation = self.iniciar_sprites(type)
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collider = pygame.Rect(x, y, self.rect.w, self.rect.h)
        

    def update(self, player, puntaje, lista_items):
        '''
        Update del sprite a mostrar y revision de colision con el jugador
        '''
        self.do_animation()
        self.is_colision(player, puntaje, lista_items)

    def draw(self, screen):
        '''
        Dibujado del objeto en la pantalla solicitada y en caso debug su collider
        '''
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
        if(DEBUG):
            pygame.draw.rect(screen, C_PINK, self.collider)

    def do_animation(self):
        '''
        Actualizacion del valor para mostrar el frame correspondiente a continuacion
        '''
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            self.frame = 0

    def iniciar_sprites(self, type):
        '''
        Inicializo que conjunto de sprites se mostraran dependiendo el tipo solicitado en la creacion
        '''
        match type:
            case 0:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Apple.png", 17, 1)
            case 1:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Bananas.png", 17, 1)
            case 2:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Strawberry.png", 17, 1)
            case 10:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Checkpoints/End/End (Pressed) (64x64).png", 8, 1)
            case _:
                return Auxiliar.getSurfaceFromSpriteSheet("recursos/Items/Fruits/Apple.png", 17, 1)
                
    def is_colision(self, player, form, lista_items):
        '''
        Valido la colision con el jugador para sumar los puntos y reproducir el sonido correspondiente,
        en caso de ser el objeto en este caso tipo 10, se finaliza el juego asi que se llama al metodo del form
        se elimina de la lista si es que colisiono con el jugador
        '''
        if self.rect.colliderect(player.body_collition_rect):
            form.puntaje_total += self.puntos
            self.play_sound()
            if self.type == 10:
                form.mostrar_victoria()
            lista_items.remove(self)
            
    def play_sound(self):
        '''
        Metodo para reproducir el sonido correspondiente del item
        '''
        general_config = Auxiliar.getJsonValues(GENERAL_CONFIG_JSON)
        match self.type:
            case 10:
                VICTORY_ITEM.set_volume(general_config["volume"])
                VICTORY_ITEM.play()
            case _:
                TAKE_ITEM.set_volume(general_config["volume"])
                TAKE_ITEM.play()
