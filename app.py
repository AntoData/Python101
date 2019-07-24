# coding: latin-1
'''
Created on 30 abr. 2019
Propuesta 2 (con complicaciones adicionales explicadas en informe)
@author: Antonio P�rez Oviedo
Librer�as extra:
- pygame (1.9.6): para la interfaz gr�fica
M�dulos propios usados:
- MenuInicial: que es el controlador de la pantalla inicial del juego
- Pantalla: que es una clase padre que controla la configuraci�n de la ventana/pantalla del juego
- Utiles: m�dulo con diversos m�todos para gestionar correctamente aspectos de la baraja y las cartas
'''
import pygame
import Front.MenuInicial as MenuInicial
from Front.Pantalla import Pantalla
import Cartas.Utiles as Utiles

#Definimos el m�todo main que ser� por donde deber� empezar la ejecuci�n del programa
#por tanto siempre debemos ejecutar este fichero
def main():
    #Iniciamos pygame
    pygame.init()
    #Generamos una pantalla
    pantalla = Pantalla()
    
    #Generamos bucle infinito para que el programa este en ejecuci�n
    #hasta que cerremos la ventana
    while True:
        #Iniciamos la pantalla
        screen = pantalla.iniciarPantalla(900, 700, "A la carta m�s alta")
        #Generamos el men� inicial
        menu = MenuInicial.MenuInicial(screen)
        #Lo mostramos y estamos pendientes del item escogido
        i = menu.menuInicial()
        #Procesamos la respuesta
        Utiles.procesarRespuestaMenu(i,screen)
        #Cuando hayamos terminado, al ser un bucle infinito
        #volveremos a ejecutar los m�todos anteriores y
        #volveremos al men� de inicio, evitando recursividad

    pygame.display.flip()
    
    
#Definimos el main               
if __name__ == '__main__':
    main()