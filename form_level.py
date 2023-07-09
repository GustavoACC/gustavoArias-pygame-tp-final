from constantes import *
import sys
import pygame
from player import Player
from pygame.locals import *
from static_plataform import *
from mobile_trap import *
from gui_level import *
from form import *

class FormLevel(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, json_level):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)
        self.screen = master_surface
        self.tiempo_transcurrido = 0
        self.pauseState = False
        self.solidImagePause = pygame.image.load("levels/level-1/background_pause.png")
        self.alpha = 0
        self.cargar_fondo_estatico("levels/level-1/background_1.png")
        self.carga_inicial_listas()
        self.carga_inicial_jugador()
        self.gui_player = Gui_Level(400,30,self.player_instance.vidas)

    def update(self, lista_eventos,keys,delta_ms):
        for event in lista_eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                     self.pauseState = not  self.pauseState
        if self.pauseState == False:
            self.alpha = 0
            self.tiempo_transcurrido += (delta_ms / 1000)
        else:
            self.alpha = 200
        for trampa in self.lista_trampas:
            trampa.update(self.pauseState)
        self.player_instance.controlar_jugador(keys, delta_ms, self.pauseState)
        self.player_instance.update(self.pauseState, self.tiempo_transcurrido)
        self.gui_player.update(self.player_instance.vidas)

    def draw(self): 
        super().draw()
        self.screen.blit(self.solid_background, self.solid_background.get_rect())
        for plataforma in self.lista_plataformas:
            plataforma.draw(self.screen)
        for trampa in self.lista_trampas:
            trampa.draw(self.screen)
        self.player_instance.draw(self.screen)
        self.gui_player.draw(self.screen)
        self.solidImagePause.set_alpha(self.alpha)
        self.screen.blit(self.solidImagePause, self.solidImagePause.get_rect())

    def carga_inicial_listas(self):
        self.lista_plataformas = []
        self.lista_plataformas.append(Plataforma(100,685,16,16,16,5,17))
        self.lista_plataformas.append(Plataforma(116,685,16,16,16,5,18))
        self.lista_plataformas.append(Plataforma(132,685,16,16,16,5,19))
        self.lista_plataformas.append(Plataforma(250,658,16,16,16,5,39))
        self.lista_plataformas.append(Plataforma(266,658,16,16,16,5,40))
        self.lista_plataformas.append(Plataforma(282,658,16,16,16,5,41))
        
        self.lista_paredes = []

        self.lista_trampas = []
        self.lista_trampas.append(Trap(200,700,100,100,0,0,VELOCIDAD_X,'r',0,0,8))
        self.lista_trampas.append(Trap(576,657,0,0,50,50,VELOCIDAD_X,'n',0,1,8))

    def carga_inicial_jugador(self):
        self.player_instance = Player(100,100,2,self.lista_plataformas, self.lista_trampas)

    def cargar_fondo_estatico(self, path):
        self.solid_background = pygame.image.load(path)