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
from enemy import *
import math
from auxiliar_sql import *

class FormLevel(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, json_level, csv_level, sub_active):
        '''
        Constructor de la clase y pasaje de los valores a la clase padre
        Inicializo las variables a utilizar
        '''
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active, sub_active)
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
        '''
        Update de la clase,
        En caso de tener un sub formulario activo no actualizo los valores en las clases y guardo el tiempo estimado que estuvo en 
        pausa para restarlo del contador total del nivel ya que el mismo utiliza el tiempo anterior con time
        En caso de iniciarse el formulario por primera vez solicito la carga de valores inicial con el start_config
        Valido en los eventos disponibles la tecla de Esc para comenzar una pausa, y la tecla F10 para un reset forzado al nivel
        En caso de no estar en una pausa solicito la actualizacion de los objetos en pantalla asi como continuar el contador del tiempo disponible del nivel
        '''
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
            self.tiempo_transcurrido = time.time() - self.tiempo_inicio - self.tiempo_total_pausa
        else:
            self.alpha = 200
            return
        for trampa in self.lista_trampas:
            trampa.update(self.pauseState)
        for item in self.lista_items:
            item.update(self.player_instance, self, self.lista_items)
        for enemigo in self.lista_enemigos:
            enemigo.update(self.pauseState, self.lista_enemigos)
        self.tiempo_restante = self.tiempo_maximo - self.tiempo_transcurrido
        self.player_instance.controlar_jugador(keys, delta_ms, self.pauseState)
        self.player_instance.update(self.pauseState, self.tiempo_transcurrido, self)
        self.gui_player.update(self.player_instance.vidas, self.puntaje_total, self.tiempo_restante)
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.mostrar_retry()

    def draw(self): 
        '''
        Metodo del dibujado los objetos en pantalla
        '''
        super().draw()
        self.screen.blit(self.solid_background, self.solid_background.get_rect())
        for plataforma in self.lista_plataformas:
            plataforma.draw(self.screen)
        for pared in self.lista_paredes:
            pared.draw(self.screen)
        for trampa in self.lista_trampas:
            trampa.draw(self.screen)
        for item in self.lista_items:
            item.draw(self.screen)
        for enemigo in self.lista_enemigos:
            enemigo.draw(self.screen)
        self.player_instance.draw(self.screen)
        self.gui_player.draw(self.screen)
        self.solidImagePause.set_alpha(self.alpha)
        self.screen.blit(self.solidImagePause, self.solidImagePause.get_rect())

    def carga_inicial_listas(self):
        '''
        Inicializo las listas desde cero cargandolos según los datos en el Json solicitado
        '''
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
            self.lista_items.append(Item(item["x"], item["y"], int(item["puntos"]), int(item["type"])))
        

    def carga_inicial_jugador(self):
        '''
        Inicializo el jugador según los valores del Json y le paso las listas cargadas de los objetos para validar las colisiones necesarias
        '''
        self.player_instance = Player(self.config_level["player"]["x"],self.config_level["player"]["y"],self.config_level["player"]["vidas"],self.lista_plataformas, self.lista_trampas, self.lista_paredes)

    def cargar_fondo_estatico(self, path):
        '''
        Guardo cual es fondo del nivel para poder dibujarlo entre frames
        '''
        self.solid_background = pygame.image.load(path)
    
    def cargar_json_level(self, json_path):
        '''
        Cargo los valores del json en una variable para que toda la clase pueda acceder
        '''
        self.config_level = Auxiliar.getJsonValues(json_path)
    
    def cargar_csv_level(self, csv_path):
        '''
        Cargo los valores del csv en una variable para que toda la clase pueda acceder
        '''
        self.paredes_level = Auxiliar.getCsvValues(csv_path)

    def start_config(self):
        '''
        Inicializo las variables para un inicio de la partida, incluida las cargas e inicio de la musica
        '''
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
        '''
        Habilito el sub formulario y establezco la flag para no actualizar los valores de los objetos
        '''
        self.pauseState = True
        Form.set_true_sub_active("level_options")

    def mostrar_retry(self):
        '''
        En caso de perder el nivel reproduzco un sonido e inicio la partida nuevamente
        '''
        self.finalizo_nivel = True
        self.pauseState = True
        LOSE.play()
        self.start_config()

    def mostrar_victoria(self):
        '''
        En caso de completar el objetivo del nivel muestro un sub formulario para volver al menu o jugar el siguiente nivel
        Tambien valido el score del jugador para guardarlo si es necesario
        '''
        self.flag_inicio = False
        self.finalizo_nivel = True
        self.pauseState = True

        # Desbloqueo el siguiente nivel y lo guardo en el json
        # Valido si supero algun valor o por primera vez y lo guardo
        is_nuevo_valor = self.is_desbloqueo_local()

        # revisar en bd si supero puntaje
        is_nuevo_score = self.validar_score_bd()

        # Guardo los valores necesarios para mostrar en el formulario de victoria
        ultima_partida_values = Auxiliar.getJsonValues("ultima_partida.json")
        ultima_partida_values["score"] = self.puntaje_total
        ultima_partida_values["local_score"] = is_nuevo_valor
        ultima_partida_values["scoreboard"] = is_nuevo_score
        ultima_partida_values["level"] = self.name
        Auxiliar.setJsonValues("ultima_partida.json", ultima_partida_values)

        # Cargo el form de victoria
        Form.set_active("win_menu")

    def is_desbloqueo_local(self):
        '''
        Valido dependiendo del nivel si es la primera vez jugando, entonces guardo el valor en el json y lo sobreescribo
        Retorno si hubo un cambio en el json
        '''
        retorno =  0
        self.puntaje_total += math.floor(self.tiempo_maximo - self.tiempo_restante) * 100
        json_values = Auxiliar.getJsonValues("saves/save_1.json")
        match self.name:
            case "level_1":
                if json_values["best_time_levels"]["level_1"] == 0:
                    json_values["unlock_levels"]["level_2"] = 1
                    json_values["best_score_levels"]["level_1"] = self.puntaje_total
                    json_values["best_time_levels"]["level_1"] =  math.floor(self.tiempo_maximo - self.tiempo_restante)
                    retorno =  1
            case "level_2":
                if json_values["best_time_levels"]["level_2"] == 0:
                    json_values["unlock_levels"]["level_3"] = 1
                    json_values["best_score_levels"]["level_2"] = self.puntaje_total
                    json_values["best_time_levels"]["level_2"] =  math.floor(self.tiempo_maximo - self.tiempo_restante)
                    retorno =  1
            case "level_3":
                if json_values["best_time_levels"]["level_3"] == 0:
                    json_values["best_score_levels"]["level_3"] = self.puntaje_total
                    json_values["best_time_levels"]["level_3"] =  math.floor(self.tiempo_maximo - self.tiempo_restante)
                    retorno =  1
            case _:
                pass
        Auxiliar.setJsonValues("saves/save_1.json", json_values)
        return retorno
    
    def validar_score_bd(self):
        retorno = AuxiliarSQL.revisar_puntaje_scoreboard(self.name, self.puntaje_total)
        return retorno
    