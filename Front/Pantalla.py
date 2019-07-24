# coding: latin-1
'''
Created on 4 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio Pérez Oviedo
Librerías extra:
- pygame (1.9.6): para la interfaz gráfica
Biblioteca estándar
- sys: para deterner la ejecución en caso de excepción con sys.exit()
y para obtener los datos de dónde se produce la excepción en el código
- os: para la gestión de ficheros (comprobar si existe, ver en qué fichero
se encuentra la ejecución cuando se produce una excepción...)
'''
import pygame
import os
import sys
"""
Esta clase representa cualquier pantalla del flujo del programa y
de la que todas las clases de este programa la heredarán
"""
class Pantalla:
    #Definimos el constructor, en este caso utilizamos un truco para
    #tener un constructor con parámetros opcionales. Le pasamos
    #un parámetro screen al que por defecto le ponemos None
    #así por defecto será None pero si queremos pasar el parámetro
    def __init__(self,screen = None):
        self.sprite_jugador = None
        self.cartasjugador = None
        self.sprite_ordenador = None
        self.cartasordenador = None
        self.baraja = None
        self.screen = screen
        try:
            #Cargamos la imagen iconoCartas.png
            icon = pygame.image.load("./Front/images/iconoCartas.png")
            #La hacemos el icono de la ventana
            pygame.display.set_icon(icon)
        except Exception as e:
            #Ante cualquier excepción, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepción: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)

    #Este método lo usamos para iniciar la pantalla
    #Y la devolvemos
    def iniciarPantalla(self,width,height,titulo):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(titulo)
        return self.screen