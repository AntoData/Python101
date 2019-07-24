# coding: latin-1
'''
Created on 3 may. 2019
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
- Baraja: Clase que encapsula todos los m�todos para gestionar la baraja
- Utiles: m�dulo con diversos m�todos para gestionar correctamente aspectos de la baraja y las cartas
(por ejemplo la conversi�n del "n�mero" de la carta en string al valor integer basado en su posici�n
en el palo) 
'''
import pygame
import Cartas.Baraja as Baraja
import sys
import os
from Front.Pantalla import Pantalla
import time
from Front.PantallaError import PantallaError
from Cartas import Utiles as Utiles

"""
Esta clase representa a la mesa de juego que es donde se hacen
todas las operaciones sobre la baraja: barajar, cortar la baraja,
extraer las cartas del mazo y el marcador por ronda. Al formar
parte del flujo del programa, hereda de la clase Pantalla
"""
class MesaJuego(Pantalla):
    #Definimos una variable que define la fuente de algunos textos
    TIPO_FUENTE_1 = 'Arial'
    #Definimos una variable que contendr� el color del fondo del pop-up
    FONDO_POP_UP = (19,102,0) 
    #Definimos un constructor que recibe una variable screen
    #que representa la pantalla y una variable que contendr�
    #el marcador con valor predeterminado None para as�
    #no tener que usarlos en el constructor
    def __init__(self,screen = None, marcador = None):
        #Llamamos al constructor de la clase padre
        Pantalla.__init__(self, screen)
        #Si no hemos pasado marcador lo iniciamos 0 a 0
        if marcador == None:
            self.marcador = {"jugador":0,"ordenador":0}
        else:
            #En caso contrario lo pasamos a la clase
            self.marcador = marcador
        #Inicializamos este objeto datacsv a lista vac�a
        #Aqu� guardaremos cada registro de una partida
        #que ser�n guardados en el fichero csv a trav�s
        #del cual generamos las estad�sticas
        self.datacsv = []
        
    #Esta funci�n prepara los sprites que ser�n mostrados
    #por pantalla cada vez que saquemos una carta
    def prepararSpriteCarta(self):
        #Creamos un grupo de sprites
        sprite_cartas = pygame.sprite.Group()
        #Extraemos la carta de la baraja
        carta_pantalla = self.baraja.seleccionarCartaSuperior()
        #   Se a�ade al grupo de sprites
        sprite_cartas.add(carta_pantalla)
        # Devolvemos el grupo de sprites
        return sprite_cartas
    #Con motivo did�ctico hemos creado este decorador que puede
    #adem�s muy �til. Este decorador generar� una baraja
    #nueva y la asignar� al par�emtro baraja de esta clase
    #antes de ejecutar el m�todo que "decora" (modifica)
    #lo usaremos con el m�todo escrito a continuaci�n
    #que genera y gestiona la pantalla inicial de la mesa de juego
    def iniciadorBarajaEnvolturaDecorador(self):
        def inciadorBarajaEnvoltura(func):
            def inciadorBarajaDecorador(self):
                self.baraja = Baraja.Baraja()
                func(self)
            return inciadorBarajaDecorador
        return inciadorBarajaEnvoltura
    
    
    #Este m�todo es el que mostrar� el mensaje inicial de la mesa
    #de juego Tengo una baraja, vamos a jugar.
    #Usamos el decorador que hemos definido previamente para que as�
    #la baraja sea creada antes de la ejecuci�n de este m�todo
    #para que as� lo tenga disponible
    @iniciadorBarajaEnvolturaDecorador("self")
    def mensajeInicial(self):
        #Gracias al decorador ya generemos la baraja nueva 
        #para la partida nueva
        i = 0
        #Generamos un bucle que mostrar� durante 5 segundos el mensaje
        #de bienvenida a la partida
        while i<5:
            #Escuchamos los eventos eventos del teclado y rat�n
            for evento in pygame.event.get ():
                #Solo responderemos al cierre de la ventana
                #terminando la ejecuci�n
                if evento.type == pygame.QUIT:
                    sys.exit()
            #Definimos una variable background que contendr� la 
            #imagen que usaremos para el fondo
            background = None
            try:
                #Cargamos la imagen del fondo usando el m�todo
                #load del m�dulo image
                background = pygame.image.load(Utiles.RUTA_FONDO_MESA_JUEGO).convert()
            except FileNotFoundError as e:
                #Ante cualquier excepci�n, primero imprimimos por 
                #consola un log del error
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
                print(exc_type, fname, exc_tb.tb_lineno)
                #Recogemos la excepci�n que se generar� en caso
                # de no encontrar el fichero y mostraremos la
                #pantalla de error
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
                #Recogemos cualquier excepci�n que se pueda
                #generar y mostramos la pantalla de error
                pantallaError = PantallaError(r"Ocurri� un problema con la mesa de juego")
                pantallaError.mostrarPantallaError()
                sys.exit()                
            
            #Definimos el rect�ngulo donde imprimiremos la imagen
            background_rect = background.get_rect()
            #Imprimimos la imagen del fondo sobre la pantalla
            #con screen.blit
            self.screen.blit(background,background_rect)
            
            #Iniciamos las fuentes de pygame
            pygame.font.init()
            
            #Definimos la fuente del mensaje
            fuenteJugador = pygame.font.SysFont(self.TIPO_FUENTE_1, 50)
        
            sizeTextoJugador = fuenteJugador.size("Tengo una baraja.")
            #Generamos el texto del mensaje
            textoJugador = fuenteJugador.render('Tengo una baraja.', False, (0, 0, 0))
            
            #Generamos el texto para el segundo mensaje        
            sizeTextoJugador2 = fuenteJugador.size("Vamos a jugar.")
                
            textoJugador2 = fuenteJugador.render('Vamos a jugar.', False, (0, 0, 0))
            
            #Imprimimos ambos mensajes en la pantalla con screen.blit
            self.screen.blit(textoJugador,(self.screen.get_width()/2-sizeTextoJugador[0]/2,self.screen.get_height()/2-sizeTextoJugador[1]))
            
            self.screen.blit(textoJugador2,(self.screen.get_width()/2-sizeTextoJugador2[0]/2,self.screen.get_height()/2+sizeTextoJugador2[1]))
            #Actualizamos la pantalla
            pygame.display.flip()
            #Esperamos 0.1 segs
            time.sleep(0.1)
            #Avanzamos el bucle
            i += 1
    #Este m�todo controla la pantalla en la que imprimimos el
    #gif con la animaci�n de la baraja
    def animacionBarajar(self):
        #Lo primero ser� barajar la baraja de verdad para dejarla
        #en el estado tras barajar
        self.baraja.barajar()
        k = 0
        #Generamos un bucle donde iremos de k = 0 a k =47
        #donde k ser� el �ndice que la imagen que mostrar en
        #cada iteraci�n
        while k<48:
            #Escuchamos a los eventos del teclado y rat�n
            for evento in pygame.event.get ():
                #Solo respondemos al cierre de la ventana, 
                #finalizando la ejecuci�n
                if evento.type == pygame.QUIT:
                    sys.exit()
                    
            #Como las im�genes se numeran como 01 a 09 y 10 a 47
            #tenemos que preparar la variable que contendr� el �ndice
            #para el nombre del fichero
            r = ""
            if(k<10):
                r = "0{0}".format(k)
            else:
                r = "{0}".format(k)
            
            #Definimos las variables para el fondo y para la imagen
            #de la animaci�n que habr� que mostrar en esta iteraci�n
            barajarGIF = None
            background = None
            
            try:
                #Cargamos la imagen de la animaci�n a mostrar en esta iteraci�n
                barajarGIF = pygame.image.load(Utiles.RUTA_IMAGENES_ANIMACION_BARAJAR.format(r)).convert()
            except FileNotFoundError as e:
                #Ante cualquier excepci�n, primero imprimimos por 
                #consola un log del error
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
                print(exc_type, fname, exc_tb.tb_lineno)
                #Como siempre capturamos el error de fichero no encontrado
                #y mostramos la pantalla de error
                pantallaError = PantallaError(r"Falta el fichero "+Utiles.RUTA_IMAGENES_ANIMACION_BARAJAR.format(r))
                pantallaError.mostrarPantallaError()
                sys.exit()
            except Exception as e1:
                #Ante cualquier excepci�n, primero imprimimos por 
                #consola un log del error
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
                print(exc_type, fname, exc_tb.tb_lineno)
                #Como siempre capturamos cualquier excepci�n que se genere
                #y mostramos la pantalla de error
                pantallaError = PantallaError("Ocurri� un problema con la animaci�n de barajar")
                pantallaError.mostrarPantallaError()
                sys.exit()
            
            try:
                #Ahora cargamos la imagen del fondo
                background = pygame.image.load(Utiles.RUTA_FONDO_MESA_JUEGO).convert()
            except FileNotFoundError as e:
                #Ante cualquier excepci�n, primero imprimimos por 
                #consola un log del error
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
                print(exc_type, fname, exc_tb.tb_lineno)
                #Capturamos la excepci�n de fichero no encontrado
                #y mostramos la pantalla de error
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
                #Capturamos cualquier otra excepci�n y mostramos
                #la pantalla de error
                pantallaError = PantallaError(r"Ocurri� un error en la mesa de juego")
                pantallaError.mostrarPantallaError()
                sys.exit()
        
            #Definimos el rect�ngulo en que impriremos la imagen del fondo
            background_rect = background.get_rect()
            #Mostramos la imagen del fondo en la pantalla usando screen.blit
            self.screen.blit(background,background_rect)
            
            #Usando screen.blit mostramos la imagen que mostrar en esta iteraci�n
            #de la animaci�n de barajar
            self.screen.blit(barajarGIF, (self.screen.get_width()/2-barajarGIF.get_rect()[2]/2,self.screen.get_height()/2 - barajarGIF.get_rect()[3]/2))
            
            #Definimos la fuente que usaremos para imprimr un texto
            fuenteTextoBarajando = pygame.font.SysFont(self.TIPO_FUENTE_1, 40)
        
            sizeTextoBarajando = fuenteTextoBarajando.size("Barajando")
            #Generamos el texto
            textBarajando = fuenteTextoBarajando.render("Barajando", 1, (0, 0, 0))
            textRectBarajando = textBarajando.get_rect()
            textRectBarajando.top = self.screen.get_height()/2 - barajarGIF.get_rect()[3]/2 - 10 - sizeTextoBarajando[1]
            textRectBarajando.left = self.screen.get_width()/2 - sizeTextoBarajando[0]/2
            #Imprimimos el texto por pantalla
            self.screen.blit(textBarajando, (textRectBarajando.left,textRectBarajando.top))
            #Actualizamos la pantalla
            pygame.display.flip()
            #Avanzamos el bucle
            k+=1
            #Esperamos un poco antes de avanzar
            time.sleep(0.005)
    
    #Este m�todo controlar� la pantalla donde le pedimos
    #al usuario que introduzca un n�mero para cortar la baraja
    def popupCortarBaraja(self):
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        #Cargamos la imagen para el fondo de la pantalla
        background = None
        try:
            background = pygame.image.load(Utiles.RUTA_FONDO_MESA_JUEGO).convert()
        #Recogemos cualquier posible excepci�n y mostramos la pantalla de error
        except FileNotFoundError as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
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
            pantallaError = PantallaError(r"Ocurri� un error en la mesa de juego")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Definimos el rect�ngulo donde imprimiremos la imagen del fondo
        background_rect = background.get_rect()
        #Definimos la caja para el input para el usuario
        input_box = pygame.Rect(self.screen.get_width()/2-17.5, self.screen.get_height()/2+15, 35, 32)
        #Definimos los colores que tendr�, azul claro para cuando est� inactivo
        #y azul m�s oscuro apra cuando est� inactivo
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        #Por defecto tal input estar� activo
        color = color_active
        active = True
        #Esta ser� la variable que contendr� y mostrar� el texto
        #que el usuario introducir� por defecto
        text = ''
        #Definimos esta variable que controla el bucle que usaremos
        #para mostrar la pantalla, hasta que el usuario no realice
        #la acci�n que cambiar� esta variable booleana a True, no 
        #se terminar� el bucle (not True = False)
        done = False
        while not done:
            #Escuchamos todos los eventos del teclado y raton
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si el usuario hace click en el input
                    if input_box.collidepoint(event.pos):
                    # El input cambiar� a activo
                        active = not active
                    else:
                    #Si ha pulsado en otra parte, pasar� a inactivo
                        active = False
                    # Esta sentencia coordina el color del input con su estado
                    color = color_active if active else color_inactive
                #Escuchamos si el usuario pulsa una tecla
                if event.type == pygame.KEYDOWN:
                    if active:
                        #Si el input est� activo
                        #Si el usuario pulsa ENTER
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            try:
                                if text == "":
                                    #Si no introdujo texto, no hacemos nada. Adem�s es una manera
                                    #de exponer de manera did�ctica qu� hace la sentencia pass
                                    pass
                                #Si el texto que ha introducido por el teclado corresponde
                                #a un n�mero que es mayor que la longitud de la baraja
                                elif int(text)>len(self.baraja.cartas):
                                    #Simplemente sustituimos la cadena por la longitud de la baraja
                                    text = "{0}".format(len(self.baraja.cartas))
                                elif int(text) == 0:
                                    #Si el usuario introdujo 0, lo cambiamos por 1
                                    text = "1"
                                else:
                                    #En caso de que no haya que cambiar el input del usuario
                                    #significa que validamos ese entero y terminamos
                                    #la ejecuci�n de este bucle, para eso cambiamos Done a True
                                    #y ello provocar� avanzar en el flujo
                                    done = True
                            except ValueError as e:
                                #Ante cualquier excepci�n, primero imprimimos por 
                                #consola un log del error
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
                                print(exc_type, fname, exc_tb.tb_lineno)
                                pantallaError = PantallaError(r"Has introducido un valor inv�lido")
                                pantallaError.mostrarPantallaError()
                                sys.exit()
                            except Exception as e1:
                                #Ante cualquier excepci�n, primero imprimimos por 
                                #consola un log del error
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
                                print(exc_type, fname, exc_tb.tb_lineno)
                                pantallaError = PantallaError(r"Ha ocurrido un error al procesar tu valor")
                                pantallaError.mostrarPantallaError()
                                sys.exit()
                        #As� borramos un caracter del input cuando el usario pulsa borrar
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            #Cada vez que a�ada un d�gito lo a�adimos al texto que mostrar
                            #aunque ponemos dos d�gitos como l�mite en el input
                            #no escucharemos si el usuario quiere meter un tercero
                            if(len(text)<2):
                                newText = ''.join(i for i in event.unicode if i.isdigit())
                                text += newText
                #Tambi�n escuchamos al cierre de la ventana
                if event.type == pygame.QUIT:
                    sys.exit()
                
            #Imprimimos en pantalla el fondo con screen.blit
            self.screen.blit(background,background_rect)
            #Generamos el texto del input
            txt_surface = font.render(text, True, color)
            rect = txt_surface.get_rect()
            #Generamos la fuente que llevar�n los textos del pop-up
            fuenteTextoPopUp = pygame.font.SysFont(self.TIPO_FUENTE_1, 22)
            #Definimos una superficie que ser� sobre la que
            #imprimiremos el pop-up
            popupSurf = pygame.Surface((400, 150))
            #Le damos color y lo colocamos en su posici�n
            popupSurf.fill(self.FONDO_POP_UP)
            popupRect = popupSurf.get_rect()
            popupRect.centerx = self.screen.get_width()/2
            popupRect.centery = self.screen.get_height()/2
            rect.bottom = popupRect.bottom
            rect.left = self.screen.get_width()/2-rect.width/2
            #Imprimimos el texto del input del usuario en la superficie
            popupSurf.blit(txt_surface, rect)
            #Generamos los textos del mensaje para el usuario y los
            # colocamos en la superficie y los mostramos
            sizeTextoPopUp = fuenteTextoPopUp.size("Te toca cortar la baraja")
            textSurf = fuenteTextoPopUp.render("Te toca cortar la baraja", 1, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.top = popupSurf.get_height()/2 - sizeTextoPopUp[1]*2
            textRect.left = popupSurf.get_width()/2 - sizeTextoPopUp[0]/2
            popupSurf.blit(textSurf, (textRect.left,textRect.top))
            sizeTextoPopUp2 = fuenteTextoPopUp.size("ELije un n�mero del 1 al {0} y pulsa Intro".format(len(self.baraja.cartas)))
            textSurf2 = fuenteTextoPopUp.render("Elije un n�mero del 1 al {0} y pulsa Intro".format(len(self.baraja.cartas)), 1, (0, 0, 0))
            textRect2 = textSurf2.get_rect()
            textRect2.top = popupSurf.get_height()/2 - sizeTextoPopUp2[1]
            textRect2.left = popupSurf.get_width()/2 - sizeTextoPopUp2[0]/2
            popupSurf.blit(textSurf2, (textRect2.left,textRect2.top))
            
            #Imprimimos la superficie que creamos para el pop-up
            #en la pantalla
            self.screen.blit(popupSurf, popupRect)
            
            #Imprimimos el input de usuario en la pantalla
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Dibujamos el rect�ngulo del input
            pygame.draw.rect(self.screen, color, input_box, 2)
            #Actualizamos la pantalla
            pygame.display.flip()
            clock.tick(30)
        #Ahora traducimos el valor introducido por el usuario a int
        n = 0
        try:
            n = int(text)
        except ValueError as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Si no es un valor entero v�lido mostramos la pantalla de error
            pantallaError = PantallaError("El valor introducido debe estar en el rango [0,{0}]".format(len(self.baraja.cartas)))
            pantallaError.mostrarPantallaError()
            sys.exit()
        except Exception as e1:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Mostramos la pantalla de error para cualquier otra posible excepci�n
            pantallaError = PantallaError("Ocurri� un error al cortar la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Cortamos la baraja
        self.baraja.cortarBaraja(n)
        
    #Este m�todo encapsula las acciones necesarias para la primera ronda
    def prepararCartasPrimeraRonda(self):
        #Mostramos el mensaje incial
        self.mensajeInicial()
        #Mostramos la animaci�n de baraja y la generamos
        self.animacionBarajar()
        #Mostramos el pop-up para la primera ronda
        self.popupCortarBaraja()
    
    #Este m�todo controla la animaci�n del papete donde
    #sacamos la carta del jugador y la del ordenador
    # en cada ronda
    def animacionPapete(self):
        #Preparamos los sprites de las cartas y los recuperamos
        self.sprite_jugador = self.prepararSpriteCarta()
        self.cartasjugador = self.sprite_jugador.sprites()
        self.sprite_ordenador = self.prepararSpriteCarta()
        self.cartasordenador = self.sprite_ordenador.sprites()
        #Como ya tenemos las cartas usamos este m�todo para calcular
        #el resultado de la ronda
        self.calcularResultado()
        background = None
        try:
            #Cargamos la imagen para el fondo del tapete
            background = pygame.image.load(Utiles.RUTA_TAPETE).convert()
        except FileNotFoundError as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Capturamos la excepci�n que se generar�a en caso
            #de no encontrar el fichero y mostramos lap pantalla de error
            pantallaError = PantallaError(r"El fichero {0} no existe".format(Utiles.RUTA_TAPETE))
            pantallaError.mostrarPantallaError()
            sys.exit()
        except Exception as e1:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Capturamos cualquier excepci�n y mostramos la pantalla de error
            pantallaError = PantallaError(r"Ocurri� un error en la mesa de juego")
            pantallaError.mostrarPantallaError()
            sys.exit()
        i = 0
        #Hasta que las cartas no est�n en el centro seguiremos
        #usando un bucle que las anima
        #Este par�metro boolean es el que cambiar� a true cuando
        #las cartas lleguen al centro y por tanto se acabe la ronda
        finRonda = False
        while not finRonda:
            #Escuchamos los eventos del teclado y el rat�n
            for evento in pygame.event.get ():
                #Solo respondemos al cierre de la ventana terminado la ejecuci�n
                if evento.type == pygame.QUIT:
                    sys.exit()
            #Recuperamos la carta del jugador
            cartajugador = self.cartasjugador[0]
            #Recuperamos la carta del ordenador
            cartaordenador = self.cartasordenador[0]
            #En cada iteraci�n movemos la carta del jugador 
            #de izquierda a derecha hasta el centro
            cartajugador.rect.left = i - (cartajugador.image.get_rect().width/2)
            cartajugador.rect.top = (self.screen.get_height()/2) - cartajugador.image.get_rect().height
            #En cada iteraci�n movemos la carta del ordenador
            #de derecha a izquierda hasta el centro
            cartaordenador.rect.left = self.screen.get_width() - i - (cartaordenador.image.get_rect().width/2)
            cartaordenador.rect.top = (self.screen.get_height()/2) + 50
            
            #Mostramos la imagen del fondo del tapete
            background_rect = background.get_rect()
            self.screen.blit(background,background_rect)
            
            #Iniciamos las fuentes
            pygame.font.init()
            
            #Generamos un texto que dice Carta Jugador
            fuenteCartas = pygame.font.SysFont(self.TIPO_FUENTE_1, 20)
            sizeTextoJugador = fuenteCartas.size("Carta Jugador")
            textoJugador = fuenteCartas.render('Carta Jugador', False, (0, 0, 0))
            #Lo vamos mostrando en cada iteraci�n de manera que se mueva junto con su carta
            self.screen.blit(textoJugador,(i - (sizeTextoJugador[0]/2),170))
            #Generamos un texto que dice Carta Ordenador
            sizeTextoOrdenador = fuenteCartas.size("Carta Ordenador")
            textoOrdenador = fuenteCartas.render('Carta Ordenador', False, (0, 0, 0))
            #Lo vamos mostrando en cada iteraci�n de manera que sigue a la carta
            self.screen.blit(textoOrdenador,(self.screen.get_width()-i-(sizeTextoOrdenador[0]/2),self.screen.get_height()-140))
            
            #Dibujamos la carta
            self.sprite_jugador.draw(self.screen)
            #Dibujamos la carta
            self.sprite_ordenador.draw(self.screen)
            #Mostramos los marcadores
            self.rotuloMarcador()
            
            #Si todav�a no hemos llegado a la mitad avanzamos
            if(i<(self.screen.get_width())/2):
                i+=1
            else:
                #En caso de llegar a la mitad mostramos el resultado
                #de la ronda usando actualizarConResultado
                ganador = self.actualizarConResultado(cartajugador, cartaordenador)
                #Es el final de la ronda, esto romper� el bucle
                finRonda = True
                #Como ha terminado la ronda, introducimos en la lista
                #de registros que recibir� el csv
                datarow = {"T":"R","G":ganador,"CPJ":"{0}".format(cartajugador),"CPO":"{0}".format(cartaordenador)}
                self.datacsv.append(datarow)
            #Actualizamos la pantalla
            pygame.display.flip()
        #Devolvemos el marcador
        return self.marcador
    #Este m�todo realiza todas las acciones necesarias para
    #mostrar tanto el marcador del usuario como el del ordenador        
    def rotuloMarcador(self):
        self.rotuloMarcadorJugador()
        self.rotuloMarcadorOrdenador()
    #Este m�todo controla el marcador del jugador 
    def rotuloMarcadorJugador(self):
        #Generamos la fuente que llevar� el texto
        fuenteMarcador = pygame.font.SysFont(self.TIPO_FUENTE_1, 50)
        sizeCabeceraMarcadorJugador = fuenteMarcador.size("Jugador")
        sizeMarcadorJugador = fuenteMarcador.size("{0}".format(self.marcador["jugador"]))
        #Generamos los textos que llevar� el marcador
        textoCabeceraJugador = fuenteMarcador.render("Jugador", False, (255, 161, 0))
        textoMarcadorJugador = fuenteMarcador.render("{0}".format(self.marcador["jugador"]), False, (255, 161, 0))
        #Mostramos los textos en el rinc�n para su marcador
        self.screen.blit(textoCabeceraJugador,(20,20))
        self.screen.blit(textoMarcadorJugador,(sizeCabeceraMarcadorJugador[0]/2,30+sizeCabeceraMarcadorJugador[1]))
    
    
    #Este m�todo controla el marcador del ordenador
    def rotuloMarcadorOrdenador(self):
        #Generamos la fuente que llevar� el texto
        fuenteMarcador = pygame.font.SysFont(self.TIPO_FUENTE_1, 50)
        sizeCabeceraMarcadorOrdenador = fuenteMarcador.size("Ordenador")
        sizeMarcadorOrdenador = fuenteMarcador.size("{0}".format(self.marcador["ordenador"]))
        #Generamos los textos que llevar� el marcador
        textoCabeceraOrdenador = fuenteMarcador.render("Ordenador", False, (255, 161, 0))
        textoMarcadorOrdenador = fuenteMarcador.render("{0}".format(self.marcador["ordenador"]), False, (255, 161, 0))
        #Mostramos los textos en el rinc�n para su marcador
        self.screen.blit(textoCabeceraOrdenador,(self.screen.get_width()-sizeCabeceraMarcadorOrdenador[0]-20,20))
        self.screen.blit(textoMarcadorOrdenador,(self.screen.get_width()-10-sizeCabeceraMarcadorOrdenador[0]/2-sizeMarcadorOrdenador[0],30+sizeCabeceraMarcadorOrdenador[1]))
    
    #Este m�todo controla el r�tulo que mostramos con el resultado de una ronda       
    def rotuloResultado(self, rotulo):
        #Generamos la fuente que llevar� el rotulo
        fuenteResultado = pygame.font.SysFont(self.TIPO_FUENTE_1, 20)
        sizeTextoResultado = fuenteResultado.size(rotulo)
        #Generamos el texto
        textoResultado = fuenteResultado.render(rotulo, False, (255, 161, 0))
        #Mostramos el texto en la parte central de la pantalla
        self.screen.blit(textoResultado,(self.screen.get_width()/2-(sizeTextoResultado[0]/2),self.screen.get_height()/2+(sizeTextoResultado[1]/2)))
    
    #Este m�todo calcula el resultado de una ronda y actualiza
    #la variable marcador de la clase
    def calcularResultado(self):
        try:
            #Recuperamos las cartas de la ronda
            cartajugador = self.cartasjugador[0]
            cartaordenador = self.cartasordenador[0]
            #Recuperamos el valor los marcadores
            j = self.marcador["jugador"]
            o = self.marcador["ordenador"]
            #Con el m�todo convertir_Carta_A_Num convertirmos el 
            #atributo string numero de la clase Carta a valor
            #num�rico para as� poder compararlo
            numJugador = Utiles.convertir_Carta_A_Num(cartajugador.numero)
            numOrdenador = Utiles.convertir_Carta_A_Num(cartaordenador.numero)
            #Si la carta del jugador es m�s alta, ha ganado la ronda
            if(numJugador>numOrdenador):
                #Sumamos uno a su marcador
                self.marcador = {"jugador":j+1,"ordenador":o}
            #Si la carta del jugador es m�s baja, ha ganado la ronda el ordenador
            elif(numJugador<numOrdenador):
                #Sumanos uno a su marcador
                self.marcador = {"jugador":j,"ordenador":o+1}
        except Exception as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Atrapamos cualquier excepci�n posible y mostramos
            #la pantalla de error
            pantallaError = PantallaError("Error al actualizar marcadores")
            pantallaError.mostrarPantallaError()
            sys.exit()
    
    #Este m�todo controla el mensaje que mostramos en el centro
    #al final de cada ronda
    def actualizarConResultado(self,cartajugador,cartaordenador):
        #Convertimos las cartas a valores num�ricos para poder
        #compararlas usando convertir_Carta_A_Num
        numJugador = Utiles.convertir_Carta_A_Num(cartajugador.numero)
        numOrdenador = Utiles.convertir_Carta_A_Num(cartaordenador.numero)
        #Si la carta del jugador es mayor que la del ordenador, es que gan� la ronda
        if(numJugador>numOrdenador):
            self.rotuloResultado("Gan� el jugador")
            return "J"
        #Si la carta del jugador es menor que la del ordenador, es que el ordenador gan� la ronda
        elif(numJugador<numOrdenador):
            self.rotuloResultado("Gan� el ordenador")
            return "O"
        else:
            #En caso contrario, ambas son iguales, por lo que hay empate
            self.rotuloResultado("Empate")
            return "E"
    
    #Este m�todo controla el r�tulo que sale en la parte
    #superior central que anuncia el n�mero de ronda
    def rotuloRonda(self,i):
        #Generamos una superfie que ser� el r�tulo
        popupSurf = pygame.Surface((350, 150))
        #Le damos un color de fondo
        popupSurf.fill(self.FONDO_POP_UP)
        #Generamos los textos que llevar� el r�tulo
        fuenteTextoPopUp = pygame.font.SysFont(self.TIPO_FUENTE_1, 20)
        sizeTextoPopUp = fuenteTextoPopUp.size("La ronda {0} ha terminado".format(i))
        textSurf = fuenteTextoPopUp.render("La ronda {0} ha terminado".format(i), 1, (0, 0, 0))
        #Generamos un rect�ngulo sobre el que pondremos el texto
        textRect = textSurf.get_rect()
        textRect.top = popupSurf.get_height()/2
        textRect.left = popupSurf.get_width()/2 - sizeTextoPopUp[0]/2
        #Mostramos el texto en este rect�ngulo
        popupSurf.blit(textSurf, (textRect.left,textRect.top))
        if i < 5:
            #Si i es menor que 5 es que aun quedan rondas
            sizeTextoPopUp2 = fuenteTextoPopUp.size("Cargando nueva ronda")
            textSurf2 = fuenteTextoPopUp.render("Cargando nueva ronda",1, (0, 0, 0))
        else:
            #En caso contrario es la �ltima ronda y por tanto se termina la partida
            sizeTextoPopUp2 = fuenteTextoPopUp.size("Partida finalizada")
            textSurf2 = fuenteTextoPopUp.render("Partida finalizada",1, (0, 0, 0))
        #Generamos un rect�ngulo sobre el que mostraremos ese texto    
        textRect2 = textSurf2.get_rect()
        textRect2.top = popupSurf.get_height()/2 + sizeTextoPopUp2[1]
        textRect2.left = popupSurf.get_width()/2 - sizeTextoPopUp2[0]/2
        #Mostramos el texto sobre ese rect�ngulo
        popupSurf.blit(textSurf2, (textRect2.left,textRect2.top))
        popupRect = popupSurf.get_rect()
        
        sizeTextoPopUp3 = fuenteTextoPopUp.size("Pulse cualquier tecla para continuar")
        textSurf3 = fuenteTextoPopUp.render("Pulse cualquier tecla para continuar", 1, (0, 0, 0))
        #Generamos un rect�ngulo sobre el que pondremos el texto
        textRect3 = textSurf.get_rect()
        textRect3.top = popupSurf.get_height()/2 + sizeTextoPopUp[1] + sizeTextoPopUp2[1]
        textRect3.left = popupSurf.get_width()/2 - sizeTextoPopUp3[0]/2
        #Mostramos el texto en este rect�ngulo
        popupSurf.blit(textSurf3, (textRect3.left,textRect3.top))
        
        popupRect.centerx = self.screen.get_width()/2
        popupRect.centery = 0
        #Mostramos los textos
        self.screen.blit(popupSurf, popupRect) 
        
        
        #Actualizamos la pantalla
        pygame.display.update()
        pygame.display.flip()
        
        #Esperamos a que el usuario pulse una tecla
        #Por ello inicialmente done = False
        done = False
        #Mientras que el usuario no pulse una tecla 
        #(es decir done = False)
        # seguiremos en la pantalla
        while not done:
            #Escuchamos todos los eventos del teclado y raton
            for event in pygame.event.get():
                #Escuchamos si el usuario pulsa una tecla
                if event.type == pygame.KEYDOWN:
                    #Ya podemos avanzar
                    done = True
                #Escuchamos si el usuario ha cerrado al ventana
                if event.type == pygame.QUIT:
                    #Y en tal caso detenemos la ejecuci�n
                    sys.exit()
