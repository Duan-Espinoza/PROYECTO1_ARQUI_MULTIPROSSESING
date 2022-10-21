
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import ray

pathImagenes = os.path.join(os.getcwd(), "imgs")
pathImagenesBase = os.path.join(os.getcwd(), "Imagenes_base")
pathResultado = os.path.join(os.getcwd(), "resultado")
newSize = 50


def Paralelo():
    inicio = time.time()
    directorioImagenes  = cargaImagenes(pathImagenes)
    print("Duración Carga Imagenes: ", time.time() - inicio)

    inicio = time.time()
    imagenesModificadas = cambioTamanioImgParalelo(directorioImagenes, pathImagenes)
    print("Duración Cambio de Tamaño: ", time.time() - inicio)

    inicio = time.time()
    diccionarioPromRgb ,diccionarioImgRGB = valorRGBParalelizado(imagenesModificadas)
    print("Duración Cambio Promedio RGB: ", time.time() - inicio)
    #Realizar Collage

    print("diccionario RGB: "+(str(len(diccionarioImgRGB)-1)))
    print("Realizando el Collage Paralelo")
    inicio = time.time()
    result = realizarCollageImg(diccionarioImgRGB, pathImagenesBase, diccionarioPromRgb)
    print("Duración Collage: ", time.time() - inicio)


    pathREsultado = os.path.join(os.getcwd(), "resultado/resultado.jpg") 
    print(pathREsultado)
    result.save( pathREsultado )
    ray.shutdown()


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

@ray.remote
def minimizarImagen(x,ruta):
  im = Image.open(os.path.join(ruta, x),"r")
  newsize = (newSize, newSize)
  im1 = {'imagen':im.resize(newsize), 'nombre':x, 'promRGB':0}
  return im1

def cambioTamanioImgParalelo(directorio,ruta):
    """Cambia el tamaño de las imagenes 

    Parameters
    ----------
    directorio: List
        Lista de nombres de las imagenes del folder
    ruta : str
        Ruta la cual se va a verificar su validez.
    """
    print("------ Cambiando el size de las imagenes")
    listaImagenes = ray.get([minimizarImagen.remote(x,ruta) for x in directorio])
    
    return listaImagenes

diccionarioImagenes = {}
diccionarioPromedios = {}


def waitSec(x):
    time.sleep(0.0001)
    return x 


@ray.remote
def obtenerRGB(x,diccionarioPromedios,diccionarioImagenes):
    arr = np.array(x['imagen']) # Vamos a convertir la imagen en un arreglo
    arr_mean = np.mean(arr, axis=(0,1))

    if(arr.ndim != 3):
        nombreImagen = x['nombre']
        #print(f'Imagen {nombreImagen} tiene {arr.ndim} dimensiones, el shape es: {arr.shape}, el promedio RGB es de {arr_mean}')

        # {'128,250,74':<imagen>, '123,345,432':<imagen2>, }

        # {'128,250,74':<imagen>, '123,345,432':<imagen2>, }
        # [12825074, 123345432, 886878687, 98168761847]

        rgb = waitSec(f'{int(arr_mean)}{int(arr_mean)}{int(arr_mean)}')

        "255255255"
        
        listaRGB = waitSec([arr_mean,arr_mean,arr_mean])

        diccionarioImagenes[rgb] =  waitSec(x['imagen'])
        diccionarioPromedios[rgb] =   waitSec(listaRGB)

        #Muestra la Imagen 
        # plt.imshow(x['imagen'])
        # plt.show()
        #x['imagen'].show()
    else:
        # print(f'[R={int(arr_mean[0])},  G={int(arr_mean[1])}, B={int(arr_mean[2])} ]')
        # El valor RGB
        

        rgb = waitSec(f'{int(arr_mean[0])}{int(arr_mean[1])}{int(arr_mean[2])}')

        listaRGB = waitSec([int(arr_mean[0]), int(arr_mean[1]),int(arr_mean[2])])

        diccionarioPromedios[rgb] = waitSec(listaRGB)
        diccionarioImagenes[rgb] = waitSec(x['imagen'])

    return [rgb,listaRGB,x]
    
    
def valorRGBParalelizado(lista):
    diccionarioPromediosID = ray.put(diccionarioPromedios)
    diccionarioImagenesID = ray.put(diccionarioImagenes)
    task_ids = [obtenerRGB.remote(waitSec(x),diccionarioPromediosID,diccionarioImagenesID) for x in lista]
    
    while len(task_ids) > 0:
        done_ids, task_ids = ray.wait(task_ids)
        result = ray.get(done_ids[0])
        diccionarioPromedios[result[0]] = waitSec(result[1])
        diccionarioImagenes[result[0]] = waitSec(result[2]['imagen'])

    return(diccionarioPromedios,diccionarioImagenes)


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
   
def buscarPixel(pixel, diccProm):
    R = pixel[0]
    G = pixel[1]
    B = pixel[2]

    keyMenor = ""
    promMenor = 0

    for key, value  in diccProm.items():
        
        prom = (abs(value[0] - R) + abs(value[1] - G) + abs(value[2] - B))//3

        if (keyMenor == ""):
            keyMenor = key
            promMenor = prom

        if prom < promMenor:
            promMenor = prom 
            keyMenor = key
    return keyMenor


@ray.remote
def collageParalelo(pixel,x,
                    height,background, 
                    diccIm,diccProm):
    time.sleep(0.000001)
    for y in range(height):
            color = pixel[y, x]
            key = buscarPixel(color,diccProm)
            background.paste(diccIm[key], (0, y*newSize) )

    return (x,background)
    time.sleep(0.000001)


def realizarCollageImg(diccionarioImagenes, 
                        pathImagenesBase, 
                        diccionarioPromedio):
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

    im_bg = Image.new(mode="RGB", size=(imgWidth*newSize, imgHeight*newSize))
    im_column = Image.new(mode="RGB", size=(newSize, imgHeight*newSize))

    # pixel = img.load() 

    # Va columan por columna, de arriba hacia abajo, empezando con la columna de la izquiera de la img
    heightId = ray.put(imgHeight)
    imColId = ray.put(im_column)
    pixelId = ray.put(np.array(img))
    diccImagenes = ray.put(diccionarioImagenes)
    diccPromedio = ray.put(diccionarioPromedio)

    task_ids = [collageParalelo.remote(pixelId, x, heightId,imColId, diccImagenes,diccPromedio ) for x in range(imgWidth)]
    
    while len(task_ids) > 0:
        done_ids, task_ids = ray.wait(task_ids)
        result = ray.get(done_ids[0])
        im_bg.paste(result[1], (result[0]*newSize, 0))

    return im_bg



