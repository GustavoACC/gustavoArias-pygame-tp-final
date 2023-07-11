import sqlite3
from auxiliar import *

class AuxiliarSQL:

    def generar_scoreboard():
        '''
        Crea la tabla y la base de datos si es que no existen
        '''
        with sqlite3.connect("db/scoreboard.db") as conexion:
            try:
                sentencia = ''' create  table scoreboard
                                (
                                        id integer primary key autoincrement,
                                        nombre text,
                                        level text,
                                        score real
                                )
                            '''
                conexion.execute(sentencia)
                print("Se creo la tabla scoreboard")
            except sqlite3.OperationalError:
                print("La tabla ya existe")
    
    def obtener_mejores_segun_level(form_name):
        '''
        Consulto la base para obtener los mejores 5 dependiendo el nivel jugado
        Devuelvo una lista con los resultados
        '''
        lista_mejores = []
        with sqlite3.connect("db/scoreboard.db") as conexion:
            try:
                sentencia = "select nombre, level, score from scoreboard where level like '{0}' ORDER BY score DESC LIMIT 5".format(form_name)
                cursor=conexion.execute(sentencia)
                for fila in cursor:
                    lista_mejores.append(fila)
            except:
                print("ERROR EN SELECT")
        return lista_mejores

    def insertar_puntaje(form_name, score):
        '''
        Inserto datos en la tabla
        '''
        json_values = Auxiliar.getJsonValues("saves/save_1.json")
        with sqlite3.connect("db/scoreboard.db") as conexion:
            try:
                cursor=conexion.execute("insert into scoreboard(nombre, level, score) values (?,?,?)", (json_values["name"], form_name, score))
            except:
                print("ERROR EN INSERT")

    def revisar_puntaje_scoreboard(form_name, score):
        '''
        Analizo si todavia no hay suficientes partidas guardadas,
        en caso de que ya haya 5 registros reviso si el score a revisar supera alguno de los valores
        '''
        retorno =  0
        mejores_level = AuxiliarSQL.obtener_mejores_segun_level(form_name)
        if len(mejores_level) < 5:
            AuxiliarSQL.insertar_puntaje(form_name, score)
            retorno = 1
        else:
            for fila in mejores_level:
                if score > fila[2]:
                    AuxiliarSQL.insertar_puntaje(form_name, score)
                    retorno = 1
                    break
        return retorno