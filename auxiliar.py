import pygame
from constantes import *

class Auxiliar:
    def getSurfaceFromSpriteSheet(path, columnas, filas, flip = False):
        lista = []
        surface_image = pygame.image.load(path)
        fotograma_ancho = int(surface_image.get_width()/columnas)
        fotograma_alto = int(surface_image.get_height()/filas)
        x = 0
        y = 0

        for fila in range(filas):
            for columna in range(columnas):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_image.subsurface(x, y, fotograma_ancho, fotograma_alto)
                if flip:
                    surface_fotograma = pygame.transform.flip(surface_fotograma, True, False)
                lista.append(surface_fotograma)
        return lista
        
        