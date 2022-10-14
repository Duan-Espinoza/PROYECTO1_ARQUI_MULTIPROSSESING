from operator import truediv
import os
from PIL import Image
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time

def rutasCarpetaImagenes():
    print("*****Elija la Ruta ******")
    print("1. Duan ")
    print("2. Josue ")
    print("3. Valen ")
    try:
        opcion=int(input("Digite su opcion:"))
    except:
        print("Opción no válida\n")
        return rutasCarpetaImagenes()
    if opcion==1:
        return r'C:\Users\Usuario\Desktop\8 semestre\Arquitectura computadores\Proyecto 1\Fotomosaico\PROYECTO1_ARQUI_MULTIPROSSESING\imgs'
    if opcion==2:
        return r'/Users/d4n11083/Desktop/Repositorios/PROYECTO1_ARQUI_MULTIPROSSESING/imgs'
        #return r'/Users/gilda/Desktop/Repositorios/Proyecto_1_Arqui/PROYECTO1_ARQUI_MULTIPROSSESING/imgs'
    if opcion==3:
        pass
    else:
        print("Opción no válida")
        return rutasCarpetaImagenes()

#E:
#S:
#R:
def cargaImagenes():
    # ruta=input("Escriba la ruta de la carpeta con las imágenes:")
    ruta = rutasCarpetaImagenes()

    if verificarRuta(ruta)==False:
        print("Ruta no válida")
    else:
        elementos = os.listdir(ruta)
        directorio=[]
        for fichero in elementos:
            if os.path.isfile(os.path.join(ruta, fichero)) and fichero.endswith('.jpg'):
                directorio.append(fichero)
                
        print(f'Hay {len(directorio)} imagenes en la carpeta')
        
        return cambioTamannoImg(directorio,ruta)

#Función que verifica la existencia de un directorio
#E: String
#S: Valor booleano
#R: ...................
def verificarRuta(ruta):
    print("------ Verificando Path")

    if os.path.exists(ruta):
        return True
    else:
        return False

#Función que cambia el tamaño de las imagenes 
#E directorio: [] Lista de nombres de las imagenes del folder
#E ruta: string Path del directorio 
#S
def cambioTamannoImg(directorio,ruta):
    print("------ Cambiando el size de las imagenes")
    listaImagenes=[]
    for x in directorio:
        im = Image.open(os.path.join(ruta, x),"r")
        newsize = (15, 15)
        im1 = {'imagen':im.resize(newsize), 'nombre':x, 'promRGB':0}

        listaImagenes.append(im1)
    return valorRGB(listaImagenes)



diccionarioImagenes = ""

# Calcula el valor promedio RGB de cada imagen 
#E lista: diccionario Lista de diccionario con información de cada imágen 
#
def valorRGB(lista):
    print("------ Calculando el Promedio RGB")

    for x in lista:
        arr = np.array(x['imagen']) # Vamos a convertir la imagen en un arreglo
        
        arr_mean = np.mean(arr, axis=(0,1))

        if(arr.ndim != 3):
            nombreImagen = x['nombre']
            print(f'Imagen {nombreImagen} tiene {arr.ndim} dimensiones, el shape es: {arr.shape}, el promedio RGB es de {arr_mean}')
            #Muestra la Imagen 
            # plt.imshow(x['imagen'])
            # plt.show()
            #x['imagen'].show()
        else:
            print(f'[R={arr_mean[0]:.1f},  G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f} ]')


def valorPromedioImg():
    pass

#
#
#
def realizarCollageImg():
    pass




    
    
    