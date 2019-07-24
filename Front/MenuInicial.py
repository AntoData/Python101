# coding: latin-1
'''
Created on 4 may. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pygame (1.9.6): para la interfaz gr�fica
Biblioteca est�ndar:
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
- os: para la gesti�n de ficheros (comprobar si existe, ver en qu� fichero
se encuentra la ejecuci�n cuando se produce una excepci�n...)
M�dulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepci�n
- Pantalla: que es una clase padre que controla la configuraci�n de la ventana/pantalla del juego
- Utiles: m�dulo con diversos m�todos para gestionar correctamente aspectos de la baraja y las cartas
(por ejemplo la conversi�n del "n�mero" de la carta en string al valor integer basado en su posici�n
en el palo) 
'''
import pygame
import os
import sys
import Front.Pantalla as Pantalla
import Front.PantallaError as PantallaError
import Cartas.Utiles as Utiles
"""
La clase MenuInicial hereda de la clase Pantalla. Esta clase
MenuInicial representa el men� inicial del programa
"""
class MenuInicial(Pantalla.Pantalla):
    #Definimos aqu� el color que tendr�n las letras del item del men� que
    #no hemos seleccionado
    COLOR_ITEM_NO_SELECCIONADO = (76, 15, 2)

    #Definimos aqu� el color que tendr�n las letras del item del men� que
    # hemos seleccionado
    COLOR_ITEM_SELECCIONADO = (164, 68, 1)
    
    #Definimos una variable que contenga los items del men�
    ITEMS_MENU = ["Partida","Estad�sticas","Salir"]
    
    #Definimos el constructor para esta clase con el par�metro screen a None
    def __init__(self,screen = None):
        #Llamamos al constructor de la clase padre
        Pantalla.Pantalla.__init__(self,screen)
        #El par�metro seleccionado representa cual es el item del men�
        #que hemos seleccionado, iniciado a 0
        self.seleccionado = 0
        self._items = ["Partida","Estad�sticas","Salir"]
        #fin es un boolean que controla cuando terminamos el bucle
        #que controla la pantalla
        self.fin = False
    
    #Por motivos did�cticos hemos definido el atributo
    #de clase items como una propiedad donde controlamos
    #como se accede a ella y como se modifica
    #Cuando queremos obtener el par�metro, simplemente lo
    #devolvemos
    @property
    def items(self):
        return self._items
    
    #Sin embargo, cuando queremos darle valor al par�metro
    #no igualamos al par�metro haciendo una copia superficial
    #que b�sicamente crea un puntero hacia la nueva variable
    #a la que lo estamos igualando y que en caso de ser modificada
    #har�a que nuestro atributo fuese modificado
    #Lo que hacemos es borrar nuestro atributo items y copiar
    #uno por uno todos los items a la lista definiendo
    #el m�todo setter para este atributo usando la anotaci�n
    #@items.setter
    @items.setter
    def items(self,itemsList):
        self._items.clear()
        for i in itemsList:
            self._items.append(i)
            
    def menuInicial(self):
        #Definimos una variable background que representa el fondo que tendr�
        #esta pantalla
        background = None
        try:
            #Dentro del try, cargamos la imagen
            background = pygame.image.load(Utiles.RUTA_FONDO_MENU_INICIAL).convert()
        except FileNotFoundError as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos la excepci�n en el caso de que no hayamos encontrado el fichero
            pantallaError = PantallaError(r"Falta el fichero .\Front\images\Background.png")
            pantallaError.mostrarPantallaError()
            sys.exit()
        except Exception as e1:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e1))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Recogemos la excepci�n en el caso de que no hayamos encontrado el fichero
            pantallaError = PantallaError.PantallaError(r"Falta el fichero .\Front\images\Background.png")
            pantallaError.mostrarPantallaError()
            sys.exit()
        
        #Definimos el rect�ngulo donde mostraremos el fondo
        background_rect = background.get_rect()
        #Imprimimos la fondo usando el m�todo blit de screen
        self.screen.blit(background,background_rect)
        #Estos son los items que tendr� el men� inicial
        posicionesItems = []
        while not self.fin:
            #Mientras que no hayamos elegido un item,
            #ejecutamos esos m�todos
            #Siempre llamamos el m�todo responderEventos que controla
            #si hemos hecho click o hemos pulsado Intro en el men�
            self.responderAEventos(self.items, posicionesItems)
            #Llamamos al m�todo pintarMenu que encapsula los m�todos
            #para imprimir por pantalla el men�
            self.pintarMenu(self.items, posicionesItems)
            #Actualizamos la pantalla con display.flip
            pygame.display.flip()
            #Devolvemos la posici�n del item seleccionado
        return self.seleccionado
    
    #Este m�todo pintarMenu encapsula todas las acciones necesarias para prinar el men�
    #de manera did�ctica incluimos un docstring aqu� donde
    #sugerimos que el tipo que hay que devolver es int,
    #tambi�n decimos que el tipo sugerido del par�metro items es
    #una lista
    def pintarMenu(self,items:list,posicionesItems) -> list:
        #Iniciamos las fuentes de pygame usando font.init
        pygame.font.init()
        #Recogemos los items del menu
        for j in range(len(items)):
            #Definimos la fuente que usaremos para el men�
            fuenteItem = pygame.font.SysFont(Utiles.LETRA_TEXTO_1, Utiles.TAMA�O_TEXTO_1)
            #Guardamos el tama�o de la fuetne
            tama�oItem = fuenteItem.size(items[j])
            #Para imprimir, el men� de inicio, si no es el elemento
            #seleccionado
            textoItem = None
            if j!=self.seleccionado:
                #Guardamos en una variable la fuente de los item no seleccionado
                textoItem = fuenteItem.render(items[j], False, self.COLOR_ITEM_NO_SELECCIONADO)
            else:
                #Guardamos en una variable la fuente de los item seleccionado
                textoItem = fuenteItem.render(items[j], False, self.COLOR_ITEM_SELECCIONADO)
            #Mostramos en pantalla la fuente usando screen.blit
            self.screen.blit(textoItem,(self.screen.get_width()/2-(tama�oItem[0]/2),self.screen.get_height()/2+(tama�oItem[1]/2)+(j*70)))
            #Guardamos los items en la lista posicionesItems
            if len(posicionesItems)<len(items):
                item = textoItem.get_rect()
                item.left, item.top = self.screen.get_width()/2-(tama�oItem[0]/2),self.screen.get_height()/2+(tama�oItem[1]/2)+(j*70)
                posicionesItems.append(item)
        #Devolvemos el �ndice del elemento seleccionado
        return self.seleccionado
    
    #Este m�todo lo usamos para responder a los ventos
    def responderAEventos(self,items,posicionesItems):
        #Este bucle hace que estemos atentos a todos los eventos
        for evento in pygame.event.get ():
            #keyinput guarda la tecla de hayamos pulsado
            keyinput = pygame.key.get_pressed()
            #As� podremos cerrar la ventana en todo momento
            if evento.type == pygame.QUIT:
                sys.exit()
            #Esto controla los clicks del rat�n en los elementos del menu
            elif evento.type == pygame.MOUSEBUTTONUP:
                for k in range(len(posicionesItems)):
                    if posicionesItems[k].collidepoint(pygame.mouse.get_pos()):
                        self.fin = True
                        self.seleccionado = k
            #Controlamos la interacci�n con el teclado
            elif keyinput != None:
                #Controlamos la subida y bajada de items usando
                #el teclado
                if keyinput[pygame.K_UP]:
                    if self.seleccionado>0:
                        self.seleccionado-=1
                elif keyinput[pygame.K_DOWN]:
                    if self.seleccionado<len(items)-1:
                        self.seleccionado+=1
                #Si pulsamos Intro es que hemos seleccionado un elemento
                #Por lo que terminamos el bucle
                elif keyinput[pygame.K_KP_ENTER] or keyinput[pygame.K_RETURN]:
                    self.fin = True
