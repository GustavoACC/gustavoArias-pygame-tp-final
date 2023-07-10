import pygame
from constantes import *
import json
import csv

class Auxiliar:
    def getSurfaceFromSpriteSheet(path, columnas, filas, flip = False):
        '''
        Obtengo la lista de sprites según su cantidad de columnas y filas, tambien realizo un flip de ser requerido
        Devuelvo la lista de sprites
        '''
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
        '''
        Levanto el json para obtener sus valores
        Devuelvo los valores del json
        '''
        with open(path) as archivo:
            return json.load(archivo)
        
    def getCsvValues(path):
        '''
        Levanto el archivo csv para obtener sus valores
        y los agrego a una lista para poder leerlos de manera ordenada
        Devuelvo una lista con los valores de cada fila del csv
        '''
        with open(path) as archivo:
            csv_filas = []
            csv_reader = csv.reader(archivo)
            for row in csv_reader:
                csv_filas.append(row)
            return csv_filas
        
    def playMusic(path):
        '''
        Reproduzco musica en el mixer deteniendo toda musica previa
        '''
        general_config = Auxiliar.getJsonValues(GENERAL_CONFIG_JSON)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(5)
        pygame.mixer.music.set_volume(general_config["volume"])
    
    def setJsonValues(path, values):
        '''
        Escribo el objeto solicitado en el path como un json
        '''
        with open(path, 'w') as archivo:
            json.dump(values, archivo)
