from constantes import *
import pygame
from player import Player
from pygame.locals import *
from static_plataform import *
from mobile_trap import *
from gui_level import *
from form import *
from auxiliar import *
from item import *
import time
from form_main_menu import *
from form_level import *
from form_opciones import *

class FormLevel(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, json_level, csv_level, sub_active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active, sub_active, None)
        self.form_option_menu = FormOptionMenu(name="level_options", master_surface=master_surface, x=0, y=0, w=ANCHO_PANTALLA, h=ALTO_PANTALLA, color_background=C_ORANGE, color_border=C_BLUE, active=False,sub_active=False, previus_form_name=name)
        self.active = active
        self.name = name
        self.screen = master_surface
        self.json_level = json_level
        self.csv_level = csv_level
        self.flag_inicio = False
        self.finalizo_nivel = False
        self.finalizo_pausa = True

    def update(self, lista_eventos,keys,delta_ms):
        aux_sub_active_form = Form.get_sub_active()
        if(aux_sub_active_form != None):
            self.finalizo_pausa = False
            return
        else:
            # Guardo el tiempo total de la pausa para poder restarlo del tiempo transcurrido
            if not self.finalizo_pausa:
                self.tiempo_transcurrido_en_pausa = time.time() - self.tiempo_inicio_pausa
                self.tiempo_total_pausa += self.tiempo_transcurrido_en_pausa
                self.finalizo_pausa = True
            self.pauseState = False
        if self.active and self.flag_inicio == False:
            self.flag_inicio = True
            self.start_config()
        for event in lista_eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                     self.pauseState = not self.pauseState
                if event.key == pygame.K_F10:
                    self.start_config()
                if self.pauseState and not self.finalizo_nivel:
                    self.tiempo_inicio_pausa = time.time()
                    self.mostrar_pausa()
        if self.pauseState == False:
            self.alpha = 0
            # if not self.finalizo_pausa:
            #     self.finalizo_pausa = True
            self.tiempo_transcurrido = time.time() - self.tiempo_inicio - self.tiempo_total_pausa
        else:
            self.alpha = 200
            return
        for trampa in self.lista_trampas:
            trampa.update(self.pauseState)
        for item in self.lista_items:
            item.update(self.player_instance, self, self.lista_items)
        self.tiempo_restante = self.tiempo_maximo - self.tiempo_transcurrido
        self.player_instance.controlar_jugador(keys, delta_ms, self.pauseState)
        self.player_instance.update(self.pauseState, self.tiempo_transcurrido, self)
        self.gui_player.update(self.player_instance.vidas, self.puntaje_total, self.tiempo_restante)
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.mostrar_retry()

    def draw(self): 
        super().draw()
        self.screen.blit(self.solid_background, self.solid_background.get_rect())
        for plataforma in self.lista_plataformas:
            plataforma.draw(self.screen)
        for pared in self.lista_paredes:
            pared.draw(self.screen)
        for trampa in self.lista_trampas:
            trampa.draw(self.screen)
        for item in self.lista_items:
            item.draw()
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
        
        self.lista_items = []
        for item in self.config_level["items"]:
            self.lista_items.append(Item(self.screen, item["x"], item["y"], int(item["puntos"]), int(item["type"])))

    def carga_inicial_jugador(self):
        self.player_instance = Player(self.config_level["player"]["x"],self.config_level["player"]["y"],self.config_level["player"]["vidas"],self.lista_plataformas, self.lista_trampas, self.lista_paredes)

    def cargar_fondo_estatico(self, path):
        self.solid_background = pygame.image.load(path)
    
    def cargar_json_level(self, json_path):
        self.config_level = Auxiliar.getJsonValues(json_path)
    
    def cargar_csv_level(self, csv_path):
        self.paredes_level = Auxiliar.getCsvValues(csv_path)

    def start_config(self):
        self.tiempo_inicio_pausa = time.time()
        self.tiempo_transcurrido_en_pausa = 0
        self.tiempo_total_pausa = 0
        self.finalizo_pausa = True
        self.tiempo_transcurrido = 0
        self.tiempo_inicio = time.time()
        self.puntaje_total = 0
        self.pauseState = False
        self.solidImagePause = pygame.image.load("levels/level-1/background_pause.png")
        self.alpha = 0
        self.cargar_fondo_estatico("levels/level-1/background_1.png")
        self.cargar_json_level(self.json_level)
        self.tiempo_maximo = self.config_level["tiempo"]
        self.cargar_csv_level(self.csv_level)
        self.carga_inicial_listas()
        self.carga_inicial_jugador()
        self.gui_player = Gui_Level(self.player_instance.vidas, self.puntaje_total, self.tiempo_maximo)
        Auxiliar.playMusic(self.config_level["music"])

    def mostrar_pausa(self):
        self.pauseState = True
        Form.set_true_sub_active("level_options")

    def mostrar_retry(self):
        self.finalizo_nivel = True
        self.pauseState = True
        LOSE.play()
        # Form.set_true_sub_active("level_options")
        self.start_config()

    def mostrar_victoria(self):
        self.finalizo_nivel = True
        self.pauseState = True
        print("CARGAR FORM VICTORIA")
        # revisar en bd si supero puntaje
        # unlock level 2
