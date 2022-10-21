
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
diccionarioImagenes = {}
diccionarioPromedios = {}


def Paralelo():

    inicio = time.time()
    directorioImagenes  = cargaImagenes(pathImagenes)
    print("Duración Carga Imagenes: ", time.time() - inicio)


    inicio = time.time()
    imagenesModificadas = cambioTamanioImg(directorioImagenes, pathImagenes)
    print("Duración Cambio de Tamaño: ", time.time() - inicio)

    inicio = time.time()
    diccionarioRGB = valorRGB(imagenesModificadas)
    print("Duración Cambio Promedio RGB: ", time.time() - inicio)
    #Realizar Collage


    print("Realizando el Collage Paralelo")
    inicio = time.time()
    result = realizarCollageImg(diccionarioImagenes, pathImagenesBase, pathResultado)
    print("Duración Collage: ", time.time() - inicio)


    pathREsultado = os.path.join(os.getcwd(), "resultado/resultado.jpg") 
    print(pathREsultado)
    result.save( pathREsultado )
    # resultado.show()




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
def minimizarImagen(x,ruta,tamanio):
  im = Image.open(os.path.join(ruta, x),"r")
  im1 = {'imagen':im.resize(tamanio), 'nombre':x, 'promRGB':0}
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
    listaImagenes = ray.get([minimizarImagen.remote(x,ruta,(newSize,newSize)) for x in directorio])
    
    return listaImagenes


def valorRGBAux(lista):
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
    return diccionarioImagenes

    

def valorRGB(lista):
    return valorRGBAux(lista)




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

def buscarPixel(pixel):
    time.sleep(0.000001)

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
    time.sleep(0.000001)
    return keyMenor


@ray.remote
def collageParalelo(pixel,x,height,background):
    for y in range(height):
            color = pixel[x, y]
            key = buscarPixel(color[y])
            background.paste(diccionarioImagenes[key], (x*newSize, y*newSize) )



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

    im_bg = Image.new(mode="RGB", size=(imgWidth*newSize, imgHeight*newSize))

    pixel = img.load() 

    # Va columan por columna, de arriba hacia abajo, empezando con la columna de la izquiera de la img

    bgId = ray.put(im_bg)
    pixel = ray.put(np.asarray(img))
    task_ids = [collageParalelo.remote(pixel, x, imgHeight,bgId ) for x in range(imgWidth)]
    im_bg.show()

    return im_bg



# def realizarCollageImg(pixels, imgBackground,diccionarioImagenes, diccionarioPromediosP, col, height):
#     time.sleep(0.000001)
#     # Va columan por columna, de arriba hacia abajo, empezando con la columna de la izquiera de la img

#     for y in range(height):
#         color = pixels[col, y]
#         key = buscarPixel(color, diccionarioPromediosP)
#         imgBackground.paste(diccionarioImagenes[key], (col*newSize, y*newSize) )
#     time.sleep(0.000001)
#     return 


# def realizarCollageImagenParalelo( diccionarioImagenes, diccionarioPromediosP, pathImagenesBase,):

#     print("Realizando el Collage Paralelo")
#     imagenesBase = cargaImagenes(pathImagenesBase)
#     imagenSeleccionada = menuSeleccionImagenBase(imagenesBase)

#     img = Image.open(os.path.join(pathImagenesBase, imagenSeleccionada),"r")
#     imgWidth, imgHeight = img.size
#     imgBackground = Image.new(mode="RGB", size=(imgWidth*newSize, imgHeight*newSize))
    
#     time.sleep(0.000001)
#     pixelsId = ray.put(np.asarray(img))
#     imgBackgroundId = ray.put(imgBackground)
#     diccionarioImagenesId = ray.put(diccionarioImagenes)
#     diccionarioPromediosPId = ray.put(diccionarioPromediosP)
    
#     result_ids = [realizarCollageImg.remote(pixelsId,imgBackgroundId,diccionarioImagenesId, diccionarioPromediosPId, x, imgHeight ) for x in range(imgWidth)]
#     #results = ray.get(result_ids)

#     ray.shutdown()

#     print("Holi")

#     return imgBackground

    



    
    





# def tiempo():
#   directorioImagenes = cargaImagenes(pathImagenes)

#   inicio = time.time()
#   cambioTamanioImg(directorioImagenes, pathImagenes)
#   print("Duración Cambio tamaño de Imágenes: ", time.time() - inicio)

# tiempo()


