#Proyecto 1 Arquitectura Computadores
#Estudiantes:
#Duan Antonio Espinoza
#Josue Daniel Chaves Araya
#Valentin Tissera Doncini
#Profesor: Luis Diego Gomez Rodriguez
#Collage de imagenes


#Librerias necesarias
import programa_paralelo as paralelo
import programa_secuencial as secuencial

def menuPrincipal():
    """Serie de prints que muestran las opciones disponibles del menu

    Input
    ----------
    Digito de entrada,para determinar cual opcion se eligio

    Out
    ----------
    Menu seleccionado
    
    Restrictions
    ----------
    Solo valor numérico entero


    """
    print("*****Collage de imagenes******\n")
    print("Opcion 1: Algoritmo Secuencial")
    print("Opcion 2: Algoritmo Paralelo")
    print("Opcion 3: Salir\n")
    try:
        opcion=int(input("Digite su opcion:"))
    except:
        print("Opción no válida\n")
        return menuPrincipal()
    if opcion==1:
        return secuencial.cargaImagenes()
    if opcion==2:
        return paralelo.hello()
        pass
    if opcion==3:
        pass
    else:
        print("Opción no válida")
        return menuPrincipal()




menuPrincipal()
