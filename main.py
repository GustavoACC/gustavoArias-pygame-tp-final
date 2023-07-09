from constantes import *
import sys
import pygame
from player import Player
from pygame.locals import *
from static_plataform import *
from mobile_trap import *
from gui_level import *


screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.init()
clock = pygame.time.Clock()

# fondo solido
pathSolidBackground = "levels/level-1/background_1.png"
solidImagePause = pygame.image.load("levels/level-1/background_pause.png")
alpha = 0
pauseState = False
# plataformas
lista_plataformas = []
lista_plataformas.append(Plataforma(100,685,16,16,16,5,17))
lista_plataformas.append(Plataforma(116,685,16,16,16,5,18))
lista_plataformas.append(Plataforma(132,685,16,16,16,5,19))
lista_plataformas.append(Plataforma(250,658,16,16,16,5,39))
lista_plataformas.append(Plataforma(266,658,16,16,16,5,40))
lista_plataformas.append(Plataforma(282,658,16,16,16,5,41))

# paderes
lista_paredes = []

# trampas
lista_trampas = []
lista_trampas.append(Trap(200,700,100,100,0,0,VELOCIDAD_X,'r',0,0,8))
lista_trampas.append(Trap(576,657,0,0,50,50,VELOCIDAD_X,'n',0,1,8))

# player
player_instance = Player(100,100,2,lista_plataformas, lista_trampas)

# Gui inicial
gui_player = Gui_Level(400,30,player_instance.vidas)

# Inicio el tiempo
tiempo_transcurrido = 0

while True:
    delta_ms = clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pauseState = not pauseState

    # Draw Background
    solid_background = pygame.image.load(pathSolidBackground)
    screen.blit(solid_background, solid_background.get_rect())
    
    # Obtencion de teclas   
    pressed_keys = pygame.key.get_pressed()

    # Draw Plataformas
    for plataforma in lista_plataformas:
        plataforma.draw(screen)

    if pauseState == True:
        alpha = 200
    else:
        alpha = 0
    
    # Draw Trampas
    for trampa in lista_trampas:
        trampa.update(pauseState)
        trampa.draw(screen)
    
    # Si no estoy en pausa sumo al tiempo de partida
    if pauseState == False:
        tiempo_transcurrido += (delta_ms / 1000)

    # UPDATE VALORES
    player_instance.controlar_jugador(pressed_keys, delta_ms, pauseState)
    player_instance.update(pauseState, tiempo_transcurrido)
    player_instance.draw(screen)

    # Update Gui
    gui_player.update(player_instance.vidas)
    gui_player.draw(screen)
    
    solidImagePause.set_alpha(alpha)
    screen.blit(solidImagePause, solidImagePause.get_rect())

    pygame.display.flip()
