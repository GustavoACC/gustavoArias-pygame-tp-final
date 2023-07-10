from constantes import *
from pygame.locals import *
from form import *
from auxiliar import *

class FormOptionMenu(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active, sub_active, previus_form_name):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active, sub_active)
        self.previus_form_name = previus_form_name
        self.boton_subir_volumen = Button(master=self,x=446,y=205,w=250,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_modificar_volumen, on_click_param=0.1, text="Subir Volumen", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.boton_bajar_volumen = Button(master=self,x=446,y=275,w=250,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_modificar_volumen, on_click_param=-0.1, text="Bajar Volumen", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)
        self.boton_volver = Button(master=self,x=502,y=335,w=140,h=50,image_background="UI_Flat_Frame_01_Horizontal.png", on_click=self.on_click_volver, on_click_param=None, text="Volver", font="fonts/Minecraft.ttf", font_size=30, font_color=C_WHITE)

        self.lista_widget = [self.boton_subir_volumen, self.boton_bajar_volumen, self.boton_volver]

    def on_click_modificar_volumen(self, parametro):
        general_config = Auxiliar.getJsonValues(GENERAL_CONFIG_JSON)
        if general_config["volume"] <= 0 and parametro == -0.1:
            return
        elif general_config["volume"] >= 1 and parametro == 0.1:
            return
        general_config["volume"] += parametro
        pygame.mixer.music.set_volume(general_config["volume"])
        Auxiliar.setJsonValues(path=GENERAL_CONFIG_JSON,values=general_config)
    
    def on_click_volver(self, parametro):
        match self.previus_form_name:
            case "main_menu":
                self.set_active("main_menu")
            case _:
                Form.set_false_sub_active()

    def update(self, lista_eventos,keys,delta_ms):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)

    def draw(self): 
        super().draw()
        for aux_widget in self.lista_widget:    
            aux_widget.draw()
