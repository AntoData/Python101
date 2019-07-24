# coding: latin-1
'''
Created on 23 may. 2019

Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pandas (0.24.2): para la gesti�n del csv donde almacenamos los datos de las partidas
y tambi�n para realizar los c�lculos
- matplotlib (3.1.0): para representar los datos estad�sticos gr�ficamente
Librer�as est�ndar:
- os: para comprobar si existe el fichero de csv
'''
import pandas as pd
import os
import matplotlib.pyplot as plt

"""
Este m�dulo es el que contiene losm m�todos que usaremos
para captar los datos estad�sticos que nos interesan
de la ejecuci�n del programa y convertirlos en csv
para luego poder recuperarlos y generar representaciones
gr�ficas de esos datos
"""

RUTA_FICHERO_CSV = "./data.csv"
#Hemos generador este decorador para la funci�n que a�ade nuevos
#registros a nuestro fichero csv. Este funci�n genera
#un nuevo fichero csv en caso de que nuestro fichero no exista
def decoradorGenerarFicheroEstadisticas(func):
    def envoluraGenerarFicheroEstadisticas(ruta, dataRow):
        #Si el fichero csv no existe, lo generamos con sus cabeceras
        if not os.path.isfile(ruta):
            data = {"T":[],"G":[],"CPJ":[],"CPO":[]}
            #Construimos el data frame con las cabeceras
            frame = pd.DataFrame(data)
            #A trav�s del data frame generamos el fichero csv
            #es importante se�alar que no queremos que genere
            #�ndices para el fichero, por ello usamos index = False
            frame.to_csv(ruta,index=False)
        func(ruta,dataRow)
    return envoluraGenerarFicheroEstadisticas

#Este m�todo junto con su decorador generar� un nuevo fichero csv
#en caso de no existir y a�adir� un nuevo registro al fichero csv
@decoradorGenerarFicheroEstadisticas
def anadirNuevoRegistro(ruta,dataRow):
    #Leemos el fichero csv actual
    frame = pd.read_csv(ruta)
    #A�adimos el nuevo registro al data frame
    frame = frame.append(dataRow,ignore_index=True)
    #Convertimos el data frame a csv otra vez para as� guardar los
    #nuevos datos
    frame.to_csv(ruta,index=False) 

#Este m�todo genera un data series con el porcentaje
#de partidas ganadas por el jugador, el ordenador y cual
#porcentaje de las partidas terminaron en empate
def calcularPorcentajePartidasGanadas(ruta):
    #Leemos el fichero csv y obtenemos el data frame
    data = pd.read_csv(ruta)
    #Filtramos por T=='P' es decir, tipo de registro, partida
    dataPartidas = data.query("T=='P'")
    #Contamos cuantas partidas hay registradas
    partidasTotales = dataPartidas.count()["T"]
    #Contamos cuantas partidas T=='P' hay ganadas por el jugador
    #G == 'J' es ganador == jugador
    partidasGanadasJugador = dataPartidas.query("T=='P' & G=='J'").count()["G"]
    #Contamos cuantas partidas T=='P' hay ganadas por el ordenador
    #G == 'O' es ganador == ordenador 
    partidasGanadasOrdenador = dataPartidas.query("T=='P' & G=='O'").count()["G"]
    #Si partidasTotales==0, es que no hemos guardado partidas
    #aun en el fichero csv, por lo tanto debemos iniciar
    #los par�metros con los que construimos el data series a 0
    #para que en el m�todo que representa este gr�fico
    #pueda imprimir algo coherente
    if partidasTotales==0:
        porcentajeGanadasJugador = 0
        porcentajeGanadasOrdenador = 0
        porcentajeEmpate = 0
    else:
        #En caso contrario calculamos los porcentajes
        porcentajeGanadasJugador = (partidasGanadasJugador*100)/partidasTotales
        porcentajeGanadasOrdenador = (partidasGanadasOrdenador*100)/partidasTotales
        porcentajeEmpate = 100 - (porcentajeGanadasJugador+porcentajeGanadasOrdenador)
    #Construimos el data series para poder pintar el gr�fico luego
    porcentaje = pd.Series([porcentajeGanadasJugador,porcentajeGanadasOrdenador,porcentajeEmpate],index = ["Jugador","Ordenador","Empate"])
    #Devolvemos el data series para as� poder luego pintarlo junto
    #con otras series
    return porcentaje

#Este m�todo calcula las partidas totales ganadas por el usuario
#por el ordenador y cuales han quedado empate
def totalesPartidas(ruta):
    #Leemos el fichero csv para obtener un data frame
    data = pd.read_csv(ruta)
    #Filtramos para obtener solo registros de partidas
    #T=='P' significa tipo == Partida
    dataPartidas = data.query("T=='P'")
    #Contamos las partidas totales
    partidasTotales = dataPartidas.count()["T"]
    #Obtenemos el total de partidas ganadas por el jugador G == 'J'
    #ganador == jugador
    partidasGanadasJugador = dataPartidas.query("T=='P' & G=='J'").count()["G"]
    #Obtenemos el total de partidas ganadas por el ordenador G == 'O'
    #ganador == ordenador
    partidasGanadasOrdenador = dataPartidas.query("T=='P' & G=='O'").count()["G"]
    #El resto ser�n las partidas que quedaron empates
    partidasGanadasEmpatadas = partidasTotales - (partidasGanadasJugador+partidasGanadasOrdenador)
    #Generamos una serie con estos datos
    totales = pd.Series([partidasGanadasJugador,partidasGanadasOrdenador,partidasGanadasEmpatadas],index = ["Jugador","Ordenador","Empate"])
    #Devolvemos la serie para que podamos representarla luego
    return totales

#Este m�todo calcula la media de puntos por partida
def mediaPuntosPorPartida(ruta):
    #Leemos el fichero csv para obtener un data frame con el que operar
    data = pd.read_csv(ruta)
    #Obtenemos todos los registros sobre resultados de partida
    #T == 'P' significa tipo de registro resultado de partida
    dataPartidas = data.query("T=='P'")
    #Contamos cuantas partidas se han jugado
    partidasTotales = dataPartidas.count()["T"]
    #Filtramos los datos obtenidos del csv para quedarnos solo
    #con los registros acerca de rondas para ello el filtro es
    #T=='R' que es tipo de registro resultado de ronda
    datosRondas = data.query("T=='R'")
    #Ahora dentro de los datos de rondas filtramos por ganador
    rondasGanadasJugador = datosRondas.query("G=='J'").count()["G"]
    rondasGanadasOrdenador = datosRondas.query("G=='O'").count()["G"]
    #Si las partidas totales son 0, la media de puntos debe ser 0
    if partidasTotales == 0:
        mediaPuntosJugador = 0
        mediaPuntosOrdenador = 0
    else:
        #En caso contrario calculamos la media
        mediaPuntosJugador = rondasGanadasJugador/partidasTotales
        mediaPuntosOrdenador = rondasGanadasOrdenador/partidasTotales
    #Para tener una comparativa, agregamos los puntos que hay en una partida
    puntosEnPartida = 5
    #Generamos una serie con estos datos
    medias = pd.Series([mediaPuntosJugador,mediaPuntosOrdenador,puntosEnPartida],index = ["Media Ptos Jugador","Media Ptos Ordenador","Puntos En una Partida"])
    #Devolvemos la serie para que pueda representarse luego en un gr�fico
    return medias

#Este m�todo analiza qu� cartas han salido en las diferentes rondas
#y devolver� una serie con las 3 cartas que m�s han salido
def cartasMasFrecuentes(ruta):
    #Como siempre leemos el fichero csv para generar el data frame
    data = pd.read_csv(ruta)
    #Filtramos para obtener los registros que sean de rondas
    # T == 'P' significa tipo de registro es resultado de ronda
    dataRonda = data.query("T=='R'")
    n = 3
    #Nos filtramos para obtener una serie con las cartas
    #que han sacado jugador y ordenador en cada ronda
    cartasJugador = dataRonda['CPJ']
    cartasOrdenador = dataRonda['CPO']
    #Juntamos ambas series
    cartasPartidas = cartasJugador.append(cartasOrdenador)
    #Generamos un data frame donde contamos cuantas veces
    #aparece cada carta y nos quedamos solo con los 3 registros
    #que nos interesan
    cartasFrecuentes = cartasPartidas.value_counts()[:n]
    #Devolvemos el data frame para poder representarlo
    return cartasFrecuentes

#Este m�todo genera un gr�fico con 4 subplots donde representaremos
#cada uno de las series o data frames que hemos explicado anteriormente
def generarGraficoEstadisticas(ruta):
    #Comprobamos que exista el fichero y si no existe lo generamos
    if not os.path.isfile(ruta):
            data = {"T":[],"G":[],"CPJ":[],"CPO":[]}
            frame = pd.DataFrame(data)
            frame.to_csv(ruta,index=False)
    #Ejecutamos las funciones anteriores para obtener las
    #4 series o dataframes con los datos que queremos
    #representar
    gp = calcularPorcentajePartidasGanadas(ruta)
    gpt = totalesPartidas(ruta)
    gmp = mediaPuntosPorPartida(ruta)
    cmf = cartasMasFrecuentes(ruta)
    #Definimos un gr�fico con 4 subplots de un tama�o determinado
    fig, axs = plt.subplots(2,2,figsize = (50,20))
    #En la posici�n superior izquierda representamos
    #el porcentaje de partidas ganadas con un gr�fico de quesitos
    axs[0,0].pie(gp,labels=["Jugador","Ordenador","Empate"])
    #Le damos un t�tulo adecuado a este gr�fico
    axs[0,0].title.set_text("Porcentajes de partidas ganadas")
    #En la posici�n superior derecha representamos los totales
    #de partidas ganadas por el usuario, ordenador o que quedaron
    #empate en un gr�fico de barras y le damos t�tulo
    axs[0,1].bar(x=["Jugador","Ordenador","Empate"],height=gpt)
    axs[0,1].title.set_text("Partidas ganadas")
    #En la posici�n inferior izquierda representamos
    #la media de puntos por ronda del usuario y ordenador
    #en un gr�fico de barras y le damos t�tulo
    axs[1,0].bar(x=["Jugador","Ordenador","Partida"],height=gmp)
    axs[1,0].title.set_text("Media de puntos partida")
    #En la posici�n inferior derecha representamos las 3 cartas
    #m�s frecuentes en un gr�fico de barras y le damos t�tulo
    axs[1,1].bar(x=cmf.index,height=cmf)
    axs[1,1].title.set_text("Cartas m�s frecuentes")
    #Damos el t�tulo Estad�sticas a la ventana
    fig.canvas.set_window_title("Estad�sticas")
    #Mostramos la figura con los 4 gr�ficos
    plt.show()
