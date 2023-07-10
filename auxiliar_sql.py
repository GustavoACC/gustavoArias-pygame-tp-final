import sqlite3
from auxiliar import *

class AuxiliarSQL:

    def generar_scoreboard():
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
        lista_mejores = []
        with sqlite3.connect("db/scoreboard.db") as conexion:
            try:
                cursor=conexion.execute("select nombre, level, score WHERE level equals {0} FROM scoreboard ORDER BY score DESC LIMIT 5".format(form_name))
                for fila in cursor:
                    lista_mejores.append(fila)
            except:
                print("ERROR EN SELECT")
        print(lista_mejores)
        return lista_mejores

    def insertar_puntaje(form_name, score):
        json_values = Auxiliar.getJsonValues("saves/save_1.json")
        print(json_values["name"])
        print(form_name)
        print(score)
        with sqlite3.connect("db/scoreboard.db") as conexion:
            try:
                cursor=conexion.execute("insert into scoreboard(nombre, level, score) values (?,?,?)", (json_values["name"], form_name, score))
            except:
                print("ERROR EN INSERT")

    def revisar_puntaje_scoreboard(form_name, score):
        retorno =  False
        mejores_level = AuxiliarSQL.obtener_mejores_segun_level(form_name)
        if len(mejores_level) < 5:
            AuxiliarSQL.insertar_puntaje(form_name, score)
            retorno = True
        return retorno