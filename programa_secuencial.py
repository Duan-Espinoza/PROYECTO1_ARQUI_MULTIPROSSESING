

import os
from PIL import Image
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time


pathImagenes = os.path.join(os.getcwd(), "imgs")
pathImagenesBase = os.path.join(os.getcwd(), "Imagenes_base")
pathResultado = os.path.join(os.getcwd(), "resultado")
newSize = 30


def Secuencial():
    directorioImagenes  = cargaImagenes(pathImagenes)
    imagenesModificadas = cambioTamannoImg(directorioImagenes, pathImagenes)
    diccionarioRGB = valorRGB(imagenesModificadas)
    realizarCollageImg(diccionarioRGB, pathImagenesBase, pathResultado)


#E:
#S:
#R:
def cargaImagenes(pathCarpeta):
    """

    """
    print("------ Cargando Lista de Imagenes")

    ruta = pathCarpeta

    if verificarRuta(ruta)==False:
        print("Ruta no válida")
    else:
        elementos = os.listdir(ruta)
        directorio=[]
        for fichero in elementos:
            if os.path.isfile(os.path.join(ruta, fichero)) and fichero.endswith('.jpg'):
                directorio.append(fichero)
                
        print(f'Hay {len(directorio)} imagenes en la carpeta')
        
        return directorio


def verificarRuta(ruta):
    """Verifica la existencia de un directorio
    Si el directorio no es encontrado retorna falso

    Parameters
    ----------
    ruta : str
        Ruta la cual se va a verificar su validez.

    Return
    ----------
    Valor booleano
        True: Si encuentra la ruta
        False: Si no la encuentra.

    """
    print("------ Verificando Path")

    if os.path.exists(ruta):
        return True
    else:
        return False


def cambioTamannoImg(directorio,ruta):
    """Cambia el tamaño de las imagenes 

    Parameters
    ----------
    directorio: List
        Lista de nombres de las imagenes del folder
    ruta : str
        Ruta la cual se va a verificar su validez.
    """
    print("------ Cambiando el size de las imagenes")
    listaImagenes=[]
    for x in directorio:
        im = Image.open(os.path.join(ruta, x),"r")
        newsize = (newSize, newSize)
        im1 = {'imagen':im.resize(newsize), 'nombre':x, 'promRGB':0}

        listaImagenes.append(im1)

    return listaImagenes

diccionarioImagenes = {}
diccionarioPromedios = {}

def valorRGB(lista):
    """Calcula el valor promedio RGB de cada imagen 

    Parameters
    ----------
    lista: Dictionary[:]
        Diccionario con información de cada imágen 
    """
    print("------ Calculando el Promedio RGB")


    for x in lista:
        arr = np.array(x['imagen']) # Vamos a convertir la imagen en un arreglo
        
        arr_mean = np.mean(arr, axis=(0,1))

        if(arr.ndim != 3):
            nombreImagen = x['nombre']
            #print(f'Imagen {nombreImagen} tiene {arr.ndim} dimensiones, el shape es: {arr.shape}, el promedio RGB es de {arr_mean}')

            # {'128,250,74':<imagen>, '123,345,432':<imagen2>, }

            # {'128,250,74':<imagen>, '123,345,432':<imagen2>, }
            # [12825074, 123345432, 886878687, 98168761847]

            rgb = f'{int(arr_mean)}{int(arr_mean)}{int(arr_mean)}'

            "255255255"
            
            
            listaRGB = [arr_mean,arr_mean,arr_mean]

            diccionarioImagenes[rgb] = x['imagen']
            diccionarioPromedios[rgb] = listaRGB

            #Muestra la Imagen 
            # plt.imshow(x['imagen'])
            # plt.show()
            #x['imagen'].show()
        else:

            # print(f'[R={int(arr_mean[0])},  G={int(arr_mean[1])}, B={int(arr_mean[2])} ]')
            # El valor RGB
            

            rgb = f'{int(arr_mean[0])}{int(arr_mean[1])}{int(arr_mean[2])}'

            listaRGB = [int(arr_mean[0]), int(arr_mean[1]),int(arr_mean[2])]

            diccionarioPromedios[rgb] = listaRGB
            diccionarioImagenes[rgb] = x['imagen']



    #print("------ Imprimiendo el diccionario")
    return diccionarioImagenes

def menuSeleccionImagenBase( listaImagenes ):
    print("*****Seleccione la Imagen a procesar******\n")

    for iterador, imagen in enumerate(listaImagenes):
        print(f'Opcion {iterador + 1}: {imagen}')

    print(" ")        
    try:
        opcion=int(input("Digite su opcion:"))
    except:
        print("Opción no válida\n")
        return menuSeleccionImagenBase(listaImagenes)

    if ( opcion > 0 and opcion <= len(listaImagenes)):
        print(f'Imagen {opcion} seleccionada')
        return (listaImagenes[opcion - 1 ])
    else:
        print("Opción no válida")
        return menuSeleccionImagenBase(listaImagenes)
   

def realizarCollageImg(diccionarioImagenes, pathImagenesBase, pathResultado):
    """

    Parameters
    ----------

    """
    print("------ Realizando el Collage")

    imagenesBase = cargaImagenes(pathImagenesBase)
    imagenSeleccionada = menuSeleccionImagenBase(imagenesBase)

    #Imagen Base
    img = Image.open(os.path.join(pathImagenesBase, imagenSeleccionada),"r")
    imgWidth, imgHeight = img.size

    #Creacion del canvas 
    #Si la imagen base es de 20 x 20 y cada imagen chiquitica es de 15x15 el nuevo size del canvas
    # va a ser width(20*15) x height(20x15)
    im_bg = Image.new(mode="RGB", size=(imgWidth*newSize, imgHeight*newSize))

    pixel = img.load()
    res = []

    # Va columan por columna, de arriba hacia abajo, empezando con la columna de la izquiera de la img
    for x in range(img.width):
        for y in range(img.height):
            color = pixel[x, y]
            # print( f'R:{color[0]}, G:{color[1]}, B{color[2]}')

            key = buscarPixel(color)
            
            # diccionarioImagenes[key].show()

            
            im_bg.paste(diccionarioImagenes[key], (x*newSize, y*newSize) )
            
            
            # newKeyRGB = f'{color[0]},{color[1]},{color[2]}'
            # newKeyRGB = f'{prom}'
            #diccionario tiene= '12,12,12' osea 'r,g,b'
            #print(diccionarioImagenes[newKeyRGB])


                
            # promedio = color[0] + color[1] + color[2]

            # promedio = promedio // 3
            # pixel[x, y] = (promedio, promedio, promedio)
    print(res)
    im_bg.show()


def buscarPixel(pixel):
    
    R = pixel[0]
    G = pixel[1]
    B = pixel[2]

    keyMenor = ""
    promMenor = 0

    for key, value  in diccionarioPromedios.items():
        
        prom = (abs(value[0] - R) + abs(value[1] - G) + abs(value[2] - B))//3

        if (keyMenor == ""):
            keyMenor = key
            promMenor = prom

        if prom < promMenor:
            promMenor = prom 
            keyMenor = key
    
    return keyMenor

        




        
    
