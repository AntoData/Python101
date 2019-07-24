# coding: latin-1
'''
Created on 3 may. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio Pérez Oviedo
Biblioteca estándar:
- sys: para deterner la ejecución en caso de excepción con sys.exit()
y para obtener los datos de dónde se produce la excepción en el código
- os: para la gestión de ficheros (comprobar si existe, ver en qué fichero
se encuentra la ejecución cuando se produce una excepción...)
- random: Módulo que proporciona diversos métodos para generar números u órdenes aleatorios
Lo usamos para barajar la baraja usando shuffle y para generar un número entero aleatorio entre 0
y la longitud de la baraja con randint
- datetime: Módulo que usamos para obtener el instante actual hasta el microsegundo
para añadir al log baraja.txt cuando empieza una partida nueva
Módulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepción
- FicheroBaraja: Módulo que encapsula la gestión del fichero baraja.txt en dos métodos
- Utiles: módulo con diversos métodos para gestionar correctamente aspectos de la baraja y las cartas
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
Esta clase representa a la baraja de este juego. Es más útil y práctico
en este caso generar una clase que contendrá todos los atributos y 
métodos relacionados con la baraja puesto que este problema se ajusta
al paradigma de programación orientada a objetos
Básicamente nuestra baraja lo que contiene es una lista de cartas
Hemos seleccionado la lista como estructura de datos para representar
la baraja por varios motivos. Primero, la estructura de datos debía ser
modificable puesto que en la baraja se baraja, se corta y se extraen cartas.
Además, el orden es importante. Las cartas están puestas en un orden en la
baraja. Al ser una lista además, podemos tener varias opciones para extraer
la carta, sacar una carta de cualquier lugar de la baraja (carta aleatoria)
sacar la carta del principio de la baraja o sacarla del final.
Actualmente solo sacamos las cartas del mazo de la parte de arriba tal y
como describe el enunciado
"""
class Baraja:
    #También nos generamos una variable palos, ya que nos puede
    # resultar útil a futuro y evitar repetir este trozo de código
    palos = ["ORO","COPA","ESPADA","BASTO"]
    #Con la excusa de generar alguna función lambda en este código,
    #se ha generado esta función lambda que genera un número aleatorio
    # entero entre 0 y x que es el que usamos cuando queremos sacar una
    # carta aleatoria. Además esto hace el código más legible y cómodo
    elegirCartaAleatoria = lambda self,x: random.randint(0,x)
    
    #El constructor de esta clase no necesita parámetros de entrada
    #puesto que según las instrucciones toda baraja se genera en un
    #orden determinado. Lleva la anotación @....... con el decorador
    #y sus parámetros para que cuando llamemos al constructor se ejecuten
    #las modificaciones que hemos incluido, en este caso limpiar primero
    #la lista de cartas antes de empezar a añadirlas una a uno
    def __init__(self):
        #Como la misión de este constructor es generar la baraja en su
        # estado incial, es decir, completar la lista de cartas
        # con el orden inicial que deben tener y las cartas en realidad
        # son Sprites de pygame que contienen imágenes, pueden ocurrir
        # errores, como que la imagen asociada a determinada carta no esté
        # o que por error el bucle sea modificado y los límites sean
        # modificados. Por ello envolvemos todo el algoritmo en una
        # estructura try and except para poder controlar cualquier error
        try:
            #La estructura que contendrá las cartas de nuestra bajara
            #será una lista puesto que es modificable y está indexada
            self.cartas = []
            #Recorremos el array de palos
            for palo in self.palos:
                #Por cada palo vamos del 1 al 12 que son las cartas que
                # tiene cada palo
                for i in range(1,13):
                    #Utilizamos el método convertir_Num_A_Carta
                    #del fichero Utiles para convertir el número
                    # i al valor asociado de la carta en string en
                    # num
                    num = Utiles.convertir_Num_A_Carta(i)
                    #Ese valor de la carta en string en num y el valor en string
                    #del palo, son los parámetros de entrada del constructor
                    # de la clase Cartas, así que ya podemos generar el objeto
                    # carta correspondiente a esa carta
                    c =  Carta.Carta(num,palo)
                    #Una vez generada la carta, se añade a la lista de la baraja cartas
                    self.cartas.append(c)
        except Exception as e:
            #Ante cualquier excepción, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepción: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Luego, mostramos la pantalla de error
            pantallaError = PantallaError("Ocurrió un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
    
    #Este método es el que realiza la lógica de barajar
    #Tanto de cambiar el orden de las cartas en la lista cartas
    #Como de escribir en el fichero /logs/baraja.txt las iteraciones sobre
    #la baraja
    def barajar(self):
        #Generamos un string con la fecha de comienzo de la partida 
        #será uno de los parámetros a pasar a la clase que controla
        #la escritura en el fichero baraja.txt
        fechaComienzoPartida = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n"
        #En la variable ordenOriginal iremos guardando, el orden original
        #de la baraja antes de barajar
        ordenOriginal = "Orden original\r\n"
        #Para ello recorremos la lista de cartas con un bucle for
        for carta in self.cartas:
            #En cada iteración añadimos la representación en string de la
            #carta en una nueva línea en la variable
            ordenOriginal += "{0}\r\n".format(carta)
        #Este método random.shuffle lo que hace es aplicar un orden aleatorio
        #a una lista. Por tanto, lo usamos para barajar nuestras cartas
        #ya que barajar no es más que aplicar un orden aleatorio a la baraja
        random.shuffle(self.cartas)
        ordenOriginal += "--------------\r\n"
        #Una vez barajadas las cartas, guardamos el nuevo orden en la variable
        #ordenBarajado
        ordenBarajado = "Barajando\r\n"
        ordenBarajado += "Orden barajado\r\n"
        #Para ello recorremos la lista de cartas con un bucle for
        for carta in self.cartas:
            #En cada iteración añadimos la representación en string de la
            #carta en una nueva línea en la variable
            ordenBarajado += "{0}\r\n".format(carta)
        ordenBarajado += "--------------\r\n"
        #Finalmente usamos el método escribirFichero de la clase FicheroBaraja
        #Tal case es una clase que controla todos los aspectos relacionados
        #con el fichero en el que escribimos el estado de la baraja
        #escribirFichero tiene un primer parámetro ruta que es la ruta
        #donde se encuentra el archivo y luego podemos meter tantos
        #parámetros como quedamos, siempre que sean parámetros que contengan
        #líneas de caracteres de texto string
        #Se realizó así para tener un ejemplo en este código de una función
        #que recibe sus parámetros como una tupla
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,fechaComienzoPartida,ordenOriginal,ordenBarajado)
    
    #Este método extrae una carta aleatoria de la baraja
    def seleccionarAleatoriaCarta(self):
        #Lo primero que hacemos es comprobar si quedan o no cartas en la baraja
        if len(self.cartas) == 0:
            #Si no hay cartas mostramos la pantalla de error
            pantallaError = PantallaError("Ocurrió un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Si todavía quedan cartas, usamos el método pop para eliminar una carta
        #en una posición determinada de la lista cartas (la baraja) y
        #devolverla a la variable carta
        #Para determinar de qué posición sacamos la carta, usamos
        #la función lambda elegirCartaAleatoria pasándole como parámetro
        #el tamaño de la lista -1 (ya que al empezar los índices por 0
        #el último índice corresponde al tamaño de la lista menos 1)
        #Esta función generará un número aleatorio de entre todas
        #las posiciones posibles de la lista
        carta = self.cartas.pop(self.elegirCartaAleatoria(len(self.cartas)-1))
        #Ahora guardaremos el nuevo orden de la baraja en el fichero
        orden = "Tras sacar la carta {0} la baraja queda:\r\n".format(carta)
        #Recorremos la baraja usando un bucle for
        for c in self.cartas:
            #Y guardamos una representación de cada carta en una línea
            orden += "{0}\r\n".format(c)
        orden += "--------------\r\n"
        #Usamos el método escribirFichero para actualizar el fichero de
        #baraja.txt
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,orden)
        #Devolvemos la carta extraída finalmente
        return carta
    #Este método selecciona la carta que está en la parte más alta del mazo
    #de la baraja
    def seleccionarCartaSuperior(self):
        #Si la baraja no tiene cartas, mostramos la pantalla de error
        if len(self.cartas) == 0:
            pantallaError = PantallaError("Ocurrió un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Extraemos la carta en la posición 0, la primera, que es la carta
        #de la parte superior del mazo
        carta = self.cartas.pop(0)
        #Recorremos la baraja con un bucle for para guardar en la variable
        #orden el nuevo estado de la baraja
        orden = "Tras sacar la carta {0} que estaba en la parte superior la baraja queda:\r\n".format(carta)
        for c in self.cartas:
            #En cada iteración guardamos la representación de una carta
            #en una línea
            orden += "{0}\r\n".format(c)
        orden += "--------------\r\n"
        #Usamos el método escribirFichero para actualizar el fichero
        #baraja.txt
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,orden)
        return carta
    
    #Este método selecciona la carta que está en la parte más baja del mazo
    #de la baraja
    def seleccionarCartaInferior(self):
        #Si la baraja no tiene cartas, mostramos la pantalla de error
        if len(self.cartas) == 0:
            pantallaError = PantallaError("Ocurrió un error con la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
        #Si hay cartas en la baraja, extraemos la última carta en la lista
        #y la devolvemos como parámetro usando el método pop
        #Para obtener la carta en la última posición, obtenemos la longitud
        #de la lista y le quitamos 1 (al empezar los índices por 0, el útlimo
        #equivale a la longitud de la lista - 1
        carta = self.cartas.pop(len(self.cartas)-1)
        #Ahora guardamos el nuevo orden de la baraja en el fichero baraja.txt
        orden = "Tras sacar la carta {0} que estaba en la parte inferior la baraja queda:\r\n".format(carta)
        #Para ello recorremos la lista de cartas con un bucle for
        for c in self.cartas:
            #En cada iteración guardamos una representación de string
            #en una línea
            orden += "{0}\r\n".format(c)
        orden += "--------------\r\n" 
        #Actualizamos el fichero baraja.txt
        FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,orden)
        #Devolvemos la variable carta con la carta extraída
        return carta
    
    #Este método es el que corta la baraja por la posición n,
    #añadiendo todas las cartas que hubiera por encima de esa posición
    #por debajo
    def cortarBaraja(self,n):
        #Lo primero es comprobar que n tiene un valor válido
        #n tiene que ser mayor que 0 y más pequeña que la última
        #posición de la baraja
        #Como a este método lo llamamos a través de interacción
        #con el usuario tendremos que quitarle uno para que tenga
        #encuenta que empezamos por la posición 0
        num = n-1
        if num<0 or num>len(self.cartas)-1:
            #Si el valor de n es inválido, mostramos la pantalla de error
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
                #En cada iteración guardamos una representación
                #en string en una línea nueva en la variable
                ordenOriginal += "{0}\r\n".format(carta)
                
            ordenOriginal += "--------------\r\n"
            #Creamos un parámetro sublist vacío
            #que contendrá todas las cartas de la parte superior
            #que vamos a cortar e incluir en la inferior
            sublist = []
            for _ in range(n):
                #Para ello vamos sacando todas las cartas en la posición 0
                #hasta n - 1 (si el usuario quiere cortar por la posición
                #5 por ejemplo, nosotros tenemos que guardar de la 0 a la 4
                #que es equivalente a range(5) y las agregamos al final
                #de la variable sublist
                sublist.append(self.cartas.pop(0))
        
            nuevoOrden = "Nuevo orden tras cortar por la posición {0}\r\n".format(n)
            #Ahora simplemente usamos el método extend de la clase list
            #para añadir la lista sublist que contiene las cartas que vamos
            #a pasar al final de la baraja al final de nuestra lista cartas
            #que representa las cartas de nuestra baraja, habiendo completado
            #la acción de cortar la baraja
            self.cartas.extend(sublist)
            #Ahora recorremos la baraja mediante un bucle for
            for carta in self.cartas:
                #En cada iteración agregamos una representación en string
                #de la carta en una nueva línea a la variable nuevoOrden
                nuevoOrden += "{0}\r\n".format(carta)
            #Utilizamos el método escribirFichero para actualizar el fichero
            #baraja.txt
            nuevoOrden += "--------------\r\n"
            #En este caso también con motivos didácticos hemos generado varias
            #variables de string que pasar al método para usar su característica
            #de tener una tupla de parámetros
            FicheroBaraja.escribirFichero(FicheroBaraja.RUTA,ordenOriginal,nuevoOrden)
        except Exception as e:
            #Ante cualquier excepción, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepción: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            #Luego, mostramos la pantalla de error
            pantallaError = PantallaError("Ocurrió un error al cortar la baraja")
            pantallaError.mostrarPantallaError()
            sys.exit()
