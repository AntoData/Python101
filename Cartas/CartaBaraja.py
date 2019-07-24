# coding: latin-1
'''
Created on 3 may. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio Pérez Oviedo
Librerías extra:
- pygame (1.9.6): para la interfaz gráfica,en este caso para que nuestra clase herede de la
clase Sprites y así encapsular la imagen asociada a la carta en la clase
Biblioteca estándar:
- sys: para deterner la ejecución en caso de excepción con sys.exit()
y para obtener los datos de dónde se produce la excepción en el código
- os: para la gestión de ficheros (comprobar si existe, ver en qué fichero
se encuentra la ejecución cuando se produce una excepción...)
Módulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepción
'''
import sys
import pygame
from Cartas import Utiles as utiles
from Front.PantallaError import PantallaError
import os
"""
Esta clase representa a cada una de las cartas que componen la baraja
Como estas cartas tendrán asociada una representación gráfica (imagen)
hemos hecho que la clase herede de la clase Sprite de pygame (para
que así podemos unir la representación gráfica de la carta y su lógica)
"""
class Carta(pygame.sprite.Sprite):
    #Definimos el constructor para esta clase
    #Recibiremos el valor de la carta en numero y su palo
    def __init__(self,numero,palo):
        pygame.sprite.Sprite.__init__(self)
        #Igualamos los parámetros de entrada a los parámetros palo y número
        #propios de la clase
        #Además los definimos como no accesibles fuera
        #de la clase, en primer lugar como método didáctico
        #y en otro porque no nos interesa que se pueda modificar
        #el valor de una carta una vez creada
        self.__palo = palo
        self.__numero =numero
        try:
            #Aquí asignamos la imagen de la carta a cada carta
            #Para ello, usamos el método load del módulo image de pygame
            #al que hay que pasarle la ruta a la imagen
            #En utiles hemos definido una función a la que si le damos
            #el valor y el palo de la carta, nos devuelve la ruta
            #en la que tal imagen debería encontrarse
            self.image = pygame.image.load(utiles.convertir_Carta_A_Ruta(self.palo, self.numero)).convert_alpha()
        except FileNotFoundError as e:
            #Ante cualquier excepción, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepción: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos la excepción en caso de que el fichero no haya sido
            #encontrado y devolvemos la pantalla de error
            pantallaError = PantallaError(r"Error al buscar las imágenes de las cartas")
            pantallaError.mostrarPantallaError()
            sys.exit() 
        except Exception as e1:
            #Ante cualquier excepción, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepción: {0}".format(e1))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos cualquier otra excepción que pueda darse y devolvemos
            #la pantalla de error
            pantallaError = PantallaError(r"Error al buscar las imágenes de las cartas")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #En caso de que no haya habido errores, procedemos a
        #terminar con la definición de las cartas
        else:
            #Definimos el rectángulo en el cual se imprime la imagen
            self.rect = self.image.get_rect()
            self.rect.centery = 350
    
    #Definimos palo como propiedad de la clase CartaBaraja
    #Eso significa que como no vamos a definir el setter con
    #la anotación @palo.setter este parámetro no se podrá
    #acceder directamente desde fuera al estar definido como
    #__palo y sólo tener un método con la anotación @property
    #por lo que solo será de lectura
    @property
    def palo(self):
        return self.__palo
    
    #Definimos numero como propiedad de la clase CartaBaraja
    #Eso significa que como no vamos a definir el setter con
    #la anotación @numero.setter este parámetro no se podrá
    #acceder directamente desde fuera al estar definido como
    #__numero y sólo tener un método con la anotación @property
    #por lo que solo será de lectura    
    @property
    def numero(self):
        return self.__numero
    
    #Sobreescribimos el método __str__ para que los métodos que convierten
    #un objeto a string directamente o imprimen el objeto, lo impriman
    #con el formato que queremos
    def __str__(self, *args, **kwargs):
        return "{0} de {1}".format(self.numero,self.palo)
