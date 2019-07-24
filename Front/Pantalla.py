# coding: latin-1
'''
Created on 4 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pygame (1.9.6): para la interfaz gr�fica
Biblioteca est�ndar
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
- os: para la gesti�n de ficheros (comprobar si existe, ver en qu� fichero
se encuentra la ejecuci�n cuando se produce una excepci�n...)
'''
import pygame
import os
import sys
"""
Esta clase representa cualquier pantalla del flujo del programa y
de la que todas las clases de este programa la heredar�n
"""
class Pantalla:
    #Definimos el constructor, en este caso utilizamos un truco para
    #tener un constructor con par�metros opcionales. Le pasamos
    #un par�metro screen al que por defecto le ponemos None
    #as� por defecto ser� None pero si queremos pasar el par�metro
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
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)

    #Este m�todo lo usamos para iniciar la pantalla
    #Y la devolvemos
    def iniciarPantalla(self,width,height,titulo):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(titulo)
        return self.screen