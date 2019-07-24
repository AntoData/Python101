# coding: latin-1
'''
Created on 12 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pygame (1.9.6): para la interfaz gr�fica
Biblioteca est�ndar:
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
'''
import pygame
import sys
"""
Esta clase representa la ventana de error que mostraremos cuando haya
un error. No hereda de la clase Pantalla porque es una ventana que no
forma parte de los flujos del programa
"""
class PantallaError:
    #Definimos una variable que define el tama�o de la ventana
    TAMA�O_VENTANA_ERROR = (500,150)
    #Definimos una variable que define el color del fondo de la ventana
    COLOR_FONDO = (175,175,175)
    #Definimos una variable que define el tipo de letra que tendr�
    #el texto que mostraremos por pantalla
    FUENTE_MENSAJE = 'Arial'
    #Definimos una variable que define el color
    #que tendr� el mensaje de error gen�rico
    COLOR_TEXTO_GENERICO = (0, 0, 0) 
    #Definimos una variable que define el color
    #que tendr� el mensaje de error espec�fico
    COLOR_TEXTO_ESPECIFICO = (255, 0, 0)
    #Definimos el constructor, que solo recibe el mensaje de error como
    #par�metro
    def __init__(self,mensaje):
        self.mensaje = mensaje
        
    #Este es el m�todo que controla el mostrar la pantalla de error
    def mostrarPantallaError(self):
        #En este caso tenemos un bucle infinito que solo romperemos 
        #al cerrar la ventana de error
        while True:
            #Escuchamos a los eventos del programa
            for evento in pygame.event.get ():
                #Solo responderemos al caso en el que cerremos la ventana
                if evento.type == pygame.QUIT:
                    sys.exit()
                #Si ocultamos esta pantalla, hacemos lo mismo
                #que si la cerr�ramos puesto que no tiene sentido
                #dejar la ventana minimizada siendo un mensaje de
                #error
                if not pygame.display.get_active():
                    sys.exit()
            #Definimos el objeto screen que representa la ventana con su 
            #tama�o
            screen = pygame.display.set_mode(self.TAMA�O_VENTANA_ERROR)
            #Le ponemos t�tulo a la ventana
            pygame.display.set_caption("A la carta m�s alta: Error")
            #Con fill, rellenamos el fondo de la pantalla con el color
            #que hemos descrito
            screen.fill(self.COLOR_FONDO)
            
            #Iniciamos las fuentes
            pygame.font.init()
            #Definimos la fuente que usar� el mensaje gen�rico de error
            #de la ventana
            fuenteError = pygame.font.SysFont(self.FUENTE_MENSAJE, 20)
        
            sizeGenericoError = fuenteError.size("Ha ocurrido el siguiente error y la ejecuci�n del")
            
            #Generamos la representaci�n del texto gen�rico en esta variable
            textoGenericoError = fuenteError.render("Ha ocurrido el siguiente error y la ejecuci�n del", False, self.COLOR_TEXTO_GENERICO)
            
            sizeGenericoError2 = fuenteError.size("programa termin�")
            
            #Generamos la representaci�n de la segunda parte del texto gen�rico en esta variable    
            textoGenericoError2 = fuenteError.render("programa termin�", False, self.COLOR_TEXTO_GENERICO)
            
            #Generamos la fuente que llevar� el mensaje espec�fico que recibimos
            #como par�metro en el constructor para cada error
            fuenteError2 = pygame.font.SysFont(self.FUENTE_MENSAJE, 15)
        
            sizeMensajeError = fuenteError2.size(self.mensaje)
            
            #Generamos el mensaje de error espec�fico  
            textoMensajeError = fuenteError2.render(self.mensaje, False, self.COLOR_TEXTO_ESPECIFICO)
            
            #Mostramos en la pantalla los 3 mensajes usando screen.blit
            screen.blit(textoGenericoError,(screen.get_width()/2-sizeGenericoError[0]/2,0))
            screen.blit(textoGenericoError2,(screen.get_width()/2-sizeGenericoError2[0]/2,sizeGenericoError[1]+10))
            screen.blit(textoMensajeError,(screen.get_width()/2-sizeMensajeError[0]/2,sizeGenericoError[1]+sizeGenericoError2[1]+30))
            #Actualizamos la pantalla
            pygame.display.flip()