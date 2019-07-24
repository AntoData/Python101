# coding: latin-1
'''
Created on 30 abr. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Biblioteca est�ndar:
- sys: para deterner la ejecuci�n en caso de excepci�n con sys.exit()
y para obtener los datos de d�nde se produce la excepci�n en el c�digo
- os: para la gesti�n de ficheros (comprobar si existe, ver en qu� fichero
se encuentra la ejecuci�n cuando se produce una excepci�n...)
M�dulos propios:
- PantallaError: Clase que controla la pantalla de error que mostramos en caso de excepci�n
- MesaJuego: Para poder generar un m�todo encapsule todas las acciones
que se hacen en una partida, todas ellas en MesaJuego. MesaJuego es
una clase que encapsula las acciones que se hacen durante una partida
a nivel de interfaz
- ResultadoPartida: Para en el m�todo que encapsula la partida
poder mostrar el resultado una vez que ha terminado. Esta clase controla
la pantalla que muestra los resultados de la partida
- Estadisticas: Es el m�dulo que almacena tanto los datos estad�sticos
como realiza los c�lculos como los representa. Aqu� es donde en
el m�todo controladorPartida lo usaremos para meter datos en el csv 
'''
import sys
import os
from Front.MesaJuego import MesaJuego
from Front.ResultadoPartida import ResultadoPartida
from Front.PantallaError import PantallaError
import Back.Estadisticas as Estadisticas
"""
Este fichero contendr� m�todos �tiles que usaremos en otros partes 
del c�digo.
Al ser s�lo un conjunto de m�todos que se aplicar�n en distintas
partes del c�digo que no tienen por qu� guardar relaci�n entre s�
no ten�a sentido que esto fuese una clase (aunque hubiera sido una clase
est�tica, es decir una clase donde todos los m�todos son est�ticos)
y as� mostramos el paradigma de programaci�n imperativa que Python
tambi�n soporta
"""
#Para hacer el c�digo m�s eficiente, hemos a�adido las variables globales
#que usaremos en todo el programa
#Hemos creado esta variable global que contiene la ruta de la carpeta donde se encuentran los ficheros
# asociados a las cartas
RUTA_CARTAS = r"./Cartas"

#Esta variable global contiene la ruta para la imagen que 
#usara el fondo del men� inicial
RUTA_FONDO_MENU_INICIAL = r"./Front/images/Background.png" 

#Esta variable global contiene la ruta para la imagen que
#usara de fondo la clase mesa de juego
RUTA_FONDO_MESA_JUEGO = r"./Front/images/BackgroundBaraja2.png"

#Esta variable global contiene la expresi�n que usaremos para
#llegar hasta las im�genes que componen la animaci�n de barajar
RUTA_IMAGENES_ANIMACION_BARAJAR = r"./Cartas/AnimacionBarajar/frame_{0}_delay-0.17s.gif"  

#Esta variable gloabl contiene la ruta del fondo del
#tapete de la mesa de juego
RUTA_TAPETE = r"./Front/images/MesaColores.jpg" 

#Aqu� incluimos el tipo de letra que usaremos en algunos textos
LETRA_TEXTO_1 = 'Futura PT'

#Aqu� incluimos el tama�o de la letra que usaremos en algunos textos
TAMA�O_TEXTO_1 = 70

#Definimos aqu� el color que tendr�n las letras del item del men� que
#no hemos seleccionado
COLOR_ITEM_NO_SELECCIONADO = (76, 15, 2)

#Definimos aqu� el color que tendr�n las letras del item del men� que
# hemos seleccionado
COLOR_ITEM_SELECCIONADO = (164, 68, 1)

#Al tener que comparar los valores de las cartas entre s�, pero tener
# cartas como la SOTA, CABALLO y REY que no son num�ricos aunque tienen
# una escala de valor, no podemos comparar directamente el valor de una 
# carta con otra, para ello hemos generado los siguientes m�todos

# Este convierte un n�mero al String correspondiente al numero de la carta7
# que usaremos en la clase CartaBaraja
def convertir_Num_A_Carta(num):
    #Para ello generamos una estructura de ifs anidados, especificando
    # los casos en los que hay que cambiar el valor num�rico por otro
    # string distinto (1 por AS, 10 por SOTA..) y devolvemos directamente
    # el string. Tambi�n ponemos un elif que controle el caso en que los 
    # valores no sean correctos y lanzamos nuestra pantalla de error en ese
    # caso. Finalmente solo quedan los casos en los que solo habr� que
    # convertir el int de num a string y lo devolvemos tambi�n
    if num == 1:
        return "AS"
    elif num == 10:
        return "SOTA"
    elif num == 11:
        return "CABALLO"
    elif num == 12:
        return "REY"
    elif num > 12 or num < 0:
        pantallaError = PantallaError(r"Error {0} no es un valor v�lido de carta".format(num))
        pantallaError.mostrarPantallaError()
        sys.exit()
    else:
        return str(num)

#Este m�todo hace el proceso opuesto al anterior, dado el string n�mero
# de la clase CartaBaraja nos devuelve el valor num�rico asociado
# En este caso, asociamos el 10 a la SOTA, el 11 al CABALLO y el 12 al REY
# tal y como viene haci�ndose tradicionalmente. Esto en realidad solo lo
# usaremos para poder comparar cartas en cada ronda del juego
def convertir_Carta_A_Num(carta):
    #Igual que antes generamos una estructura de ifs anidada donde
    # primero ponemos el casos donde no podemos convertir directamente
    # el string a int y luego mediante un else controlamos el resto de
    # casos. Es importante en ese �ltimo caso que controla todos los
    # casos en los que se puede hacer la conversi�n directamente, el crear
    # una estructura try y except donde controlemos el proceso de conversi�n
    # de string a int. Puesto que a ese caso llegar� cualquier string
    # que no sea AS, SOTA, CABALLO y REY, por lo que podr�a resultar
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
            #Ante cualquier excepci�n, primero imprimimos por 
            #consola un log del error
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Ha ocurrido la siguiente excepci�n: {0}".format(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            
            pantallaError = PantallaError(r"Error {0} no es un valor v�lido de carta".format(carta))
            pantallaError.mostrarPantallaError()
            sys.exit()  

#Todas nuestras cartas estar�n asociadas a una imagen que sea la que
# sea mostrada por pantalla cuando salgan elegidas en la baraja.
#Este m�todo realiza la conversi�n entre el palo y valor de la carta
# y la ruta relativa a la imagen
def convertir_Carta_A_Ruta(palo,carta):
    #Como las cartas est�n nombradas por n�meros del 1 al 12 y las cartas
    # de cada palo est�n en una carpeta distinta
    # Convertimos el valor de la carta a num�rico
    num = convertir_Carta_A_Num(carta)
    # Componemos la ruta a ese carta: RUTA_CARTAS es donde se encuentra
    # la carpeta principal, luego en palo estar�n las im�genes de las cartas
    # de cada palo y el �ltimo trozo es simplemente el n�mero de cada una
    # que es como se llaman + jpg que es el formato en que se encuentran
    ruta = RUTA_CARTAS + "/" + palo + "/" + "{0}.jpg".format(num) 
    return ruta

#Este m�todo procesa la respuesta que genera el evento del interacci�n
# del usuario cuando en la clase MenuInicial selecciona una opci�n
# En este caso utilizamos la asignaci�n de valores por defecto a par�metros
# de entrada para el par�metro screen           
def procesarRespuestaMenu(i,screen = None):
    #En este caso generamos una estructura de ifs aninados
    # Solo hay tres valores posibles
    # Caso el usuario elige el primer item, significa que el usuario
    # quiere jugar una partida
    if i == 0:
        #Llamamos al m�todo controladorPartida que gestiona todos
        # los eventos necesario para generar esa partida
        controladorPartida(screen)
    elif i == 1:
        Estadisticas.generarGraficoEstadisticas(Estadisticas.RUTA_FICHERO_CSV)
    elif i == 2:
        #En caso de seleccionar Salir, simplemente detenemos la ejecuci�n
        sys.exit()
    else:
        #Controlamos por si acaso el caso en que llegara un valor inv�lido
        # y mostramos la pantalla de error
        pantallaError = PantallaError(r"Error con los items del men�")
        pantallaError.mostrarPantallaError()
        sys.exit() 

def controladorPartida(screen = None):
    #Generamos un objeto MesaJuego que contiene todos los m�todos
    # para que realicemos la partida para el usuario
    mesaJuego = MesaJuego(screen)
    #Llamos al m�todo prepararCartasPrimeraRonda que hace varias cosas
    # Baraja las cartas y genera la animaci�n de barajado
    # Genera el pop-up para pedir al usuario que introduzca un valor
    # por el teclado para cortar la baraja y corta la baraja por ah�
    mesaJuego.prepararCartasPrimeraRonda()
    #Como cada partida tiene 5 ronda, usarmos un bucle for
    # que genere 5 iteraciones (de ah� el range(0,5)
    for i in range(0,5):
        #En cada ronda, debemos llamar a este m�todo
        #animacionPapete encapsula la sacada de carta de la baraja
        # para el usuario, luego la del ordenador y la animaci�n
        # en como se presenta el usuario
        marcador = mesaJuego.animacionPapete()
        # Una vez la animaci�n para mostramos el r�tulo de la
        # ronda actual, usando este m�todo
        mesaJuego.rotuloRonda(i+1)
    
    #Cuando salimos del bucle for, implica que ya se han terminado
    # todas las rondas, por lo que ya hemos terminado la partida
    # Ya solo queda anunciar al usuario quien ha ganado
    # Para ello, generamos un objeto de la clase ResultadoPartida
    # que controla la pantalla de resultados
    pantallaResultado = ResultadoPartida(screen)
    #Y llamamos al m�todo PantallaResultado que es el controlador de
    # esa pantalla
    datarowPartida = pantallaResultado.PantallaResultado(marcador)
    #Como hemos terminado la ronda, actualizamos el csv
    for datarowRonda in mesaJuego.datacsv:
        Estadisticas.anadirNuevoRegistro(Estadisticas.RUTA_FICHERO_CSV,datarowRonda)
    #Limpiamos el objeto auxiliar donde guardamos los registros
    #para el csv ya que hemos terminado la ronda, para la siguiente
    mesaJuego.datacsv.clear()
    Estadisticas.anadirNuevoRegistro(Estadisticas.RUTA_FICHERO_CSV,datarowPartida)
