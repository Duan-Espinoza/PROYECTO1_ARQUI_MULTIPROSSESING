
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import ray

ray.init()
pathImagenes = os.path.join(os.getcwd(), "imgs")
pathImagenesBase = os.path.join(os.getcwd(), "Imagenes_base")
pathResultado = os.path.join(os.getcwd(), "resultado")
newSize = 50


def Secuencial():
    directorioImagenes  = cargaImagenes(pathImagenes)
    imagenesModificadas = cambioTamanioImg(directorioImagenes, pathImagenes)
    diccionarioRGB = valorRGB(imagenesModificadas)
    realizarCollageImg(diccionarioRGB, pathImagenesBase, pathResultado)


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

def cambioTamanioImg(directorio,ruta):
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
def obtenerRGB(x):
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

    
def valorRGBParalelizado(lista):
    ray.get([obtenerRGB.remote(waitSec(x)) for x in lista])


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
   

def tiempo():
  inicio = time.time()
  directorioImagenes = cargaImagenes(pathImagenes)
  imagenesModificadas = cambioTamanioImg(directorioImagenes, pathImagenes)
  diccionarioRGB = valorRGBParalelizado(imagenesModificadas)
  print("Duración: ", time.time() - inicio)

tiempo()


