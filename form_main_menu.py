from constantes import *
from pygame.locals import *
from form import *
from auxiliar import *

class FormMainMenu(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, sub_active, image_background):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active, sub_active, image_background)
        self.active = active
        self.inicio = False
        # self.boton_jugar = Button(master=self,x=446,y=205,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="level_1", text="Level 1", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.boton_opciones = Button(master=self,x=446,y=205,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="options_menu", text="Opciones", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.boton_seleccion_nivel = Button(master=self,x=446,y=280,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="selector_nivel", text="Niveles", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.boton_salir = Button(master=self,x=446,y=350,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_salir, on_click_param="", text="Salir", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)

        self.lista_widget = [self.boton_seleccion_nivel, self.boton_opciones, self.boton_salir]

    def on_click_active_form(self, parametro):
        self.set_active(parametro)

    def on_click_salir(self, parametro):
        pygame.quit()

    def update(self, lista_eventos,keys,delta_ms):
        if self.active and not self.inicio:
            self.inicio = True
            json_values = Auxiliar.getJsonValues("levels/main-menu/start-config.json")
            Auxiliar.playMusic(path=json_values["music"])
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self): 
        super().draw()
        for aux_widget in self.lista_widget:    
            aux_widget.draw()
