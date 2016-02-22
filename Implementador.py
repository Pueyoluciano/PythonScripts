class Item:
    
    """
    - Item permite administrar entidades con nombre, una descripcion y una implementacion,
      brindando una interfaz sencilla para manejar funcionalidades.
      
    - nombre y descripcion son strings.
    
    - implementacion es una funcion que se ejecuta al invocar
      accionDiccionario, accionLista o accionParametro.
    
    
    - metodos:
    
    - los tres metodos realizan la misma accion, ejecutar la funcion asiganda en self.implementacion,
      diferenciandose cada uno en como se invoca.
      
    - accionDiccionario(self,**params)
        Ej: accionDiccionario(parametro1=True, parametro2=4)
        
    - accionLista(self,*params)
        Ej: accionLista(True,4)
        
    - accionParametro(self,params)
        Ej: accionParametro("ErnestoSabato")
    """
    
    def __init__(self,nombre,desc,impl):
        self.nombre = nombre
        self.descripcion = desc
        self.implementacion = impl

    def __str__(self):
        return str(self.nombre)
        
    def accionDiccionario(self,**params):
        return self.implementacion(params)
    
    def accionLista(self,*params):
        return self.implementacion(params)
    
    def accionParametro(self,params):
        return self.implementacion(params)

class Implementaciones:
    
    """
    FILLME
    """

    def __init__(self):
        self.contenido = []
        self.nombres = []
    
    def _actualizarNombres(self):
        self.nombres = [item.nombre for item in self.contenido]
    
    def agregarItem(self,nombre,desc,impl):
        self.contenido.append(Item(nombre,desc,impl))
        self._actualizarNombres()

    def obtenerID(self,nombre):
        if(nombre in self.nombres):
            return self.nombres.index(nombre)
        else:
            return -1
        
    def obtenerItem(self,nombre):
        return self.contenido[self.obtenerID(nombre)]
    
    def obtenerNombre(self,id):
        return self.nombres[id]