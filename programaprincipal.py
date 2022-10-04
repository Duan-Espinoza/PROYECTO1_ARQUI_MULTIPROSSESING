#Proyecto 1 Arquitectura Computadores
#Estudiantes:
#Duan Antonio Espinoza
#Josue Daniel Chaves Araya
#Profesor: Luis Diego Gomez Rodriguez
#Collage de imagenes

import PIL
import multiprocessing as mp

#Descripción: Serie de prints que muestran las opciones disponibles
#del menú principal
#E: Digito
#S: Menu seleccionado
#R: Solo valor numérico entero
def menuPrincipal():
    print("*****Collage de imagenes******\n")
    print("Opcion 1: Cambio del tamaño de las imágenes")
    print("Opcion 2: Sacar el valor promedio de las imágenes")
    print("Opcion 3: Realizar Collage de Imágenes\n")
    try:
        opcion=int(input("Digite su opcion:"))
    except:
        print("Opción no válida\n")
        return menuPrincipal()

    if opcion==1:
        pass
    if opcion==2:
        pass
    if opcion==3:
        pass
    else:
        print("Opción no válida\n")
        return menuPrincipal()

#
#
#
def cambioTamannoImg():
    pass


def valorPromedioImg():
    pass

#
#
#
def realizarCollageImg():
    pass








    
    
    
