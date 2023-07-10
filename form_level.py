from constantes import *
import pygame
from player import Player
from pygame.locals import *
from static_plataform import *
from mobile_trap import *
from gui_level import *
from form import *
from auxiliar import *

class FormLevel(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, json_level, csv_level):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)
        self.screen = master_surface
        self.tiempo_transcurrido = 0
        self.pauseState = False
        self.solidImagePause = pygame.image.load("levels/level-1/background_pause.png")
        self.alpha = 0
        self.cargar_fondo_estatico("levels/level-1/background_1.png")
        self.cargar_json_level(json_level)
        self.cargar_csv_level(csv_level)
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
        for pared in self.lista_paredes:
            pared.draw(self.screen)
        for trampa in self.lista_trampas:
            trampa.draw(self.screen)
        self.player_instance.draw(self.screen)
        self.gui_player.draw(self.screen)
        self.solidImagePause.set_alpha(self.alpha)
        self.screen.blit(self.solidImagePause, self.solidImagePause.get_rect())

    def carga_inicial_listas(self):
        self.lista_plataformas = []
        for plataforma in self.config_level["plataformas"]:
            self.lista_plataformas.append(Plataforma(plataforma["x"],plataforma["y"],plataforma["w"],plataforma["h"],plataforma["coll_w"],plataforma["coll_h"],plataforma["type"]))
        
        self.lista_paredes = []
        for indexFila, row in enumerate(self.paredes_level):
            for indexColumna, item in enumerate(row):
                if item != "-1":
                    x = (indexColumna + 2) * 16
                    y = (indexFila + 7) * 16
                    self.lista_paredes.append(Plataforma(x, y, 16, 16,16,16, int(item)))
        
        self.lista_trampas = []
        for trampa in self.config_level["trampas"]:
            self.lista_trampas.append(Trap(trampa["x"],trampa["y"],trampa["min_x"],trampa["max_x"],trampa["min_y"],trampa["max_y"],trampa["velocidad"],trampa["movimiento"],trampa["type"],trampa["sub_type"],trampa["col_rest"]))


    def carga_inicial_jugador(self):
        self.player_instance = Player(self.config_level["player"]["x"],self.config_level["player"]["y"],self.config_level["player"]["vidas"],self.lista_plataformas, self.lista_trampas, self.lista_paredes)

    def cargar_fondo_estatico(self, path):
        self.solid_background = pygame.image.load(path)
    
    def cargar_json_level(self, json_path):
        self.config_level = Auxiliar.getJsonValues(json_path)
    
    def cargar_csv_level(self, csv_path):
        self.paredes_level = Auxiliar.getCsvValues(csv_path)
