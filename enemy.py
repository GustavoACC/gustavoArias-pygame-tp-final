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

    def __init__(self, x, y, velocidad, tiempo):
        '''
        Constructor del enemigo
        No retorna valores
        '''
        self.iniciar_sprites()
        self.frame = 0
        self.direccion = 1
        self.is_dead = False
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.animation = self.idle_r
        self.imagen = self.animation[self.frame]
        self.velocidad = velocidad
        self.proximo_movimiento = self.set_proximo_movimiento(tiempo)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_body_colision = pygame.Rect(x,y + self.rect.height / 2.5 + 2,self.rect.width, self.rect.height - self.rect.height / 2.5)
        self.rect_height_colision = pygame.Rect(self.rect.x, self.rect.y + self.rect.height / 2.5, self.rect.width, 4)
        self.rect_ground_colision = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, 4)
        
    
    def update(self, pauseState, lista_enemigos, lista_plataformas, lista_paredes, player, tiempo):
        '''
        Update del enemigo
        No retorna valores
        '''
        if pauseState == True:
            return
        self.do_animation()
        if self.is_dead:
            return
        self.lista_paredes = lista_paredes
        self.player= player
        self.lista_enemigos = lista_enemigos
        self.aplicar_gravedad()
        self.is_colision_player()

    def draw(self, screen):
        '''
        Dibujado del enemigo en la pantalla solicitada
        No retorna valores
        '''
        if DEBUG:
            pygame.draw.rect(screen, C_RED, self.rect_body_colision)
            pygame.draw.rect(screen, C_BLACK, self.rect_height_colision)
            pygame.draw.rect(screen, C_WHITE, self.rect_ground_colision)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

    def do_animation(self):
        '''
        Actualiza el sprite a mostrar
        Tambien valida si el enemigo esta en un estado de muerte lo elimina de la lista al finalizar la animacion de hit
        No retorna valores
        '''
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            if self.is_dead:
                ENEMY_DEAD.play()
                self.lista_enemigos.remove(self)
            self.frame = 0

    def aplicar_gravedad(self):
        '''
        En caso de no estar en el limite inferior aplico la gravedad en el eje Y
        No retorna valores
        '''
        if not self.is_min_height() and not self.is_over_something():
            self.add_y(GRAVEDAD)

    def is_min_height(self):
        '''
        Valido si el enemigo se encuentra en el limite inferior vertical establecido en las constantes
        Retorno un booleando con el resultado
        '''
        retorno = False
        if self.rect.y >= GROUND_LEVEL:
            retorno = True
        return retorno
    
    def is_over_something(self):
        retorno = False
        for pared in self.lista_paredes:
            if self.rect_ground_colision.colliderect(pared.collider):
                retorno = True
        return retorno

    def add_y(self, delta_y):
        '''
        Actualizo el valor del eje Y del personaje y sus colisiones,
        tambien valido si en esta nueva posicion se encuentra colisionando con algun suelo
        No retorna valores
        '''
        if delta_y != 0:
            self.rect.y += delta_y
            self.rect_body_colision.y += delta_y
            self.rect_height_colision.y += delta_y
            self.rect_ground_colision.y += delta_y

    def is_colision_player(self):
        '''
        Valido si el enemigo colisiono contra el jugador
        No retorna valores
        '''
        if self.rect_height_colision.colliderect(self.player.ground_collition_rect):
            self.do_muerte()

    def do_muerte(self):
        '''
        Seteo las variables para iniciar el proceso de muerte del personaje
        No retorna valores
        '''
        self.is_dead = True
        self.animation = self.hit
        self.frame = 0

    def set_direccion(self):
        pass

    def set_proximo_movimiento(self, tiempo):
        return tiempo + random.randint(1, 5)