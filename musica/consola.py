# -*- coding: utf-8 -*-

class Menu:
    def __init__(self, nodoRaiz):
        self.nodo = nodoRaiz
        self.nodo.soyRaiz = True
        
    def iniciar(self):
        self.nodo.evaluar()
    
    
class Nodo:
    def __init__(self, nombre, texto, accion, *nodos):
        self.nombre = nombre
        self.texto = texto
        self.accion = accion
        self.nodos = nodos
        self.soyRaiz = False
        
    def soyHoja(self):
        return False if self.submenus else True
        
    def _seleccionar(self):
        correcto = False
        
        while not correcto:
            eleccion = input("> ")
        
            try:
                eleccion = int(eleccion)
                
                # Volver o salir siempre es una opcion valida,
                # Por eso preguntamos por eleccion <= len(self.nodos) + 1
                
                offset = 1 if self.accion else 0
                if eleccion > 0 and (eleccion <= len(self.nodos) + 1 + offset):
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
            
            # Si el nodo tiene una accion, es la primera que se muestra.
            offset = 0
            if self.accion:
                print("1 - " + self.accion.descripcion)
                offset += 1
            
            # Recorro los nodos internos, y muestro sus nombres.
            # Al usuario se le muestran los indices en la numeracion normal (de 1 en adelante)
            # Por ultimo debemos tener en cuenta el offset, ya que si el nodo tiene una accion,
            # todas las que siguen estan corridas 1 lugar.
            for i, submenu in enumerate(self.nodos):
                print(str(i + 1 + offset) + " - " + submenu.nombre)
           
            #Si Estamos en el nodo raiz, salimos, sino volvemos un nivel para arriba
            if self.soyRaiz:
                print(str(len(self.nodos) + 1 + offset) + " - " + "salir")
                
            else:
                print(str(len(self.nodos) + 1 + offset) + " - " + "volver")
            
            #Le pedimos al usuario que eliga una opcion    
            eleccion = self._seleccionar()
            
            if self.accion:
                if eleccion == 1:
                    self.accion.ejecutar()

                else:
                    if eleccion == (len(self.nodos) + 2):
                        pass
                    
                    
            else:
                # Salir o volver
                if eleccion == (len(self.nodos) + 1 + offset):
                    salir = True
                    
                else:
                    self.nodos[eleccion].evaluar()
                
        return
        
    def __str__(self):
        return self.nombre + " " + self.texto + " " + str(self.soyRaiz)
    
class Accion:
    def __init__(self, descripcion, metodo, argumentos=None):
        self.descripcion = descripcion
        self._metodo = metodo
        self._argumentos = argumentos
        
    def ejecutar(self):
        return self._metodo(*self._argumentos) if self._argumentos else self._metodo()
        
    
def funcion():
    print("Soy una Funcion sin argumentos")
    
def funcionDos(a):
    print("Soy una funcion con un argumento", a)
    
def funcionTres(a,b,c):
    print("Soy una funcion con tres argumentos", a, b, c)

# nodos = Nodo("Menu Principal", "A tu vieja le gusta asi", Accion("Accion del menu principal", funcion),
            # Nodo("Opcion 1", "Soy la primera opcion", Accion("Accion de la opcion 1", funcionDos, "QUESO")),
            # Nodo("Opcion 2", "Soy la segunda opcion",Accion("Accion de la opcion 2", funcionTres, ("HOLA", "VIEJO", "COMO ESTAS")))
        # )

        
# menuA = Menu(nodos)


# print(menuA.nodo)

# menuA.iniciar()