from validador import *
from Generales import Generales
class Nodo:

    """
    Esta clase sirve para hacer Menus para interaccion con el usuario.
    es un arbol donde cada Nodo tiene un nombre, un texto y una lista de nodos.
    el Leaf es un nodo que tiene la accion concreta.

    Expandir muestra todo el arbol.
    evaluar permite ejecutar la operacion deseada recorriendo el arbol 1 nodo a la vez.
    
    Ejemplo de Menu:
    a = Nodo("Nodo Principal","",Nodo("Nodo1","",Nodo("Nodo3","",Leaf("Leaf1","",lambda x:1),Leaf("Leaf2","",lambda x:2))),Nodo("Nodo2","",Leaf("Leaf3","",lambda x:3),Leaf("Leaf4","",lambda x:4))) 
    """
    
    def __init__(self,nombre,texto,*nodos,**args):
        if("root" in args.keys()):
            self.soyRaiz = True # este atributo sirve para indicar que el nodo es el nodo Raiz. si NO es raiz, se muestra el item "volver" en el menu
        else:
            self.soyRaiz = False

        self.nodos = []
        self.nombre = nombre
        self.texto = texto
        self.nodos.extend(nodos)
        
    def expandir(self,tabs=""):
        print(self.nombre)
        for nodo in self.nodos:
            print("|-" + tabs,)
            nodo.expandir(tabs + "-")
    
    def evaluar(self):
        print(self.nombre)
        print(self.texto)
        
        nombreNodos = [item.nombre for item in self.nodos]
        listaNodos = nombreNodos if self.soyRaiz else nombreNodos + ["volver"]
        Generales.enumerarLista(listaNodos)
        
        if(not self.soyRaiz):
            nodo = validador.seleccionar(self.nodos+["volver"])
        else:
            nodo = validador.seleccionar(self.nodos)    
            
        if(nodo != "volver"):
            return nodo.evaluar()
    
    def agregar(self,i,nodo):
        if(i<0):
            i = len(self.nodos) + (i + 1)
        self.nodos.insert(i,nodo)
    
    
class Leaf:
    def __init__(self,nombre,texto,accion):
        self.nombre = nombre
        self.texto = texto
        self.accion = accion
    
    def expandir(self,tabs=""):
        print("> " + self.nombre)
    
    def evaluar(self):
        print(self.texto)
        return self.accion()
 