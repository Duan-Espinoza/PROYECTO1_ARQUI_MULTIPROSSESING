#Proyecto 1 Arquitectura Computadores
#Estudiantes:
#Duan Antonio Espinoza
#Josue Daniel Chaves Araya
#Profesor: Luis Diego Gomez Rodriguez
#Collage de imagenes


#Librerias necesarias
from operator import truediv
import os
from PIL import Image
import multiprocessing as mp
import numpy as np

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
        return cargaImagenes()
    if opcion==2:
        pass
    if opcion==3:
        pass
    else:
        print("Opción no válida")
        return menuPrincipal()



#E:
#S:
#R:
def cargaImagenes():
    ruta=input("Escriba la ruta de la carpeta con las imágenes:")
    
    if verificarRuta(ruta)==False:
        print("Ruta no válida")
    else:
        elementos = os.listdir(ruta)
        directorio=[]
        for fichero in elementos:
            if os.path.isfile(os.path.join(ruta, fichero)) and fichero.endswith('.jpg'):
                directorio.append(fichero)
                
        print(len(directorio))
        
        return cambioTamannoImg(directorio,ruta)

#Función que verifica la existencia de un directorio
#E: String
#S: Valor booleano
#R: ...................
def verificarRuta(ruta):
    if os.path.exists(ruta):
        return True
    else:
        return False

#
#
#
def cambioTamannoImg(directorio,ruta):
    lista=[]
    for x in directorio:
        im = Image.open(ruta+"\\"+x,"r")
        newsize = (10, 10)
        im1 = im.resize(newsize)
        lista.append(im1)
    print(directorio)
    return valorRGB(lista)

#
#
#
def valorRGB(lista):
    print("test")

    for x in lista:
        arr = np.array(x)
        arr_mean = np.mean(arr, axis=(0,1))

        print(arr_mean)
        
        #print(f'[R={arr_mean[0]:.1f},  G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f} ]')

#C:\Users\Usuario\Desktop\8 semestre\Arquitectura computadores\Proyecto 1\Fotomosaico\PROYECTO1_ARQUI_MULTIPROSSESING\imgs










def valorPromedioImg():
    pass

#
#
#
def realizarCollageImg():
    pass






menuPrincipal()

    
    
    
