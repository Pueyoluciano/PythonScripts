import os
import math
import traceback
from validador import *
class Generales:

    """
    Clase con funciones para uso generico.
    -- self.enumerarLista(self) sirve mostrar en pantalla los items de una lista con un numero de orden.
    """
    
    @staticmethod
    def enumerarLista(lista):
        if (len(lista) == 0):
            print("[!!] Lista vacia")
            
        else:
            retorno = []
            relleno = " " * int(math.floor(math.log(len(lista),10)))
            multiplicador = 1
            contador = 1
            
            print("")
            
            for i in range(0,len(lista)):
                if(i > (9*multiplicador) - 1):
                    relleno = relleno[0:-1]
                    multiplicador += 10 ** contador
                    contador += 1
                
                retorno.append(str(i+1) + ") " + relleno + str(lista[i]))
                print(str(i+1) + ") " + relleno + str(lista[i]))
                
            print("")
            
            return retorno
        
    @staticmethod
    def seleccionarArchivo(ruta):
        if(os.path.isdir(ruta)):
            listado = os.listdir(ruta)
            Generales.enumerarLista(listado)
            indice = validador.ingresar(int,validador.entre, 1, len(listado))
            file = listado[indice - 1]
            return  os.path.abspath(file)
    
    @staticmethod
    def abrirArchivo(ruta):
        if(os.path.isdir(ruta)):
            listado = os.listdir(ruta) + ["Volver"]
            
            print("Directorio: " + ruta)
            Generales.enumerarLista(listado)
            
            file = validador.seleccionar(listado)
            
        else:
            if(os.path.isfile(ruta)):
                file = ruta
            
            else:
                raise Exception("ruta invalida")
            
        if(file != "Volver"):
            if(os.path.isfile(file)):
                os.startfile(file)
            else:
                respuesta = Generales.abrirArchivo(file)
                    
            