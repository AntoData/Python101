# coding: latin-1
'''
Created on 30 abr. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio Pérez Oviedo
Biblioteca estándar:
- sys: para deterner la ejecución en caso de excepción con sys.exit()
y para obtener los datos de dónde se produce la excepción en el código
- os: para la gestión de ficheros (comprobar si existe, ver en qué fichero
se encuentra la ejecución cuando se produce una excepción...)
Módulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepción
- MesaJuego: Para poder generar un método encapsule todas las acciones
que se hacen en una partida, todas ellas en MesaJuego. MesaJuego es
una clase que encapsula las acciones que se hacen durante una partida
a nivel de interfaz
- ResultadoPartida: Para en el método que encapsula la partida
poder mostrar el resultado una vez que ha terminado. Esta clase controla
la pantalla que muestra los resultados de la partida
- Estadisticas: Es el módulo que almacena tanto los datos estadísticos
como realiza los cálculos como los representa. Aquí es donde en
el método controladorPartida lo usaremos para meter datos en el csv 
'''
import sys
import os
from Front.MesaJuego import MesaJuego
from Front.ResultadoPartida import ResultadoPartida
from Front.PantallaError import PantallaError
import Back.Estadisticas as Estadisticas
"""
Este fichero contendrá métodos útiles que usaremos en otros partes 
del código.
Al ser sólo un conjunto de métodos que se aplicarán en distintas
partes del código que no tienen por qué guardar relación entre sí
no tenía sentido que esto fuese una clase (aunque hubiera sido una clase
estática, es decir una clase donde todos los métodos son estáticos)
y así mostramos el paradigma de programación imperativa que Python
también soporta
"""
#Para hacer el código más eficiente, hemos añadido las variables globales
#que usaremos en todo el programa
#Hemos creado esta variable global que contiene la ruta de la carpeta donde se encuentran los ficheros
# asociados a las cartas
RUTA_CARTAS = r"./Cartas"

#Esta variable global contiene la ruta para la imagen que 
#usara el fondo del menú inicial
RUTA_FONDO_MENU_INICIAL = r"./Front/images/Background.png" 

#Esta variable global contiene la ruta para la imagen que
#usara de fondo la clase mesa de juego
RUTA_FONDO_MESA_JUEGO = r"./Front/images/BackgroundBaraja2.png"

#Esta variable global contiene la expresión que usaremos para
#llegar hasta las imágenes que componen la animación de barajar
RUTA_IMAGENES_ANIMACION_BARAJAR = r"./Cartas/AnimacionBarajar/frame_{0}_delay-0.17s.gif"  

#Esta variable gloabl contiene la ruta del fondo del
#tapete de la mesa de juego
RUTA_TAPETE = r"./Front/images/MesaColores.jpg" 

#Aquí incluimos el tipo de letra que usaremos en algunos textos
LETRA_TEXTO_1 = 'Futura PT'

#Aquí incluimos el tamaño de la letra que usaremos en algunos textos
TAMAÑO_TEXTO_1 = 70

#Definimos aquí el color que tendrán las letras del item del menú que
#no hemos seleccionado
COLOR_ITEM_NO_SELECCIONADO = (76, 15, 2)

#Definimos aquí el color que tendrán las letras del item del menú que
# hemos seleccionado
COLOR_ITEM_SELECCIONADO = (164, 68, 1)

#Al tener que comparar los valores de las cartas entre sí, pero tener
# cartas como la SOTA, CABALLO y REY que no son numéricos aunque tienen
# una escala de valor, no podemos comparar directamente el valor de una 
# carta con otra, para ello hemos generado los siguientes métodos

# Este convierte un número al String correspondiente al numero de la carta7
# que usaremos en la clase CartaBaraja
def convertir_Num_A_Carta(num):
    #Para ello generamos una estructura de ifs anidados, especificando
    # los casos en los que hay que cambiar el valor numérico por otro
    # string distinto (1 por AS, 10 por SOTA..) y devolvemos directamente
    # el string. También ponemos un elif que controle el caso en que los 
    # valores no sean correctos y lanzamos nuestra pantalla de error en ese
    # caso. Finalmente solo quedan los casos en los que solo habrá que
    # convertir el int de num a string y lo devolvemos también
    if num == 1:
        return "AS"
    elif num == 10:
        return "SOTA"
    elif num == 11:
        return "CABALLO"
    elif num == 12:
        return "REY"
    elif num > 12 or num < 0:
        pantallaError = PantallaError(r"Error {0} no es un valor válido de carta".format(num))
        pantallaError.mostrarPantallaError()
        sys.exit()
    else:
        return str(num)

#Este método hace el proceso opuesto al anterior, dado el string número
# de la clase CartaBaraja nos devuelve el valor numérico asociado
# En este caso, asociamos el 10 a la SOTA, el 11 al CABALLO y el 12 al REY
# tal y como viene haciéndose tradicionalmente. Esto en realidad solo lo
# usaremos para poder comparar cartas en cada ronda del juego
def convertir_Carta_A_Num(carta):
    #Igual que antes generamos una estructura de ifs anidada donde
    # primero ponemos el casos donde no podemos convertir directamente
    # el string a int y luego mediante un else controlamos el resto de
    # casos. Es importante en ese último caso que controla todos los
    # casos en los que se puede hacer la conversión directamente, el crear
    # una estructura try y except donde controlemos el proceso de conversión
    # de string a int. Puesto que a ese caso llegará cualquier string
    # que no sea AS, SOTA, CABALLO y REY, por lo que podría resultar
    # que llegara cualquier string que no fuera convertible a int y
    # eso tenemos que controlarlo mostrando la pantalla de error
    if carta == "AS":
        return 1
    elif carta == "SOTA":
        return 10
    elif carta == "CABALLO":
        return 11
    elif carta == "REY":
        return 12
    else:
        try:
            num = int(carta)
            return num
        except Exception as e:
            #Ante cualquier excepción, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepción: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            
            pantallaError = PantallaError(r"Error {0} no es un valor válido de carta".format(carta))
            pantallaError.mostrarPantallaError()
            sys.exit()  

#Todas nuestras cartas estarán asociadas a una imagen que sea la que
# sea mostrada por pantalla cuando salgan elegidas en la baraja.
#Este método realiza la conversión entre el palo y valor de la carta
# y la ruta relativa a la imagen
def convertir_Carta_A_Ruta(palo,carta):
    #Como las cartas están nombradas por números del 1 al 12 y las cartas
    # de cada palo están en una carpeta distinta
    # Convertimos el valor de la carta a numérico
    num = convertir_Carta_A_Num(carta)
    # Componemos la ruta a ese carta: RUTA_CARTAS es donde se encuentra
    # la carpeta principal, luego en palo estarán las imágenes de las cartas
    # de cada palo y el último trozo es simplemente el número de cada una
    # que es como se llaman + jpg que es el formato en que se encuentran
    ruta = RUTA_CARTAS + "/" + palo + "/" + "{0}.jpg".format(num) 
    return ruta

#Este método procesa la respuesta que genera el evento del interacción
# del usuario cuando en la clase MenuInicial selecciona una opción
# En este caso utilizamos la asignación de valores por defecto a parámetros
# de entrada para el parámetro screen           
def procesarRespuestaMenu(i,screen = None):
    #En este caso generamos una estructura de ifs aninados
    # Solo hay tres valores posibles
    # Caso el usuario elige el primer item, significa que el usuario
    # quiere jugar una partida
    if i == 0:
        #Llamamos al método controladorPartida que gestiona todos
        # los eventos necesario para generar esa partida
        controladorPartida(screen)
    elif i == 1:
        Estadisticas.generarGraficoEstadisticas(Estadisticas.RUTA_FICHERO_CSV)
    elif i == 2:
        #En caso de seleccionar Salir, simplemente detenemos la ejecución
        sys.exit()
    else:
        #Controlamos por si acaso el caso en que llegara un valor inválido
        # y mostramos la pantalla de error
        pantallaError = PantallaError(r"Error con los items del menú")
        pantallaError.mostrarPantallaError()
        sys.exit() 

def controladorPartida(screen = None):
    #Generamos un objeto MesaJuego que contiene todos los métodos
    # para que realicemos la partida para el usuario
    mesaJuego = MesaJuego(screen)
    #Llamos al método prepararCartasPrimeraRonda que hace varias cosas
    # Baraja las cartas y genera la animación de barajado
    # Genera el pop-up para pedir al usuario que introduzca un valor
    # por el teclado para cortar la baraja y corta la baraja por ahí
    mesaJuego.prepararCartasPrimeraRonda()
    #Como cada partida tiene 5 ronda, usarmos un bucle for
    # que genere 5 iteraciones (de ahí el range(0,5)
    for i in range(0,5):
        #En cada ronda, debemos llamar a este método
        #animacionPapete encapsula la sacada de carta de la baraja
        # para el usuario, luego la del ordenador y la animación
        # en como se presenta el usuario
        marcador = mesaJuego.animacionPapete()
        # Una vez la animación para mostramos el rótulo de la
        # ronda actual, usando este método
        mesaJuego.rotuloRonda(i+1)
    
    #Cuando salimos del bucle for, implica que ya se han terminado
    # todas las rondas, por lo que ya hemos terminado la partida
    # Ya solo queda anunciar al usuario quien ha ganado
    # Para ello, generamos un objeto de la clase ResultadoPartida
    # que controla la pantalla de resultados
    pantallaResultado = ResultadoPartida(screen)
    #Y llamamos al método PantallaResultado que es el controlador de
    # esa pantalla
    datarowPartida = pantallaResultado.PantallaResultado(marcador)
    #Como hemos terminado la ronda, actualizamos el csv
    for datarowRonda in mesaJuego.datacsv:
        Estadisticas.anadirNuevoRegistro(Estadisticas.RUTA_FICHERO_CSV,datarowRonda)
    #Limpiamos el objeto auxiliar donde guardamos los registros
    #para el csv ya que hemos terminado la ronda, para la siguiente
    mesaJuego.datacsv.clear()
    Estadisticas.anadirNuevoRegistro(Estadisticas.RUTA_FICHERO_CSV,datarowPartida)
