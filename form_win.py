from constantes import *
from pygame.locals import *
from form import *
from auxiliar import *
from gui_label import *

class FormWinMenu(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, sub_active):
        '''
        Constructor de la clase,
        Inicializo los botones para presentarlos
        '''
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active, sub_active)
        self.ultima_partida_values = Auxiliar.getJsonValues("ultima_partida.json")
        self.label_puntaje_final = Label(master=self, x=400, y=100, w=200, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text="Puntaje Final", font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        self.label_puntaje_final_valor = Label(master=self, x=610, y=100, w=200, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text=self.ultima_partida_values["score"], font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        self.boton_inicio = Button(master=self,x=502,y=400,w=140,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.set_active, on_click_param="main_menu", text="Menu", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.label_registro_scoreboard = Label(master=self, x=400, y=250, w=400, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text="Nuevo Record en Scoreboard", font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        self.label_registro_local = Label(master=self, x=400, y=175, w=400, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text="Nuevo Record en Local", font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        
        self.lista_widget = [self.boton_inicio, self.label_puntaje_final, self.label_puntaje_final_valor]

    def update(self, lista_eventos,keys,delta_ms):
        '''
        Actualizo los datos buscandolos en el json para mostrar los datos correctos
        '''
        self.ultima_partida_values = Auxiliar.getJsonValues("ultima_partida.json")
        self.label_puntaje_final_valor = Label(master=self, x=610, y=100, w=200, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text=self.ultima_partida_values["score"], font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        self.label_registro_scoreboard = Label(master=self, x=400, y=250, w=400, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text="Nuevo Record en Scoreboard", font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        self.label_registro_local = Label(master=self, x=400, y=175, w=400, h=50, color_border=C_BLACK, image_background="UI_Flat_Frame_01_Horizontal.png", text="Nuevo Record en Local", font="fonts/Minecraft.ttf", font_size=25, font_color=C_WHITE)
        self.lista_widget.append(self.label_puntaje_final_valor)
        if self.ultima_partida_values["local_score"] == 1:
            self.lista_widget.append(self.label_registro_local)
        else:
            if self.label_registro_local in self.lista_widget:
                self.lista_widget.remove(self.label_registro_local)
        if self.ultima_partida_values["scoreboard"] == 1:
            self.lista_widget.append(self.label_registro_scoreboard)
        else:
            if self.label_registro_scoreboard in self.lista_widget:
                self.lista_widget.remove(self.label_registro_scoreboard)
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self):
        super().draw()
        for aux_widget in self.lista_widget:    
            aux_widget.draw()
