# -*- coding: utf-8 -*-
"""
    Pequeña implementacion para crear Menus para una interfaz de consola.
    
    ---
    
    La estructura principal es un arbol de Nodos y Acciones. La clase Menu es el punto de entrada a la estructura.
    
    cada Nodo tiene una lista de nodos y/o acciones. La conjuncion de nodos permite armar la estructura del menu,
    las acciones concretas estan resueltas con la clase Accion.
"""

from functools import *

class Menu:
    """
        Clase principal, recibe un Nodo, que será el raiz. La estructura 
        de nodos debe estar previamente creada.
        
        --- atributos ---
        - nodo: Arbol de Nodos y Acciones
        
        --- metodos ---
        - iniciar: Loop del menu. Invoca al evaluar del nodo raiz.
        
    """
    def __init__(self, nodoRaiz):
        """
            nodoRaiz: Nodo que contiene toda la estructura. 
            Es la representacion del menu principal.
            
            Cuando se crea el menu se marca como "raiz" a dicho nodo.
            Principalmente para que pueda distinguir entre el mensaje de "salir" o "volver".
            
        """
        self.nodo = nodoRaiz
        self.nodo.marcarComoRaiz()
        
    def iniciar(self):
        """
            Invoca al evaluar del nodo raiz.
        """
        self.nodo.evaluar()
    
    def mapa(self):
        return self.__str__()
        
    def __str__(self):
        return self.nodo.mapa(0)
        
class Nodo:
    """
        Estructura que permite crear arboles de menus.
        
        --- atributos ---
        - nombre: Nombre del menu. Es el texto que se muestra para identificarlo.
        
        - texto: Texto descriptivo del rol que cumple el nodo.
        
        - repetible: Los nodos repetibles ofrecen sus distintas opciones luego de terminar la accion anterior.
            Es decir, el nodo estara activo hasta que se realice la accion de "volver" (o salir si es raiz).
            Los NO repetibles por el contrario permiten realizar una accion una unica vez y luego sube un nivel en la estructura.
            El nodo raiz suele ser repetible.
          
        - nodos: lista de nodos y acciones. Están ordenados por lo que aparecerán en la pantalla segun su orden de insercion.
            La ultima accion siempre es la de "volver" (o salir si es raiz).
        
        - _soyRaiz: booleano que denota al nodo raiz. De uso interno, para cambiar este valor hay que usar la accion
            marcarComoRaiz.
            
        - accionVolver: Accion para "volver" un nivel hacia atras, o si el nodo raiz, "salir" del programa.
    """

    def __init__(self, nombre, texto, repetible, *nodos):
        self.nombre = nombre
        self.texto = texto
        self.repetible = repetible
        self._soyRaiz = False
        
        self.accionVolver = Accion("Volver", False, lambda: True)

        self.nodos = list(nodos)

        self.nodos.append(self.accionVolver)
        
    def marcarComoRaiz(self):
        self.accionVolver.nombre = "Salir"
        
    def _seleccionar(self):
        correcto = False
        
        while not correcto:
            eleccion = input("> ")
        
            try:
                eleccion = int(eleccion)
                
                # Volver o salir siempre es una opcion valida,
                # Por eso preguntamos por eleccion <= len(self.nodos) + 1
                
                if eleccion > 0 and eleccion <= len(self.nodos):
                    correcto = True
                
                else:
                    raise IndexError
                    
            except (ValueError, IndexError):
                print("La opción no es valida")
        
        return eleccion
        
    def evaluar(self):
        salir = False
        
        while not salir:
            print(self.nombre)
            print(self.texto)
            print("")
            
            for i, opcion in enumerate(self.nodos, 1):
                print(str(i) + " - " + opcion.nombre)
                
            eleccion = self._seleccionar()
            self.nodos[eleccion - 1].evaluar()
            
            salir = not self.nodos[eleccion - 1].repetible or eleccion == len(self.nodos)
        
        return self.repetible
    
    def mapa(self, tabs):
        return self.__str__(tabs)
    
    def __str__(self, tabs):
        tabulacion = ('|   ' * tabs)
        return self.nombre + " - " + self.texto + "\n" + reduce(lambda x, y: x + y, [tabulacion + "| - " + x.mapa(tabs + 1) for x in self.nodos])
   
   
class Accion:
    def __init__(self, nombre, repetible, metodo, *argumentos):
        self.nombre = nombre
        self._metodo = metodo
        self.repetible = bool(repetible)
        self._argumentos = argumentos
        
    def evaluar(self):
        return self._metodo(*self._argumentos) if self._argumentos else self._metodo()
        
    def mapa(self, tabs):
        return self.__str__(tabs)
    
    def __str__(self, tabs):
        tabulacion = ('    ' * tabs)
        return self.nombre + "()\n"
        

    
# Estructura de ejemplo
# def funcionUno():
    # print("Soy una Funcion sin argumentos")
    
# def funcionDos(a):
    # print("Soy una funcion con un argumento", a)
    
# def funcionTres(a,b,c):
    # print("Soy una funcion con tres argumentos", a, b, c)

# nodos = Nodo("Menu Principal", "Este es el menu principal. Re cheto", True, 
        # Accion("Accion 1",True, funcionUno), 
        # Accion("Accion 2",True, funcionDos, "HOLA VIEJA"),
        # Nodo("SubMenu 1", "Este nodo no tiene acciones", True,
            # Nodo("SubMenu 2", "asd", True, Accion("Accion 3", False,funcionTres, "A", "B", "C")),
            # Nodo("SubMenu 3", "asdaasd", True, Accion("Accion 4", False, funcionTres, "D", "E", "F"))
        # )
    # )
        
# menuA = Menu(nodos)

# print(menuA.mapa())

# menuA.iniciar()