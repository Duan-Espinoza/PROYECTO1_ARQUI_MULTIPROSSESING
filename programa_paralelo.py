"""
Instituto Tecnológico de Costa Rica
Escuela de Ingeniería en Computación - Sede San Carlos
Curso de Arquitectura de Computadoras 

Proyecto 1 - Multiprocesamiento
Profesor: Luis Diego Gómez Rodríguez

Código de la Solucion Paralela

Estudiantes:
    Josué Chaves Araya 
    Duan Espinosa Olivares
    Valentín Tissera Doncini 

II Semestre 2022
"""
import ray
ray.init(num_cpus = 4)
print(ray.available_resources())

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time

pathImagenes = os.path.join(os.getcwd(), "imgs")
pathImagenesBase = os.path.join(os.getcwd(), "Imagenes_base")
pathResultado = os.path.join(os.getcwd(), "resultado")
tamanioPixel = 50


def paralelo():
    """Funcion Main que ejecuta las funciones paralelas 
    
    Parameters
    ----------

    Return
    ----------
    Guarda una Imagen Collage en la carpeta "resultado"

    """

    #Carga  los nombres de las imágenes dentro de la carptea de imgs
    fileNamesImagenes  = cargarFileNames(pathImagenes)
    
    #Cambio de Tamaño
    print("Resize de Imágenes - Paralelo")
    imagenesModificadas, tiempoReduccionImagenes = cambioTamanioImgParalelo(fileNamesImagenes, pathImagenes)
    
    #Cálculo del Promedio
    print("Promedios RGB - Paralelo")
    diccionarioPromRgb, diccionarioImgRGB, tiempoCalculoPromedios = valorRGBParalelizado(imagenesModificadas)

    #Creación del collage
    print("Collage - Paralelo")
    collage, tiempoCollage = realizarCollageImg(diccionarioImgRGB, pathImagenesBase, diccionarioPromRgb)

    #Guardar la Imagen
    pathCollage = os.path.join(os.getcwd(), "resultado/resultado.jpg") 
    collage.save( pathCollage )

    tiempoTotal = tiempoReduccionImagenes + tiempoCalculoPromedios + tiempoCollage
    print(f'\n\nTiempos para ejecución Paralela: \n - Redu Ima: {tiempoReduccionImagenes} \n - Prom RGB: {tiempoCalculoPromedios} \n - Proc Col: {tiempoCollage} \n - Total   : {tiempoTotal}')
   

def waitSec():
    time.sleep(0.0001)

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
    print("------ Cargando FileNames de las Imagenes")

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



@ray.remote
def minimizarImagen(nombreImagen,pathCarpetaImagen):
    """Cambia el tamaño de una imagen

    Parameters
    ----------
    nombreImagen: string
        Nombre del Archivo 
    pathCarpetaImagen : str
        Path de la carpeta que contiene la imagen
    Return
    ----------

    """
    imagen = Image.open(os.path.join(pathCarpetaImagen, nombreImagen),"r")
    tamanioImagen = (tamanioPixel, tamanioPixel)
    nuevaImagen = {'imagen':imagen.resize(tamanioImagen), 'nombre':nombreImagen, 'promRGB':0}
    return nuevaImagen


def cambioTamanioImgParalelo(listaNombresArchivos,pathCarpetaArchivos):
    """Cambia el tamaño de las imagenes 

    Parameters
    ----------
    directorio: List
        Lista de nombres de las imagenes del folder
    ruta : str
        Ruta la cual se va a verificar su validez.
    """
    # print("------ Cambiando el size de las imagenes")
    
    inicioReduccionImagenes = time.time()    
    listaImagenesTamanioReducido = ray.get([minimizarImagen.remote(archivo,pathCarpetaArchivos) for archivo in listaNombresArchivos])
    tiempoReduccionImagenes = time.time() - inicioReduccionImagenes

    return (listaImagenesTamanioReducido,tiempoReduccionImagenes)


@ray.remote
def obtenerRGB(infoImagen):
    """Calcula el valor promedio de una imagen

    Parameters
    ----------
    infoImagen: Dicionario con key=Nombre Imagen Value=<Image>
        Diccionario con la informacion de la imagen
    

    Return
    ----------
    rgb: string
        Valor RGB promedio de la imagen 
    listaRGB: list
        Lista con los valors R,G,B
    infoImagen:
        Imagen procesada

    """

    time.sleep(0.000001)

    arr = np.array(infoImagen['imagen']) # Vamos a convertir la imagen en un arreglo
    arr_mean = np.mean(arr, axis=(0,1))

    if(arr.ndim != 3):

        rgb = f'{int(arr_mean)}{int(arr_mean)}{int(arr_mean)}'
        listaRGB = [arr_mean,arr_mean,arr_mean]

    else:

        rgb = f'{int(arr_mean[0])}{int(arr_mean[1])}{int(arr_mean[2])}'
        listaRGB = [int(arr_mean[0]), int(arr_mean[1]),int(arr_mean[2])]

    return [rgb,listaRGB,infoImagen]
    
    
def valorRGBParalelizado( listaImagenesReducidas ):
    """Cambia el tamaño de las imagenes 

    Parameters
    ----------
    listaImagenesReducidas: List
        Lista de dicccionarios con información de cada imagen

    Return
    ----------
    diccionarioPromedios: Diccionario
        Diccionario de Promedios en donde key:ValorRGB Promedio, Value: Valores RGB
    diccionarioImagenes: Diciconario
        Diccionario de imagenes en donde key:ValorRGB, Value:Imagen
    """

    diccionarioPromedios = {}
    diccionarioImagenes = {}

    inicioPromedioRGB = time.time()    

    task_ids = [obtenerRGB.remote( infoImagen ) for infoImagen in listaImagenesReducidas]
    
    while len(task_ids) > 0:
        done_ids, task_ids = ray.wait(task_ids)
        result = ray.get(done_ids[0])

        diccionarioPromedios[result[0]] = result[1]
        diccionarioImagenes[result[0]] = result[2]['imagen']

    tiempoCalculoPromedios = time.time() - inicioPromedioRGB


    return [diccionarioPromedios,diccionarioImagenes, tiempoCalculoPromedios]


def menuSeleccionImagenBase( listaNombresImagenes ):
    """Desplieg un menu para que el usuario elija la imagen base

    Parameters
    ----------
    listaNombresImagenes: List
        Lista de con los nombres de las imagenes base 

    Return
    ----------
    El nombre de la imagen seleccioanda
       
    """
    print("***** Seleccione la Imagen Base ******\n")

    for iterador, imagen in enumerate(listaNombresImagenes):
        print(f'Opción {iterador + 1}: {imagen}')

    print(" ")        
    try:
        opcion=int(input("Digite su opción:"))
    except:
        print("Opción no válida\n")
        return menuSeleccionImagenBase(listaNombresImagenes)

    if ( opcion > 0 and opcion <= len(listaNombresImagenes)):
        print(f'Imágen {opcion} seleccionada')
        return (listaNombresImagenes[opcion - 1 ])
    else:
        print("Opción no válida")
        return menuSeleccionImagenBase(listaNombresImagenes)
   
@ray.remote
def buscarPixel(pixel, diccProm):
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

    for key, value  in diccProm.items():
        
        prom = (abs(value[0] - R) + abs(value[1] - G) + abs(value[2] - B)) // 3

        if (keyMenor == ""):
            keyMenor = key
            promMenor = prom

        if prom < promMenor:
            promMenor = prom 
            keyMenor = key

    return keyMenor


@ray.remote
def collageParalelo(pixel,columna,
                    height, 
                    diccIm,diccProm):

    """Busca el pixel dentro del diccionario de Promedios para seleccionar la imagen más parecida al RGB del Pixel 

    Parameters
    ----------
    pixel: np.array[[R,G,B]]
        Lista de pixeles de una columna de la imagen 

    columna: int
        Columna que se va a procesar 
    height: 
        Cantidad de filas dentro de la columna 

    diccIm: Diccionario
        Diccionario con la informaciond de las imagenes 

    diccProm: Diccionario
        Diccionario con los promedios RGB de las imagenes pequenias 

    Return
    ----------
    columna: int
        Columna que se esta procesando, para luego saber donde pegar esta columna en el background final

    imagenesColumna: lisa
        Lista con las imagenes de esa columna 
    """
    imagenesColumna = []
    time.sleep(0.000001)
    for y in range(height):
            color = pixel[y, columna]

            keyMenor = ""
            promMenor = 0

            for key, value  in diccProm.items():
                prom = (abs(value[0] - color[0]) + abs(value[1] - color[1]) + abs(value[2] - color[2])) // 3

                if (keyMenor == ""):
                    keyMenor = key
                    promMenor = prom

                if prom < promMenor:
                    promMenor = prom 
                    keyMenor = key

            imagenesColumna.append(  diccIm[keyMenor] )

    return (columna,imagenesColumna)


def realizarCollageImg(diccionarioImagenes, 
                        pathImagenesBase, 
                        diccionarioPromedio):

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

    nombresImagenesBase = cargarFileNames(pathImagenesBase)
    imagenSeleccionada = menuSeleccionImagenBase(nombresImagenesBase)

    #Imagen Base
    img = Image.open(os.path.join(pathImagenesBase, imagenSeleccionada),"r")
    imgWidth, imgHeight = img.size

    #Canvas del collage
    canvasCollage = Image.new(mode="RGB", size=(imgWidth*tamanioPixel, imgHeight*tamanioPixel))

    #Lista que tendrá las imagenes de cada columna 
    listaColumnas = [0] * imgWidth

    #Ray puts
    heightId = ray.put(imgHeight)
    pixelId = ray.put(np.array(img))
    diccImagenes = ray.put(diccionarioImagenes)
    diccPromedio = ray.put(diccionarioPromedio)

    inicioCollage = time.time()    

    task_ids = [collageParalelo.remote( pixelId, columna, heightId, diccImagenes,diccPromedio ) for columna in range(imgWidth)]
    
    while len(task_ids) > 0:
        done_ids, task_ids = ray.wait(task_ids)
        result = ray.get(done_ids[0])
        listaColumnas[result[0]] = result[1]
    
    tiempoCollage = time.time() - inicioCollage

    for col in range(imgWidth):
        for row in range(imgHeight):
            canvasCollage.paste(listaColumnas[col][row] ,(col*tamanioPixel, row*tamanioPixel))
    

    return (canvasCollage, tiempoCollage)



