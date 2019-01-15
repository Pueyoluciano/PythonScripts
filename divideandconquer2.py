class AB:
    def __init__(self, raiz=None, izq=None, der=None):
        self.raiz = raiz
        self.izq = izq
        self.der = der
    
    def esHoja(self):
        if(self.raiz != None and self.izq == None and self.der == None):
            return True
        
        return False
        
def hijosEnNivel(arbol,nivel):
    return hijosEnNivelAux(arbol,nivel,0)
        
def hijosEnNivelAux(arbol,nivel,nivelActual):
    acumulado = 0
    if(not(arbol)):
        return 0
    
    if(nivel == 0):
        return int(arbol.raiz != None)
        
    if(nivelActual == nivel - 1):
        return int(arbol.izq != None) + int(arbol.der != None)
    else:
        acumulado += hijosEnNivelAux(arbol.izq, nivel, nivelActual + 1) + hijosEnNivelAux(arbol.der, nivel, nivelActual + 1)
    return acumulado
    
    
    
a = AB(1,AB(2,AB(4),AB(5)),AB(3,AB(6),AB(7)))

print hijosEnNivel(a,0)
print hijosEnNivel(a,1)
print hijosEnNivel(a,2)
