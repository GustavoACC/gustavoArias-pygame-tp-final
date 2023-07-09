import pygame
from constantes import *
from pygame.locals import *
from auxiliar import *

class Player:

    def iniciar_sprites(self):
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/walk.png", 12, 1)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/walk.png", 12, 1, True)
        self.idle_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/idle.png", 11, 1)
        self.idle_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/idle.png", 11, 1, True)
        self.jump_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/jump.png", 1, 1)
        self.jump_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/jump.png", 1, 1, True)
        self.fall_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/fall.png", 1, 1)
        self.fall_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/fall.png", 1, 1, True)

    def __init__(self, init_x = 0, init_y = 0, init_vidas = 1, lista_plataformas = [], lista_trampas = []) -> None:
        self.iniciar_sprites()
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        # Para dar vulnerabilidad al ser golpeado
        self.is_golpeado = False
        self.tiempo_invulnerable = 0
        self.vidas = init_vidas
        self.flag_salto = False
        self.max_height_jump = MAX_HEIGHT_JUMP
        self.start_jump_y = init_y
        # guardo las posibles colisiones
        self.lista_plataformas = lista_plataformas
        self.lista_trampas = lista_trampas

        self.last_view = "RIGHT"
        self.flag_inicio_salto = False
        self.flag_salto_disponible = False
        self.solto_tecla_salto = False
        self.flag_finalizo_salto_anterior = True
        self.animation = self.idle_r
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.ground_collition_rect = pygame.Rect(self.rect.x + self.rect.w / 2.5, (self.rect.y + self.rect.h), self.rect.w / 2.5, 2)
        self.body_collition_rect = pygame.Rect(self.rect.x + self.rect.w / 3.5, self.rect.y + self.rect.h / 3.5, self.rect.w / 2, self.rect.h / 1.5)
    
    def update(self, pauseState, delta_ms):
        if pauseState == True:
            return
        self.do_animation()
        if self.is_golpeado == False:
            self.image.set_alpha(200)
            self.is_colision_enemigo(self.lista_trampas, delta_ms)
        else:
            self.is_invulnerable(delta_ms)

    def draw(self, screen):
        if(DEBUG):
            pygame.draw.rect(screen, C_RED, self.rect)
            pygame.draw.rect(screen, C_BLUE, self.ground_collition_rect)
            pygame.draw.rect(screen, C_GREEN, self.body_collition_rect)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
    
    def do_animation(self):
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            self.frame = 0

    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.ground_collition_rect.x += delta_x
        self.body_collition_rect.x += delta_x

    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.ground_collition_rect.y += delta_y
        self.body_collition_rect.y += delta_y

    def is_on_plataforma(self, lista_plataformas):
        retorno = False
        if self.rect.y >= GROUND_LEVEL - 34:
            retorno = True
        else:
            for plataforma in lista_plataformas:
                if self.ground_collition_rect.colliderect(plataforma.collider):
                    retorno = True
        return retorno

    def is_colision_enemigo(self, lista_trampas, delta_ms):
        for trampa in lista_trampas:
            if self.body_collition_rect.colliderect(trampa.collider):
                self.vidas -= 1
                self.is_golpeado = True
                self.tiempo_invulnerable = delta_ms +  2
                
    def is_invulnerable(self, delta_ms):
        if self.is_golpeado == True:
            self.image.set_alpha(50)
            if delta_ms > self.tiempo_invulnerable:
                self.is_golpeado = False

    def movement(self, action, x = 0, y = 0):
        self.add_x(x)
        self.add_y(y)
        if(action == "WALK_RIGHT"):
            self.last_view = "RIGHT"
            self.animation = self.walk_r
        elif(action == "WALK_LEFT"):
            self.last_view = "LEFT"
            self.animation = self.walk_l
        elif(action == "FALL"):
            if(self.last_view == "RIGHT"):
                self.animation = self.fall_r
            else:
                self.animation = self.fall_l
        elif(action == "JUMP"):
            if(self.last_view == "RIGHT"):
                self.animation = self.jump_r
            else:
                self.animation = self.jump_l
        elif(action == "STAY"):
            if(self.last_view == 'RIGHT'):
                self.animation = self.idle_r
            else:
                self.animation = self.idle_l

    def aplicar_gravedad(self):
        # TODO cambiar por si esta o no sobre una plataforma
        if not self.is_on_plataforma(self.lista_plataformas):
            self.movement("FALL", y = GRAVEDAD)
        else:
            # En caso de tocar el suelo minimo activo el salto
            self.flag_salto_disponible = True
            # TODO agregar donde analize si toco suelo
            self.flag_finalizo_salto_anterior = True
            self.flag_inicio_salto = False

    def validar_salto(self):
        if self.flag_salto_disponible == True and self.flag_inicio_salto == True:
            self.flag_inicio_salto = False
            self.flag_salto_disponible = False
            self.solto_tecla_salto = True
        else:
            self.solto_tecla_salto = False
    
    def controlar_jugador(self, pressed_keys, delta_ms, pauseState):
        if pauseState == True:
            return
        if True in pressed_keys:
            if pressed_keys[K_d]:
                self.movement("WALK_RIGHT", x = VELOCIDAD_X)
            if pressed_keys[K_a]:
                self.movement("WALK_LEFT", x = VELOCIDAD_X * -1)
            if pressed_keys[K_w]:
                if self.flag_salto_disponible == True:
                    if self.flag_inicio_salto == False and self.solto_tecla_salto == True and self.flag_finalizo_salto_anterior == True:
                        self.flag_inicio_salto = True
                        self.flag_finalizo_salto_anterior = False
                        self.solto_tecla_salto = False
                        self.start_jump_y = self.rect.y
                        self.max_height_jump = self.start_jump_y - MAX_HEIGHT_JUMP
                        self.movement("JUMP", y = VELOCIDAD_Y * -1)
                    elif self.flag_inicio_salto == True and (self.rect.y > self.max_height_jump) and self.solto_tecla_salto == False and self.flag_finalizo_salto_anterior == False:
                        self.movement("JUMP", y = VELOCIDAD_Y * -1)
                    elif self.rect.y <= self.max_height_jump or self.solto_tecla_salto == True:
                        self.flag_salto_disponible = False
                else:
                    pass
            if not pressed_keys[K_w]:
                self.solto_tecla_salto = True
        else:
            self.solto_tecla_salto = True
            self.movement("STAY",0,0)

        # Aplico la gravedad siempre
        self.aplicar_gravedad()
