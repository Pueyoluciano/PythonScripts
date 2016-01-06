import math
class Generales:

    """
    Clase con funciones para uso generico.
    -- self.enumerarLista(self) sirve mostrar en pantalla los items de una lista con un numero de orden.
    """
    
    @staticmethod
    def enumerarLista(lista):
        relleno = " " * int(math.floor(math.log(len(lista),10)))
        multiplicador = 1
        contador = 1
                
        for i in range(0,len(lista)):
            if(i > (9*multiplicador) - 1):
                relleno = relleno[0:-1]
                multiplicador += 10 ** contador
                contador += 1
                
            print str(i+1) + ") " + relleno + str(lista[i])
