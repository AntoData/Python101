# coding: latin-1
'''
Created on 11 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pygame (1.9.6): para la interfaz gr�fica
Biblioteca est�ndar
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
- os: para la gesti�n de ficheros (comprobar si existe, ver en qu� fichero
se encuentra la ejecuci�n cuando se produce una excepci�n...)
- time: Para pausar el hilo de ejecuci�n
M�dulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepci�n
- Pantalla: que es una clase padre que controla la configuraci�n de la ventana/pantalla del juego
- FicheroBaraja: M�dulo que encapsula todos los m�todos para gestionar el fichero baraja.txt
(abrirlo, realizar una copia del mismo y borrar la instancia principal si pasa de un determinado
tama�o, escribir en �l...)
- Utiles: m�dulo con diversos m�todos para gestionar correctamente aspectos de la baraja y las cartas
(por ejemplo la conversi�n del "n�mero" de la carta en string al valor integer basado en su posici�n
en el palo) 
'''
import pygame
from Front.Pantalla import Pantalla
from Front.PantallaError import PantallaError
from Back import FicheroBaraja as FicheroBaraja
from Cartas import Utiles as Utiles
import sys
import os
import time
"""
Esta clase representa la pantalla que mostrar� los resultados
finales de la partida. Como forma parte del flujo del programa
heredar� de la clase Pantalla
"""
class ResultadoPartida(Pantalla):
    #Definimos una variable que contendr� la fuente que usaremos
    FUENTE_TEXTO = 'Arial'
    #Definimos una variable que contendr� el tama�o del texto
    TAMA�O_TEXTO = 50
    #Definimos una variable de clase que definir� el color del texto
    COLOR_TEXTO = (0,0,0)
    #Definimos un constructor que recibir� un objeto
    #que representa la pantalla, y al ganador
    #con valor predeterminado None para poder usarlo sin
    #par�metros en el caso en que sea necesario
    def __init__(self,screen = None, ganador = None):
        Pantalla.__init__(self, screen)
        self.ganador = ganador
    #Este m�todo es el controlador que muestra la pantalla
    #de resultado    
    def PantallaResultado(self,resultado):
        #Definimos la variable background que representar� el
        #fondo de la pantalla
        background = None
        try:
            #Dentro de este try, cargamos la imagen para el fondo
            #de esta pantalla usando el m�todo load del m�dulo image
            background = pygame.image.load(Utiles.RUTA_FONDO_MESA_JUEGO).convert()
        except FileNotFoundError as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos la posible excepc��n que generar� el caso
            #en que no podramos encontrar la imagen
            #En tal caso mostramos la pantalla de error
            pantallaError = PantallaError(r"Falta el fichero {0}".format(Utiles.RUTA_FONDO_MESA_JUEGO))
            pantallaError.mostrarPantallaError()
            sys.exit()
        except Exception as e1:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos cualquier otra posible excepci�n
            pantallaError = PantallaError(r"Ocurri� un error en la pantalla de resultado")
            pantallaError.mostrarPantallaError()
            sys.exit()    
        
        #Definimos el rect�ngulo donde impriremos la imagen
        #del fondo
        background_rect = background.get_rect()
        #Mostramos el fondo por pantalla usando screen.bilt
        self.screen.blit(background,background_rect)
        i = 0
        #Generamos otra estructura try and except para atrapar
        #otros posible errores
        try:
            #Iniciamos las fuentes de pygame
            pygame.font.init()
            
            #Definimos la fuente del texto
            fuenteMensaje = pygame.font.SysFont(self.FUENTE_TEXTO, self.TAMA�O_TEXTO)
        
            sizeTextoMensaje = fuenteMensaje.size("Jugador {0}:{1} Ordenador".format(resultado["jugador"],resultado["ordenador"]))
            
            #Generamos el texto con la fuente
            textoMensaje = fuenteMensaje.render("Jugador {0}:{1} Ordenador".format(resultado["jugador"],resultado["ordenador"]), False, self.COLOR_TEXTO)
        
            mensaje = ""
            ganador = ""
            #En la variable mensaje incluiremos un mensaje un otro
            #en funci�n de quien haya ganado o si ha habido empate
            if resultado["jugador"]>resultado["ordenador"]:
                mensaje = "Has ganado la partida"
                ganador = "J"
            elif resultado["jugador"]<resultado["ordenador"]:
                mensaje = "Has perdido la partida"
                ganador="O"
            else:
                mensaje = "Hab�is empatado"
                ganador = "E"
                
            sizeTextoMensaje2 = fuenteMensaje.size(mensaje)
            #Generamos el texto del mensaje diciendo quien ha ganado    
            textoMensaje2 = fuenteMensaje.render(mensaje, False, self.COLOR_TEXTO)
            
            #Imprimimos en pantalla los mensajes usando screen.blit
            self.screen.blit(textoMensaje,(self.screen.get_width()/2-sizeTextoMensaje[0]/2,self.screen.get_height()/2-sizeTextoMensaje[1]))
            self.screen.blit(textoMensaje2,(self.screen.get_width()/2-sizeTextoMensaje2[0]/2,self.screen.get_height()/2+sizeTextoMensaje2[1]))
            
            #Actualizamos la pantalla
            pygame.display.flip()
            #Esperamos algo 5 segundos antes de terminar con esta pantalla
            while i<500:
                i+=1
                #Escuchamos los eventos del teclado y el rat�n
                for evento in pygame.event.get ():
                    #Solo respondemos al cierre de la ventana terminado la ejecuci�n
                    if evento.type == pygame.QUIT:
                        sys.exit()
                #Paramos el hilo 0.01 segundos para que
                #tras 500 iteraciones hayamos esperado aproximadamente
                #5 segs      
                time.sleep(0.01)
            #Actualizamos el fichero que controla el estado de la baraja para decir que se termin�o la partida (y ya de paso a�adimos qui�n gan�)
            FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,mensaje+"\r\n","Partida finalizada\r\n","--------------\r\n")   
            #Construimos el registro con la informaci�n del fin de esta ronda para que se pueda escribir en el fichero csv
            datarow= {"T":"P","G":ganador,"CPJ":resultado["jugador"],"CPO":resultado["ordenador"]}
            #Lo devolvemos para que as� se pueda a�adir al csv y as� contribuir a las estad�sticas
            return datarow
        except Exception:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos cualquier error y mostramos la pantalla de error
            pantallaError = PantallaError(r"Error al buscar los resultados")
            pantallaError.mostrarPantallaError()
            sys.exit() 
