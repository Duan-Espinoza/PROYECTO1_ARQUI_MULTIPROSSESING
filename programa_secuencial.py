"""
Instituto Tecnológico de Costa Rica
Escuela de Ingeniería en Computación - Sede San Carlos
Curso de Arquitectura de Computadoras 

Proyecto 1 - Multiprocesamiento
Profesor: Luis Diego Gómez Rodríguez

Código de la Solucion Secuencial

Estudiantes:
    Josué Chaves Araya 
    Duan Espinosa Olivares
    Valentín Tissera Doncini 

II Semestre 2022
"""

import os
from PIL import Image
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time

pathImagenes = os.path.join(os.getcwd(), "imgs")
pathImagenesBase = os.path.join(os.getcwd(), "Imagenes_base")
pathResultado = os.path.join(os.getcwd(), "resultado")
newSize = 50


def secuencial():
    """Funcion Main que ejecuta las funciones secualmente 


    Return
    ----------
    Guarda una Imagen Collage en la carpeta "resultado"

    """
    directorioImagenes  = cargarFileNames(pathImagenes)
    
    #Cambio de Tamaño
    print("Resize de Imágenes - Secuencial")
    inicioTiempo= time.time()    
    imagenesModificadas = cambioTamannoImg(directorioImagenes, pathImagenes)
    tiempoReduccionImagenes = time.time() - inicioTiempo

    #Cálculo del Promedio
    print("Promedios RGB - Secuencial")
    inicioTiempo= time.time()    
    diccionarioRGB, diccionarioImagenes = valorRGB(imagenesModificadas)
    tiempoCalculoPromedios = time.time() - inicioTiempo

    #Creación del collage
    print("Collage - Secuencial")
    inicioTiempo= time.time()    
    collage = realizarCollageImg(diccionarioImagenes, diccionarioRGB, pathImagenesBase)
    tiempoCollage = time.time() - inicioTiempo

    #Guardar Imagen 
    pathCollage = os.path.join(os.getcwd(), "resultado/resultado.jpg") 
    collage.save( pathCollage )

    tiempoTotal = tiempoReduccionImagenes + tiempoCalculoPromedios + tiempoCollage
    print(f'\n\nTiempos para ejecución Secuencial: \n - Redu Ima: {tiempoReduccionImagenes} \n - Prom RGB: {tiempoCalculoPromedios} \n - Proc Col: {tiempoCollage} \n - Total   : {tiempoTotal}')
    

    



def cargarFileNames(pathCarpeta):    
    """Carga los nombres de los archivos que existen dentro de un directorio
    Solo carga los nombres de archvios en formato .jpg

    Parameters
    ----------
    pathCarpeta : str
        Path del directorio con los archivos a enlistar

    Return
    ----------
    listaFilenames: list
        Lista con los nombres de los archivos dentro de una carpeta 

    Si la ruta no es válida, entonces retoirna lista vacía
    """

    # print("------ Cargando FileNames de las Imagenes")

    if verificarRuta(pathCarpeta)==False:
        print("Ruta no válida")
        return []
    else:
        archivos = os.listdir(pathCarpeta)
        listaFilenames=[]
        for archivo in archivos:
            if os.path.isfile(os.path.join(pathCarpeta, archivo)) and archivo.endswith('.jpg'):
                listaFilenames.append(archivo)
                
        # print(f'Hay {len(listaFilenames)} imagenes en la carpeta')
        
        return listaFilenames


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
    # print("------ Verificando Path")

    if os.path.exists(ruta):
        return True
    else:
        return False


def cambioTamannoImg(listaNombreImagenes,pathCarpetaImagen):
    """Cambia el tamaño de las imagenes 

    Parameters
    ----------
    directorio: List
        Lista de nombres de las imagenes del folder
    ruta : str
        Ruta la cual se va a verificar su validez.
    """
    # print("------ Cambiando el size de las imagenes")
    listaImagenes=[]
    for x in listaNombreImagenes:
        im = Image.open(os.path.join(pathCarpetaImagen, x),"r")
        newsize = (newSize, newSize)
        im1 = {'imagen':im.resize(newsize), 'nombre':x, 'promRGB':0}

        listaImagenes.append(im1)

    return listaImagenes

def valorRGB(diccionarioInfoImagen):
    """Calcula el valor promedio RGB de cada imagen 

    Parameters
    ----------
    diccionarioInfoImagen: Dictionary[:]
        Diccionario con información de cada imágen 

    Return
    ----------
    diccionarioPromedios: Diccionario
        Valores promedios de RGB de cada imagen 
    diccionarioImagenes: Diccionario
        Diccioanrio de imagenes 

    """
    # print("------ Calculando el Promedio RGB")
    diccionarioPromedios = {}
    diccionarioImagenes = {}


    for x in diccionarioInfoImagen:
        arr = np.array(x['imagen']) # Vamos a convertir la imagen en un arreglo
        
        arr_mean = np.mean(arr, axis=(0,1))
        rgb = 0
        listaRGB = []

        if(arr.ndim != 3):
            nombreImagen = x['nombre']

            # {'128,250,74':<imagen>, '123,345,432':<imagen2>, }
            # [12825074, 123345432, 886878687]
            rgb = f'{int(arr_mean)}{int(arr_mean)}{int(arr_mean)}'
            listaRGB = [arr_mean,arr_mean,arr_mean]

        else:
    
            rgb = f'{int(arr_mean[0])}{int(arr_mean[1])}{int(arr_mean[2])}'
            listaRGB = [int(arr_mean[0]), int(arr_mean[1]),int(arr_mean[2])]

        diccionarioPromedios[rgb] = listaRGB
        diccionarioImagenes[rgb] = x['imagen']

    return diccionarioPromedios, diccionarioImagenes

def menuSeleccionImagenBase( listaImagenes ):
    """Despliega un menu para que el usuario elija la imagen base

    Parameters
    ----------
    listaNombresImagenes: List
        Lista de con los nombres de las imagenes base 

    Return
    ----------
    El nombre de la imagen seleccioanda
       
    """
    print("*****Seleccione la Imagen Base ******\n")

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
   

def realizarCollageImg(diccionarioImagenes, diccionarioPromedios, pathImagenesBase):
    """Crea el collage de la Imagen Base 
    Parameters
    ----------
    diccionarioImagenes: List[R,G,B]
        Diccionario con la informaciond de las imagenes 
    
    pathImagenesBase: string
        Path del directorio con las imagenes base
    
    diccionarioPromedio: 
        Diccionario con los promedios RGB de las imagenes pequenias 

    Return
    ----------
    Objeto de tipo imagen con el collage de la imagen base creada en base a las imagenes de tamano reducido 
    """
    # print("------ Realizando el Collage")

    imagenesBase = cargarFileNames(pathImagenesBase)
    imagenSeleccionada = menuSeleccionImagenBase(imagenesBase)

    #Imagen Base
    img = Image.open(os.path.join(pathImagenesBase, imagenSeleccionada),"r")
    imgWidth, imgHeight = img.size

    #Creacion del canvas 
    #Si la imagen base es de 20 x 20 y cada imagen chiquitica es de 15x15 el nuevo size del canvas
    # va a ser width(20*15) x height(20x15)
    canvasCollage = Image.new(mode="RGB", size=(imgWidth*newSize, imgHeight*newSize))

    #Carga la informacion de los pixeles de la imagen Base
    pixel = img.load()

    # Va columan por columna, de arriba hacia abajo, empezando con la columna de la izquiera de la img
    for x in range(img.width):
        for y in range(img.height):
            color = pixel[x, y]

            #Encuentra el key con el RGB más parecido al Pixel 
            key = buscarPixel(color, diccionarioPromedios)
            #Toma la imagen con ese Key y lo pega en el Canvas
            canvasCollage.paste(diccionarioImagenes[key], (x*newSize, y*newSize) )

    return canvasCollage



def buscarPixel(pixel, dicProm):
    """Busca el pixel dentro del diccionario de Promedios para seleccionar la imagen más parecida al RGB del Pixel 

    Parameters
    ----------
    pixel: List[R,G,B]
        Lista con los valores RGB del pixel que se está procesando de la imagen base
    
    diccProm: Diccionario
        Diccionario con los promedios RGB de las imagenes pequenias 

    Return
    ----------
    El Key con el RGB más parecido al del Pixel 
    """

    R = pixel[0]
    G = pixel[1]
    B = pixel[2]

    keyMenor = ""
    promMenor = 0

    for key, value  in dicProm.items():
        
        prom = (abs(value[0] - R) + abs(value[1] - G) + abs(value[2] - B))//3

        if (keyMenor == ""):
            keyMenor = key
            promMenor = prom

        if prom < promMenor:
            promMenor = prom 
            keyMenor = key
    
    return keyMenor

        




        
    
