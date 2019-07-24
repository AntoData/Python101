# coding: latin-1
'''
Created on 12 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio Pérez Oviedo
Librerías extra:
- pygame (1.9.6): para la interfaz gráfica
Biblioteca estándar:
- sys: para deterner la ejecución en caso de excepción con sys.exit()
y para obtener los datos de dónde se produce la excepción en el código
'''
import pygame
import sys
"""
Esta clase representa la ventana de error que mostraremos cuando haya
un error. No hereda de la clase Pantalla porque es una ventana que no
forma parte de los flujos del programa
"""
class PantallaError:
    #Definimos una variable que define el tamaño de la ventana
    TAMAÑO_VENTANA_ERROR = (500,150)
    #Definimos una variable que define el color del fondo de la ventana
    COLOR_FONDO = (175,175,175)
    #Definimos una variable que define el tipo de letra que tendrá
    #el texto que mostraremos por pantalla
    FUENTE_MENSAJE = 'Arial'
    #Definimos una variable que define el color
    #que tendrá el mensaje de error genérico
    COLOR_TEXTO_GENERICO = (0, 0, 0) 
    #Definimos una variable que define el color
    #que tendrá el mensaje de error específico
    COLOR_TEXTO_ESPECIFICO = (255, 0, 0)
    #Definimos el constructor, que solo recibe el mensaje de error como
    #parámetro
    def __init__(self,mensaje):
        self.mensaje = mensaje
        
    #Este es el método que controla el mostrar la pantalla de error
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
                #que si la cerráramos puesto que no tiene sentido
                #dejar la ventana minimizada siendo un mensaje de
                #error
                if not pygame.display.get_active():
                    sys.exit()
            #Definimos el objeto screen que representa la ventana con su 
            #tamaño
            screen = pygame.display.set_mode(self.TAMAÑO_VENTANA_ERROR)
            #Le ponemos título a la ventana
            pygame.display.set_caption("A la carta más alta: Error")
            #Con fill, rellenamos el fondo de la pantalla con el color
            #que hemos descrito
            screen.fill(self.COLOR_FONDO)
            
            #Iniciamos las fuentes
            pygame.font.init()
            #Definimos la fuente que usará el mensaje genérico de error
            #de la ventana
            fuenteError = pygame.font.SysFont(self.FUENTE_MENSAJE, 20)
        
            sizeGenericoError = fuenteError.size("Ha ocurrido el siguiente error y la ejecución del")
            
            #Generamos la representación del texto genérico en esta variable
            textoGenericoError = fuenteError.render("Ha ocurrido el siguiente error y la ejecución del", False, self.COLOR_TEXTO_GENERICO)
            
            sizeGenericoError2 = fuenteError.size("programa terminó")
            
            #Generamos la representación de la segunda parte del texto genérico en esta variable    
            textoGenericoError2 = fuenteError.render("programa terminó", False, self.COLOR_TEXTO_GENERICO)
            
            #Generamos la fuente que llevará el mensaje específico que recibimos
            #como parámetro en el constructor para cada error
            fuenteError2 = pygame.font.SysFont(self.FUENTE_MENSAJE, 15)
        
            sizeMensajeError = fuenteError2.size(self.mensaje)
            
            #Generamos el mensaje de error específico  
            textoMensajeError = fuenteError2.render(self.mensaje, False, self.COLOR_TEXTO_ESPECIFICO)
            
            #Mostramos en la pantalla los 3 mensajes usando screen.blit
            screen.blit(textoGenericoError,(screen.get_width()/2-sizeGenericoError[0]/2,0))
            screen.blit(textoGenericoError2,(screen.get_width()/2-sizeGenericoError2[0]/2,sizeGenericoError[1]+10))
            screen.blit(textoMensajeError,(screen.get_width()/2-sizeMensajeError[0]/2,sizeGenericoError[1]+sizeGenericoError2[1]+30))
            #Actualizamos la pantalla
            pygame.display.flip()