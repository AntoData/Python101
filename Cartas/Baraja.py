# coding: latin-1
'''
Created on 3 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Biblioteca est�ndar:
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
- os: para la gesti�n de ficheros (comprobar si existe, ver en qu� fichero
se encuentra la ejecuci�n cuando se produce una excepci�n...)
- random: M�dulo que proporciona diversos m�todos para generar n�meros u �rdenes aleatorios
Lo usamos para barajar la baraja usando shuffle y para generar un n�mero entero aleatorio entre 0
y la longitud de la baraja con randint
- datetime: M�dulo que usamos para obtener el instante actual hasta el microsegundo
para a�adir al log baraja.txt cuando empieza una partida nueva
M�dulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepci�n
- FicheroBaraja: M�dulo que encapsula la gesti�n del fichero baraja.txt en dos m�todos
- Utiles: m�dulo con diversos m�todos para gestionar correctamente aspectos de la baraja y las cartas
- Carta: Clase que representa una carta (junto con su sprite y atributos)
'''
import Cartas.CartaBaraja as Carta
import random
import sys
from Front.PantallaError import PantallaError
import Back.FicheroBaraja as FicheroBaraja
from Cartas import Utiles as Utiles
import datetime
import os
"""
Esta clase representa a la baraja de este juego. Es m�s �til y pr�ctico
en este caso generar una clase que contendr� todos los atributos y 
m�todos relacionados con la baraja puesto que este problema se ajusta
al paradigma de programaci�n orientada a objetos
B�sicamente nuestra baraja lo que contiene es una lista de cartas
Hemos seleccionado la lista como estructura de datos para representar
la baraja por varios motivos. Primero, la estructura de datos deb�a ser
modificable puesto que en la baraja se baraja, se corta y se extraen cartas.
Adem�s, el orden es importante. Las cartas est�n puestas en un orden en la
baraja. Al ser una lista adem�s, podemos tener varias opciones para extraer
la carta, sacar una carta de cualquier lugar de la baraja (carta aleatoria)
sacar la carta del principio de la baraja o sacarla del final.
Actualmente solo sacamos las cartas del mazo de la parte de arriba tal y
como describe el enunciado
"""
class Baraja:
    #Tambi�n nos generamos una variable palos, ya que nos puede
    # resultar �til a futuro y evitar repetir este trozo de c�digo
    palos = ["ORO","COPA","ESPADA","BASTO"]
    #Con la excusa de generar alguna funci�n lambda en este c�digo,
    #se ha generado esta funci�n lambda que genera un n�mero aleatorio
    # entero entre 0 y x que es el que usamos cuando queremos sacar una
    # carta aleatoria. Adem�s esto hace el c�digo m�s legible y c�modo
    elegirCartaAleatoria = lambda self,x: random.randint(0,x)
    
    #El constructor de esta clase no necesita par�metros de entrada
    #puesto que seg�n las instrucciones toda baraja se genera en un
    #orden determinado. Lleva la anotaci�n @....... con el decorador
    #y sus par�metros para que cuando llamemos al constructor se ejecuten
    #las modificaciones que hemos incluido, en este caso limpiar primero
    #la lista de cartas antes de empezar a a�adirlas una a uno
    def __init__(self):
        #Como la misi�n de este constructor es generar la baraja en su
        # estado incial, es decir, completar la lista de cartas
        # con el orden inicial que deben tener y las cartas en realidad
        # son Sprites de pygame que contienen im�genes, pueden ocurrir
        # errores, como que la imagen asociada a determinada carta no est�
        # o que por error el bucle sea modificado y los l�mites sean
        # modificados. Por ello envolvemos todo el algoritmo en una
        # estructura try and except para poder controlar cualquier error
        try:
            #La estructura que contendr� las cartas de nuestra bajara
            #ser� una lista puesto que es modificable y est� indexada
            self.cartas = []
            #Recorremos el array de palos
            for palo in self.palos:
                #Por cada palo vamos del 1 al 12 que son las cartas que
                # tiene cada palo
                for i in range(1,13):
                    #Utilizamos el m�todo convertir_Num_A_Carta
                    #del fichero Utiles para convertir el n�mero
                    # i al valor asociado de la carta en string en
                    # num
                    num = Utiles.convertir_Num_A_Carta(i)
                    #Ese valor de la carta en string en num y el valor en string
                    #del palo, son los par�metros de entrada del constructor
                    # de la clase Cartas, as� que ya podemos generar el objeto
                    # carta correspondiente a esa carta
                    c =  Carta.Carta(num,palo)
                    #Una vez generada la carta, se a�ade a la lista de la baraja cartas
                    self.cartas.append(c)
        except Exception as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Luego, mostramos la pantalla de error
            pantallaError = PantallaError("Ocurri� un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
    
    #Este m�todo es el que realiza la l�gica de barajar
    #Tanto de cambiar el orden de las cartas en la lista cartas
    #Como de escribir en el fichero /logs/baraja.txt las iteraciones sobre
    #la baraja
    def barajar(self):
        #Generamos un string con la fecha de comienzo de la partida 
        #ser� uno de los par�metros a pasar a la clase que controla
        #la escritura en el fichero baraja.txt
        fechaComienzoPartida = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n"
        #En la variable ordenOriginal iremos guardando, el orden original
        #de la baraja antes de barajar
        ordenOriginal = "Orden original\r\n"
        #Para ello recorremos la lista de cartas con un bucle for
        for carta in self.cartas:
            #En cada iteraci�n a�adimos la representaci�n en string de la
            #carta en una nueva l�nea en la variable
            ordenOriginal += "{0}\r\n".format(carta)
        #Este m�todo random.shuffle lo que hace es aplicar un orden aleatorio
        #a una lista. Por tanto, lo usamos para barajar nuestras cartas
        #ya que barajar no es m�s que aplicar un orden aleatorio a la baraja
        random.shuffle(self.cartas)
        ordenOriginal += "--------------\r\n"
        #Una vez barajadas las cartas, guardamos el nuevo orden en la variable
        #ordenBarajado
        ordenBarajado = "Barajando\r\n"
        ordenBarajado += "Orden barajado\r\n"
        #Para ello recorremos la lista de cartas con un bucle for
        for carta in self.cartas:
            #En cada iteraci�n a�adimos la representaci�n en string de la
            #carta en una nueva l�nea en la variable
            ordenBarajado += "{0}\r\n".format(carta)
        ordenBarajado += "--------------\r\n"
        #Finalmente usamos el m�todo escribirFichero de la clase FicheroBaraja
        #Tal case es una clase que controla todos los aspectos relacionados
        #con el fichero en el que escribimos el estado de la baraja
        #escribirFichero tiene un primer par�metro ruta que es la ruta
        #donde se encuentra el archivo y luego podemos meter tantos
        #par�metros como quedamos, siempre que sean par�metros que contengan
        #l�neas de caracteres de texto string
        #Se realiz� as� para tener un ejemplo en este c�digo de una funci�n
        #que recibe sus par�metros como una tupla
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,fechaComienzoPartida,ordenOriginal,ordenBarajado)
    
    #Este m�todo extrae una carta aleatoria de la baraja
    def seleccionarAleatoriaCarta(self):
        #Lo primero que hacemos es comprobar si quedan o no cartas en la baraja
        if len(self.cartas) == 0:
            #Si no hay cartas mostramos la pantalla de error
            pantallaError = PantallaError("Ocurri� un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Si todav�a quedan cartas, usamos el m�todo pop para eliminar una carta
        #en una posici�n determinada de la lista cartas (la baraja) y
        #devolverla a la variable carta
        #Para determinar de qu� posici�n sacamos la carta, usamos
        #la funci�n lambda elegirCartaAleatoria pas�ndole como par�metro
        #el tama�o de la lista -1 (ya que al empezar los �ndices por 0
        #el �ltimo �ndice corresponde al tama�o de la lista menos 1)
        #Esta funci�n generar� un n�mero aleatorio de entre todas
        #las posiciones posibles de la lista
        carta = self.cartas.pop(self.elegirCartaAleatoria(len(self.cartas)-1))
        #Ahora guardaremos el nuevo orden de la baraja en el fichero
        orden = "Tras sacar la carta {0} la baraja queda:\r\n".format(carta)
        #Recorremos la baraja usando un bucle for
        for c in self.cartas:
            #Y guardamos una representaci�n de cada carta en una l�nea
            orden += "{0}\r\n".format(c)
        orden += "--------------\r\n"
        #Usamos el m�todo escribirFichero para actualizar el fichero de
        #baraja.txt
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,orden)
        #Devolvemos la carta extra�da finalmente
        return carta
    #Este m�todo selecciona la carta que est� en la parte m�s alta del mazo
    #de la baraja
    def seleccionarCartaSuperior(self):
        #Si la baraja no tiene cartas, mostramos la pantalla de error
        if len(self.cartas) == 0:
            pantallaError = PantallaError("Ocurri� un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Extraemos la carta en la posici�n 0, la primera, que es la carta
        #de la parte superior del mazo
        carta = self.cartas.pop(0)
        #Recorremos la baraja con un bucle for para guardar en la variable
        #orden el nuevo estado de la baraja
        orden = "Tras sacar la carta {0} que estaba en la parte superior la baraja queda:\r\n".format(carta)
        for c in self.cartas:
            #En cada iteraci�n guardamos la representaci�n de una carta
            #en una l�nea
            orden += "{0}\r\n".format(c)
        orden += "--------------\r\n"
        #Usamos el m�todo escribirFichero para actualizar el fichero
        #baraja.txt
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,orden)
        return carta
    
    #Este m�todo selecciona la carta que est� en la parte m�s baja del mazo
    #de la baraja
    def seleccionarCartaInferior(self):
        #Si la baraja no tiene cartas, mostramos la pantalla de error
        if len(self.cartas) == 0:
            pantallaError = PantallaError("Ocurri� un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Si hay cartas en la baraja, extraemos la �ltima carta en la lista
        #y la devolvemos como par�metro usando el m�todo pop
        #Para obtener la carta en la �ltima posici�n, obtenemos la longitud
        #de la lista y le quitamos 1 (al empezar los �ndices por 0, el �tlimo
        #equivale a la longitud de la lista - 1
        carta = self.cartas.pop(len(self.cartas)-1)
        #Ahora guardamos el nuevo orden de la baraja en el fichero baraja.txt
        orden = "Tras sacar la carta {0} que estaba en la parte inferior la baraja queda:\r\n".format(carta)
        #Para ello recorremos la lista de cartas con un bucle for
        for c in self.cartas:
            #En cada iteraci�n guardamos una representaci�n de string
            #en una l�nea
            orden += "{0}\r\n".format(c)
        orden += "--------------\r\n" 
        #Actualizamos el fichero baraja.txt
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,orden)
        #Devolvemos la variable carta con la carta extra�da
        return carta
    
    #Este m�todo es el que corta la baraja por la posici�n n,
    #a�adiendo todas las cartas que hubiera por encima de esa posici�n
    #por debajo
    def cortarBaraja(self,n):
        #Lo primero es comprobar que n tiene un valor v�lido
        #n tiene que ser mayor que 0 y m�s peque�a que la �ltima
        #posici�n de la baraja
        #Como a este m�todo lo llamamos a trav�s de interacci�n
        #con el usuario tendremos que quitarle uno para que tenga
        #encuenta que empezamos por la posici�n 0
        num = n-1
        if num<0 or num>len(self.cartas)-1:
            #Si el valor de n es inv�lido, mostramos la pantalla de error
            pantallaError = PantallaError("El valor introducido debe estar en el rango [1,{0}]".format(len(self.cartas)))
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Ahora generamos una estructura try y except
        try:
            #Primero guardamos el orden antes de cortar la baraja
            #en la variable ordenOriginal
            ordenOriginal = "Orden Antes de Cortar la baraja\r\n"
            #Para ello recorremos la lista de cartas con un bucle for
            for carta in self.cartas:
                #En cada iteraci�n guardamos una representaci�n
                #en string en una l�nea nueva en la variable
                ordenOriginal += "{0}\r\n".format(carta)
                
            ordenOriginal += "--------------\r\n"
            #Creamos un par�metro sublist vac�o
            #que contendr� todas las cartas de la parte superior
            #que vamos a cortar e incluir en la inferior
            sublist = []
            for _ in range(n):
                #Para ello vamos sacando todas las cartas en la posici�n 0
                #hasta n - 1 (si el usuario quiere cortar por la posici�n
                #5 por ejemplo, nosotros tenemos que guardar de la 0 a la 4
                #que es equivalente a range(5) y las agregamos al final
                #de la variable sublist
                sublist.append(self.cartas.pop(0))
        
            nuevoOrden = "Nuevo orden tras cortar por la posici�n {0}\r\n".format(n)
            #Ahora simplemente usamos el m�todo extend de la clase list
            #para a�adir la lista sublist que contiene las cartas que vamos
            #a pasar al final de la baraja al final de nuestra lista cartas
            #que representa las cartas de nuestra baraja, habiendo completado
            #la acci�n de cortar la baraja
            self.cartas.extend(sublist)
            #Ahora recorremos la baraja mediante un bucle for
            for carta in self.cartas:
                #En cada iteraci�n agregamos una representaci�n en string
                #de la carta en una nueva l�nea a la variable nuevoOrden
                nuevoOrden += "{0}\r\n".format(carta)
            #Utilizamos el m�todo escribirFichero para actualizar el fichero
            #baraja.txt
            nuevoOrden += "--------------\r\n"
            #En este caso tambi�n con motivos did�cticos hemos generado varias
            #variables de string que pasar al m�todo para usar su caracter�stica
            #de tener una tupla de par�metros
            FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,ordenOriginal,nuevoOrden)
        except Exception as e:
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Luego, mostramos la pantalla de error
            pantallaError = PantallaError("Ocurri� un error al cortar la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
