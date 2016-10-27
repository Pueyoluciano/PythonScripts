#- EJ1 ---------------------------------------------------------------------------------
# - Complejidad:
# -- c    = 2      <-- Ya que en cada llamado parto en 2 la lista recibida.
# -- a    = 2      <-- Ya que siempre hago 2 llamados recursivos.
# -- f(n) = O(1)   <-- En el caso base(cuando la |lista|=2) solo hago asignaciones y 
#                      comparasiones.
# -- log2(2) = 1   <-- f(n)  e O(n^1)
# -- T(n) = O(n^1 * log(n))      2T(n/2) + f(n) 

def masALaIzquierda(lista):
    print lista
    #raw_input("...")
    
    if (len(lista) == 2):
        if(lista[0] > lista[1]):
            return True
            
        else:
        
            return False
    else:
        
        resultado = masALaIzquierda(lista[: len(lista)/2]) and masALaIzquierda(lista[len(lista)/2:])

    return resultado
#---------------------------------------------------------------------------------------
#- EJ2 ---------------------------------------------------------------------------------
def listaCreciente(lista):
    return listaCrecienteAux(lista, 0);
    
def listaCrecienteAux(lista, offset):
    print lista
    #raw_input("...")
    
    if(len(lista) == 0):
        return True
        
    if(len(lista) == 1):
        if(offset + 1 == lista[0]):
            return True
        else:
            return False
            
    if(len(lista) == 2):
        if(offset + 1 == lista[0] or offset + 2 == lista[1]):
            return True
        else:
            return False
    
    resultado = listaCrecienteAux(lista[0: len(lista)/2], offset) or listaCrecienteAux(lista[len(lista)/2:], offset + len(lista)/2)
    
    return resultado
#---------------------------------------------------------------------------------------
#- EJ3 ---------------------------------------------------------------------------------
def exponencial(base, exponente):
    if(exponente == 0):
        return 1
        
    if(exponente == 1):
        return base
        
    if(exponente == 2):
        return base*base
    
    # me voy llamando recursivamente hasta llegar a un exponente de 0 1 o 2.
    # cuando vuelvo de la llamada tomo ese valor calculado y lo multiplico por si mismo.
    # Si hago eso ciegamente estoy haciendo esto:
    # (b*b) * (b*b) * ...
    # que funciona perfecto para exponentes pares, pero para impares agregue una b de mas.
    # Por eso si el exponente es impar hago esa cuenta rara para que
    # el resultado quede (b*b) * b
    # y si es par queda (b*b) * (b*b)

    parcial = exponencial(base,exponente - exponente/2)
    resultado = parcial * parcial/(base**(exponente%2))
        
    return resultado
    
#---------------------------------------------------------------------------------------
#- EJ4 ---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
#- SEGUNDO PARCIAL(RECUPERATORIO) 2015 -------------------------------------------------
class AB:
    def __init__(self, raiz=None, izq=None, der=None):
        self.raiz = raiz
        self.izq = izq
        self.der = der
    
    def esHoja(self):
        if(self.raiz != None and self.izq == None and self.der == None):
            return True
        
        return False
        
def maximaSumaCamino(arbol):
    return maximaSumaCaminoAux(arbol)

def maximaSumaCaminoAux(arbol):
    raiz
    hijoIzq
    hijoDer
    maxParcialIzq
    maxParcialDer

    maximo(raiz, hijoIzq,hijoDer, )

    
    raiz + hijoIzq + maxParcialIzq > maxParcialIzq? => 


    maxIzq = 0
    maxDer = 0
    print arbol.raiz
    if(arbol.esHoja()):
        print "maximo parcial: " + str(arbol.raiz)
        return arbol.raiz, arbol.raiz # raiz y maximo
        
    else:
        if(arbol.izq):
            hijoIzquierdo, maximoParcial = maximaSumaCamino(arbol.izq)
            # maxIzq = arbol.raiz + izquierdo
            
        if(arbol.der):
            hijoDerecho, maximoParcial = maximaSumaCamino(arbol.der)
            # maxDer = arbol.raiz + derecho
    
        if(arbol.raiz >= maxIzq and arbol.raiz >= maxDer):
            return arbol.raiz
            print "maximo parcial: " + str(arbol.raiz)
        else:
            if(izquierdo > maxIzq):
                print "maximo parcial: " + str(maxIzq)
                return maxIzq
            else:
                print "maximo parcial: " + str(maxDer)
                return maxDer
                
                
#---------------------------------------------------------------------------------------
#- EJERCICIOS --------------------------------------------------------------------------
def ej1():
    si = [13,12,11,10,9,8,7,6,12,11,10,9,8,7,6,5]
    no = [11,12,10,9,8,7,6,5]
    print masALaIzquierda(si)
    print masALaIzquierda(no)
    
def ej2():
    si = [-4,-3,-2,-1,0,6,8,9]
    no = [-4,-3,-2,-1,0,7,8,9]
    print listaCreciente(si)
    print listaCreciente(no)
    
def ej3():
    print exponencial(2,9)
    print exponencial(5,7)
    print exponencial(6,8)
    print exponencial(6,13)
    
def parcial():
    # AB(-1,
        # AB(-2,
            # AB(81),AB(0))
        # ,AB(-3)
        # )
    ab = AB(-1,AB(-2,AB(81),AB(0)),AB(-3))
    print maximaSumaCamino(ab)
#---------------------------------------------------------------------------------------
#- LLAMADAS ----------------------------------------------------------------------------
#ej1()
#ej2()
# ej3()
parcial()
#---------------------------------------------------------------------------------------
