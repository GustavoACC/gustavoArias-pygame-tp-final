from constantes import *
import sys
import pygame
from player import Player
from pygame.locals import *
from static_plataform import *
from mobile_trap import *
from gui_level import *
from form import *
from form_main_menu import *
from form_level import *
from form_opciones import *

screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.init()
clock = pygame.time.Clock()

# Inicio los Forms
form_main_menu = FormMainMenu(name="main_menu", master_surface=screen, x=0, y=0, w=ANCHO_PANTALLA, h=ALTO_PANTALLA, color_background=C_ORANGE, color_border=C_BLUE, active=True, sub_active=False)
form_level_1 = FormLevel(name="level_1", master_surface=screen, x=0, y=0, w=ANCHO_PANTALLA, h=ALTO_PANTALLA, color_background=C_ORANGE, color_border=C_BLUE, active=False, json_level="levels/level-1/start-config.json", csv_level="levels/level-1/paredes_level_1.csv", sub_active=False)
form_option_menu = FormOptionMenu(name="options_menu", master_surface=screen, x=0, y=0, w=ANCHO_PANTALLA, h=ALTO_PANTALLA, color_background=C_ORANGE, color_border=C_BLUE, active=True,sub_active=False, previus_form_name="main_menu")

while True:
    lista_eventos = pygame.event.get()

    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    delta_ms = clock.tick(FPS)
    keys = pygame.key.get_pressed()

    aux_form_active = Form.get_active()
    aux_form_sub_active = Form.get_sub_active()
    if(aux_form_active != None):
        aux_form_active.update(lista_eventos,keys,delta_ms)
        aux_form_active.draw()
    if(aux_form_sub_active != None):
        aux_form_sub_active.update(lista_eventos, keys, delta_ms)
        aux_form_sub_active.draw()

    pygame.display.flip()
