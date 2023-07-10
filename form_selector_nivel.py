from constantes import *
from pygame.locals import *
from form import *
from auxiliar import *

class FormSelectorMenu(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, sub_active, previus_form_name):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active, sub_active)
        self.previus_form_name = previus_form_name
        self.boton_volver = Button(master=self,x=446,y=375,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="main_menu", text="Volver", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.lista_widget = [self.boton_volver]
        self.validar_niveles_desbloquedos()
    
    def on_click_active_form(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos,keys,delta_ms):
        self.validar_niveles_desbloquedos()
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self): 
        super().draw()
        for aux_widget in self.lista_widget:    
            aux_widget.draw()

    def validar_niveles_desbloquedos(self):
        json_values = Auxiliar.getJsonValues("saves/save_1.json")
        for level in json_values["unlock_levels"]:
            match level:
                case "level_1":
                    if json_values["unlock_levels"][level] == 1:
                        self.boton_level_1 = Button(master=self,x=446,y=150,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="level_1", text="Level 1", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
                        self.lista_widget.append(self.boton_level_1)
                case "level_2":
                    if json_values["unlock_levels"][level] == 1:
                        self.boton_level_2 = Button(master=self,x=446,y=225,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="level_2", text="Level 2", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
                        self.lista_widget.append(self.boton_level_2)
                case "level_3":
                    if json_values["unlock_levels"][level] == 1:
                        self.boton_level_3 = Button(master=self,x=446,y=300,w=170,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_active_form, on_click_param="level_3", text="Level 3", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
                        self.lista_widget.append(self.boton_level_3)
                case _:
                    pass