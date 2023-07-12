import pygame
from constantes import *
from pygame.locals import *
from auxiliar import *

class Player:

    def iniciar_sprites(self):
        '''
        Guardo las distintas listas de sprites disponibles para el personaje
        No retorna valores
        '''
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/walk.png", 12, 1)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/walk.png", 12, 1, True)
        self.idle_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/idle.png", 11, 1)
        self.idle_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/idle.png", 11, 1, True)
        self.jump_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/jump.png", 1, 1)
        self.jump_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/jump.png", 1, 1, True)
        self.fall_r = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/fall.png", 1, 1)
        self.fall_l = Auxiliar.getSurfaceFromSpriteSheet("recursos/player/fall.png", 1, 1, True)

    def __init__(self, init_x = 0, init_y = 0, init_vidas = 1, lista_plataformas = [], lista_trampas = [], lista_paredes = []):
        '''
        Constructor de la clase, inicializo todos los valores posibles del personaje al comienzo de la partida
        No retorna valores
        '''
        self.iniciar_sprites()
        self.frame = 0
        # Para dar vulnerabilidad al ser golpeado
        self.is_golpeado = False
        self.tiempo_invulnerable = 0
        # Guardo las vidas disponibles
        self.vidas = init_vidas
        # Variables para el salto
        self.flag_salto = False
        self.max_height_jump = MAX_HEIGHT_JUMP
        self.start_jump_y = init_y
        # Las posibles colisiones
        self.lista_plataformas = lista_plataformas
        self.lista_trampas = lista_trampas
        self.lista_paredes = lista_paredes
        # deshabilito el salto hasta que colisione con un suelo
        self.flag_inicio_salto = False
        self.flag_salto_disponible = False
        self.solto_tecla_salto = False
        self.flag_finalizo_salto_anterior = True
        # Guardo la direccion inicial del personaje para los sprites
        self.last_view = "RIGHT"
        self.animation = self.idle_r
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.update_collition_position()
        
    
    def update(self, pauseState, delta_ms, form):
        '''
        Update de la clase, valido si la partida esta en pausa para no actualizar los datos
        No retorna valores
        '''
        if pauseState == True:
            return
        self.do_animation()
        if self.is_golpeado == False:
            self.image.set_alpha(200)
            self.is_colision_enemigo(self.lista_trampas, delta_ms, form)
        else:
            self.is_invulnerable(delta_ms)

    def draw(self, screen):
        '''
        Draw general de la clase, es para aplicar la imagen en la screen disponible del formulario,
        en caso de estar en modo DEBUG muestro las colisiones disponibles del personaje
        No retorno valores
        '''
        if(DEBUG):
            pygame.draw.rect(screen, C_BLACK, self.ground_collition_rect)
            pygame.draw.rect(screen, C_ORANGE, self.body_collition_rect)
            # pygame.draw.rect(screen, C_BLUE, self.rect)
            pygame.draw.rect(screen, C_RED, self.vertical_collition_rect)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
    
    def do_animation(self):
        '''
        Aumenta el valor del frame para mostrar el sprite siguiente en la animacion
        No retorna valores
        '''
        if(self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            self.frame = 0

    def add_x(self, delta_x):
        '''
        Actualizo el valor del eje X del personaje y sus colisiones,
        tambien valido si en esta nueva posicion se encuentra colisionando con alguna pared
        No retorna valores
        '''
        if delta_x != 0:
            self.rect.x += delta_x
            self.update_collition_position()
            self.is_colision_pared_horizontal(self.lista_paredes, delta_x)

    def add_y(self, delta_y):
        '''
        Actualizo el valor del eje Y del personaje y sus colisiones,
        tambien valido si en esta nueva posicion se encuentra colisionando con algun suelo
        No retorna valores
        '''
        if delta_y != 0:
            self.rect.y += delta_y
            self.update_collition_position()
            self.apply_colision_pared_vertical(self.lista_paredes, delta_y)

    def is_on_plataforma(self, lista_plataformas):
        '''
        Valida si el colider del suelo se encuentra en colision directa con alguna plataforma
        Retorna un boolean representando si se encuentra o no en una plataforma
        '''
        retorno = False
        for plataforma in lista_plataformas:
            if self.ground_collition_rect.colliderect(plataforma.collider):
                retorno = True
        return retorno

    def is_colision_pared_horizontal(self, lista_paredes, delta_x):
        '''
        Valido si el personaje se encuentra colisionando directamente con una pared en el eje X y 
        ademas si se encuentra entre los limites descritos en las constantes,
        en caso de que sea asi lo devuelve una posicion anterior
        No retorna valores
        '''
        for pared in lista_paredes:
            if pared.rect.colliderect(self.body_collition_rect) or self.body_collition_rect.x <= LEFT_LEVEL or self.body_collition_rect.x >= RIGHT_LEVEL:
                self.rect.x -= delta_x
                self.update_collition_position()
                
    def apply_colision_pared_vertical(self, lista_paredes, delta_y):
        '''
        Valido si el personaje se encuentra colisionando directamente con una pared en el eje Y,
        en caso de que sea asi lo devuelve una posicion anterior y habilita las flags de disponibilidad de salto
        No retorna valores
        '''
        for pared in lista_paredes:
            if pared.rect.colliderect(self.body_collition_rect):
                if delta_y > 0:
                    self.rect.bottom = pared.rect.top
                    self.update_collition_position()
                    self.flag_salto_disponible = True
                elif delta_y < 0:
                    self.rect.top = pared.rect.bottom
                    self.update_collition_position()
                    self.solto_tecla_salto = True
                    self.flag_salto_disponible = False

    def is_colision_vertical(self, lista_paredes, delta_y):
        '''
        Devuelvo si el personaje colisiono de forma vertical contra un techo
        Retorno un booleando representando el resultado
        '''
        retorno = False
        for pared in lista_paredes:
            if pared.rect.colliderect(self.vertical_collition_rect):
                if delta_y > 0:
                    retorno = True
        return retorno

    def update_collition_position(self):
        '''
        Actualiza la posicion de los colliders en base al rect principal para mantenerlos en la correcta posicion
        No retorna valores
        '''
        self.vertical_collition_rect = pygame.Rect(self.rect.x + self.rect.w / 3.5, self.rect.y, self.rect.w / 2, self.rect.h + 1)
        self.ground_collition_rect = pygame.Rect(self.rect.x + self.rect.w / 2.5, (self.rect.y + self.rect.h), self.rect.w / 2.5, 2)
        self.body_collition_rect = pygame.Rect(self.rect.x + self.rect.w / 3.5, self.rect.y + self.rect.h / 3.5, self.rect.w / 2, self.rect.h / 1.5)

    def is_max_min_height(self):
        '''
        Valido si el personaje se encuentra entre los limites verticales establecidos en las constantes
        Retorno un booleando con el resultado
        '''
        retorno = False
        if self.rect.y >= GROUND_LEVEL or self.rect.y <= HIGH_LEVEL:
            retorno = True
        return retorno

    def is_colision_enemigo(self, lista_trampas, delta_ms, form):
        '''
        Valido si el cuerpo del personaje colisiono contra una trampa u enemigo,
        actualizo las vidas disponibles, reproduzco un sonido y habilito la invulneabilidad para no recibir golpes consecutivos
        No retorno valores
        '''
        for trampa in lista_trampas:
            if self.body_collition_rect.colliderect(trampa.collider):
                HIT.play()
                self.vidas -= 1
                self.is_golpeado = True
                self.tiempo_invulnerable = delta_ms +  2
                if self.vidas == 0:
                    form.mostrar_retry()
                
    def is_invulnerable(self, delta_ms):
        '''
        En caso de haber colisionado (flag) bajo el valor de alpha en el sprite y
        valido si pasaron los suficientes ticks para disponibilizar el daño nuevamente
        No retorno valores
        '''
        if self.is_golpeado == True:
            self.image.set_alpha(50)
            if delta_ms > self.tiempo_invulnerable:
                self.is_golpeado = False

    def do_movement(self, action, x = 0, y = 0):
        '''
        Llamo a los metodos para actualizar las posiciones de los ejes
        y seteo que sprites se necesitan dibujar en pantalla
        No retorno valores
        '''
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
        '''
        Valido si se encuentra en alguna plataforma, suelo o limite vertical
        en caso que no este en ninguno aplico el valor de gravedad declarado en las constantes en el eje Y,
        caso contrario si esta sobre alguna habilito las flags de salto
        No retorno valores
        '''
        if not self.is_max_min_height() and not self.is_on_plataforma(self.lista_plataformas) and not self.is_colision_vertical(self.lista_paredes, GRAVEDAD):
            self.do_movement("FALL", y = GRAVEDAD)
            self.aplicando_gravedad = True
        else:
            # En caso de tocar el suelo activo el salto
            self.aplicando_gravedad = False
            self.flag_salto_disponible = True
            self.flag_finalizo_salto_anterior = True
            self.flag_inicio_salto = False
            self.solto_tecla_salto = True
    
    def controlar_jugador(self, pressed_keys, delta_ms, pauseState):
        '''
        En caso de estado de pausa no realizo ninguna actualizacion de datos,
        caso contrario valido las teclas precionadas para setear la actualizacion de ejes y el set de sprites a utilizar,
        llamo de manera constante a la aplicacion de gravedad al final para que setee los sprites en caso de una caida
        No retorno valores
        '''
        if pauseState == True:
            return

        if True in pressed_keys:
            if pressed_keys[K_d]:
                self.do_movement("WALK_RIGHT", x = VELOCIDAD_X)
            if pressed_keys[K_a]:
                self.do_movement("WALK_LEFT", x = VELOCIDAD_X * -1)
            if pressed_keys[K_w]:
                if self.flag_salto_disponible == True:
                    if self.flag_inicio_salto == False and self.solto_tecla_salto == True and self.flag_finalizo_salto_anterior == True:
                        self.flag_inicio_salto = True
                        self.flag_finalizo_salto_anterior = False
                        self.solto_tecla_salto = False
                        self.start_jump_y = self.rect.y
                        self.max_height_jump = self.start_jump_y - MAX_HEIGHT_JUMP
                        self.do_movement("JUMP", y = VELOCIDAD_Y * -1)
                    elif self.flag_inicio_salto == True and (self.rect.y > self.max_height_jump) and self.solto_tecla_salto == False and self.flag_finalizo_salto_anterior == False:
                        self.do_movement("JUMP", y = VELOCIDAD_Y * -1)
                    elif self.rect.y <= self.max_height_jump or self.solto_tecla_salto == True:
                        self.flag_salto_disponible = False
                        self.flag_finalizo_salto_anterior = True
                else:
                    pass
            if not pressed_keys[K_w]:
                self.solto_tecla_salto = True
        else:
            self.solto_tecla_salto = True
            self.do_movement("STAY")

        # Aplico la gravedad siempre
        self.aplicar_gravedad()
