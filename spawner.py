from player import *
from enemy import *
import random

class Spawner:

    def __init__(self, lista_enemigos = [], lista_spawn_enemigo = [], flag_spawn = 0, tiempo_transcurrido = 0):
        '''
        Constructor de la clase
        Seteo el tiempo del proximo spawn
        '''
        self.lista_enemigos = lista_enemigos
        self.lista_posiciones_disponibles = lista_spawn_enemigo
        self.flag_spawn = flag_spawn
        self.tiempo_proximo_spawn = tiempo_transcurrido + 5

    def update(self, player, lista_enemigos, tiempo_transcurrido):
        '''
        update de la clase
        llamo al proceso de validacion de generacion de enemigos
        '''
        self.player = player
        self.lista_enemigos = lista_enemigos
        if self.flag_spawn == 1:
            self.proceso_spawn_enemigo(tiempo_transcurrido)
    
    def proceso_spawn_enemigo(self, tiempo_transcurrido):
        '''
        Valido el tiempo trancurrido y en caso de alcanzar el anterior seteo un nuevo tiempo
        '''
        if tiempo_transcurrido > self.tiempo_proximo_spawn:
            self.tiempo_proximo_spawn += random.randint(2,5)
            self.spawnear_enemigo(tiempo_transcurrido)

    def spawnear_enemigo(self, tiempo_transcurrido):
        '''
        Genero un numero aleatorio para seleccionar una posicion
        Una vez tengo la posicion reviso si la misma no se encuentra muy cerca del personaje utilizando la colision
        En caso de estar lejos agrego un nuevo enemigo a la lista
        '''
        random_tile = random.randint(0, (len(self.lista_posiciones_disponibles)-1))
        selected_tile = self.lista_posiciones_disponibles[random_tile]
        if not selected_tile.collider.colliderect(self.player.rect):
            self.lista_enemigos.append(Enemy(selected_tile.rect.x, selected_tile.rect.y - 4, VELOCIDAD_X, tiempo_transcurrido))