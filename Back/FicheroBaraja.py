# coding: latin-1
'''
Created on 12 may. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio Pérez Oviedo
Biblioteca estándar:
- sys: para deterner la ejecución en caso de excepción con sys.exit()
y para obtener los datos de dónde se produce la excepción en el código
- os: para la gestión de ficheros (comprobar si existe, ver en qué fichero
se encuentra la ejecución cuando se produce una excepción...)
- shutil.copyfile: para copiar el fichero de log en caso de que su tamaño exceda
el máximo configurado
- datetime: Módulo que usamos para obtener el instante actual hasta el microsegundo
para añadir al final del nombre del fichero del log cuando realizamos una copia
Módulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepción
'''
from Front.PantallaError import PantallaError
import sys
import os
from shutil import copyfile
import datetime

"""
Este módulo contiene los métodos con los que controlaremos
el fichero que contiene el estado de la baraja (logs/baraja.txt)
"""
#Definimos una variable global que contiene la ruta donde se encuentra
#el fichero, en este caso en la carpeta logs
RUTA = "./logs/baraja.txt"
#Definimos este método que controla la apertura del archivo
#por defecto el parámetro de entrada ruta apunta a RUTA
def abrirFicheroEscritura(ruta = RUTA):
    #Creamos una variable fichero
    fichero = None
    try:
        #Si el fichero ya existe y el tamaño del fichero es mayor que
        # un determinado valor de bytes
        if os.path.isfile(ruta) and os.path.getsize(ruta) > 100000:
            #Copiamos el fichero baraja.txt a una fichero der back-up
            #que termina el la fecha actual hasta el milisegundo
            copyfile(ruta, ruta+"-"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f"))
            #Borramos el contenido del fichero baraja.txt y
            #lo abrimos para escritura mediante el modo w
            fichero = open(ruta,"w",encoding="utf-8")
        else:
            #En caso contrario tenemos que seguir escribiendo
            #en el fichero baraja.txt para lo que usamos el modo a
            fichero = open(ruta,"a+",encoding="utf-8")
    except FileNotFoundError as e:
        #Ante cualquier excepción, primero imprimimos por 
        #consola un log del error
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Ha ocurrido la siguiente excepción: {0}".format(e))
        print(exc_type, fname, exc_tb.tb_lineno)
        #Atrapamos al excepción que se producirá en el caso de
        #no encontrar el archivo y mostramos la pantalla de error
        pantallaError = PantallaError(r"Falta el fichero {0}".format(ruta))
        pantallaError.mostrarPantallaError()
        sys.exit()
    #Devolvemos el fichero
    return fichero

#Este será el método que usaremos para escribir en el fichero
#con motivo didáctico hemos hecho que reciba ruta, pero también 
#una tupla de parámetros que contendrá los textos a imprimir
#en el archivo
def escribirFichero(ruta,*textos):
    #Abrimos el fichero usando el método que habíamos desarrollado
    #anteriormente
    fichero = abrirFicheroEscritura(ruta)
    try:
        for texto in textos:
            #Cogemos cada línea de la variable sobre la que iteramos
            #Escribimos la línea en el fichero usando write
            fichero.write(texto)
    except FileNotFoundError as e:
        #Ante cualquier excepción, primero imprimimos por 
        #consola un log del error
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Ha ocurrido la siguiente excepción: {0}".format(e))
        print(exc_type, fname, exc_tb.tb_lineno)
        #Atrapamos la excepción de fichero no encontrado
        #y mostramos la pantalla de error
        pantallaError = PantallaError(r"Falta el fichero {0}".format(ruta))
        pantallaError.mostrarPantallaError()
        sys.exit()
    except Exception as e1:
        #Ante cualquier excepción, primero imprimimos por 
        #consola un log del error
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Ha ocurrido la siguiente excepción: {0}".format(e1))
        print(exc_type, fname, exc_tb.tb_lineno)
        #Atrapamos cualquier otra posible excepción y mostramos
        #la pantalla de error
        pantallaError = PantallaError(r"Error al escribir en el fichero {0}".format(ruta))
        pantallaError.mostrarPantallaError()
        sys.exit()
    finally:
        #Usamos finally aquí para asegurarnos de que el fichero 
        #será cerrado siempre. Ya que finally siempre es ejecutado
        #antes de terminar la iteración sobre la estructura try y except
        fichero.close()
        
