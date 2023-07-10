import pygame
from constantes import *
import json
import csv

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
        
    def getJsonValues(path):
        with open(path) as archivo:
            return json.load(archivo)
        
    def getCsvValues(path):
        with open(path) as archivo:
            csv_filas = []
            csv_reader = csv.reader(archivo)
            for row in csv_reader:
                csv_filas.append(row)
            return csv_filas
        
    def playMusic(path):
        general_config = Auxiliar.getJsonValues(GENERAL_CONFIG_JSON)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(5)
        pygame.mixer.music.set_volume(general_config["volume"])
    
    def setJsonValues(path, values):
        with open(path, 'w') as archivo:
            json.dump(values, archivo)
