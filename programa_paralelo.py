
import os
from PIL import Image
# impport multiprocessing as mp
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


def tiempo():
  inicio = time.time()
  directorioImagenes = cargaImagenes(pathImagenes)
  cambioTamanioImg(directorioImagenes, pathImagenes)
  print("Duración: ", time.time() - inicio)

tiempo()


