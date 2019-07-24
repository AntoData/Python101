# coding: latin-1
'''
Created on 3 may. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pygame (1.9.6): para la interfaz gr�fica,en este caso para que nuestra clase herede de la
clase Sprites y as� encapsular la imagen asociada a la carta en la clase
Biblioteca est�ndar:
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
- os: para la gesti�n de ficheros (comprobar si existe, ver en qu� fichero
se encuentra la ejecuci�n cuando se produce una excepci�n...)
M�dulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepci�n
'''
import sys
import pygame
from Cartas import Utiles as utiles
from Front.PantallaError import PantallaError
import os
"""
Esta clase representa a cada una de las cartas que componen la baraja
Como estas cartas tendr�n asociada una representaci�n gr�fica (imagen)
hemos hecho que la clase herede de la clase Sprite de pygame (para
que as� podemos unir la representaci�n gr�fica de la carta y su l�gica)
"""
class Carta(pygame.sprite.Sprite):
    #Definimos el constructor para esta clase
    #Recibiremos el valor de la carta en numero y su palo
    def __init__(self,numero,palo):
        pygame.sprite.Sprite.__init__(self)
        #Igualamos los par�metros de entrada a los par�metros palo y n�mero
        #propios de la clase
        #Adem�s los definimos como no accesibles fuera
        #de la clase, en primer lugar como m�todo did�ctico
        #y en otro porque no nos interesa que se pueda modificar
        #el valor de una carta una vez creada
        self.__palo = palo
        self.__numero =numero
        try:
            #Aqu� asignamos la imagen de la carta a cada carta
            #Para ello, usamos el m�todo load del m�dulo image de pygame
            #al que hay que pasarle la ruta a la imagen
            #En utiles hemos definido una funci�n a la que si le damos
            #el valor y el palo de la carta, nos devuelve la ruta
            #en la que tal imagen deber�a encontrarse
            self.image = pygame.image.load(utiles.convertir_Carta_A_Ruta(self.palo, self.numero)).convert_alpha()
        except FileNotFoundError as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos la excepci�n en caso de que el fichero no haya sido
            #encontrado y devolvemos la pantalla de error
            pantallaError = PantallaError(r"Error al buscar las im�genes de las cartas")
            pantallaError.mostrarPantallaError()
            sys.exit() 
        except Exception as e1:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos cualquier otra excepci�n que pueda darse y devolvemos
            #la pantalla de error
            pantallaError = PantallaError(r"Error al buscar las im�genes de las cartas")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #En caso de que no haya habido errores, procedemos a
        #terminar con la definici�n de las cartas
        else:
            #Definimos el rect�ngulo en el cual se imprime la imagen
            self.rect = self.image.get_rect()
            self.rect.centery = 350
    
    #Definimos palo como propiedad de la clase CartaBaraja
    #Eso significa que como no vamos a definir el setter con
    #la anotaci�n @palo.setter este par�metro no se podr�
    #acceder directamente desde fuera al estar definido como
    #__palo y s�lo tener un m�todo con la anotaci�n @property
    #por lo que solo ser� de lectura
    @property
    def palo(self):
        return self.__palo
    
    #Definimos numero como propiedad de la clase CartaBaraja
    #Eso significa que como no vamos a definir el setter con
    #la anotaci�n @numero.setter este par�metro no se podr�
    #acceder directamente desde fuera al estar definido como
    #__numero y s�lo tener un m�todo con la anotaci�n @property
    #por lo que solo ser� de lectura    
    @property
    def numero(self):
        return self.__numero
    
    #Sobreescribimos el m�todo __str__ para que los m�todos que convierten
    #un objeto a string directamente o imprimen el objeto, lo impriman
    #con el formato que queremos
    def __str__(self, *args, **kwargs):
        return "{0} de {1}".format(self.numero,self.palo)
