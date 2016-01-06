import random
import time
from Generales import Generales
from validador import *

class Probabilidad:

    """
    Esta clase permite cargar un conjunto de datos, asignarle una probabilidad
    de ocurrencia, y obtener uno de estos en base a la probabilidad asignada.
    
    - El atributo self.conjunto tiene la siguiente estructura:
    -- para cuatro valores : a, b, c, d
    -- con probabilidades 0.5, 0.0, 0.9, 0.1 # el valor 0.0 quiere decir que no puede ser seleccionado.
    
    -- self.conjunto queda = [['a', [0.0, 0.5]], ['b', [-1, -1]], ['c', [0.5, 0.9]], ['d', [0.9, 1.0]]]
    
    -- Como se aprecia, se guarda una lista de tuplas de la forma ["elemento",[desde,hasta]]
    -- Donde desde y hasta tienen la propiedad de ser : hasta - desde = probabilidad(elemento)
        
    ----------------------------------------------------------------------------
    
    - Metodos:
    
    - cargarDatos(self,*datos)
    -- Recibe los datos para asignarles una probabilidad, en este metodo se
       reparte equitativamente la misma para cada dato. es decir:
       Para cada dato: probabilidad = 1.0/len(datos)
    
    - cargarProbabilidades(self)
    -- para una lista de datos cargada, permite asignarle a mano una por una
       la probabilidad deseada a cada elemento. La suma total siempre sera = 1.0
       - Si se alcanza el total(osea 1.0) antes de recorrer todos los elementos,
         se termina la carga, es decir que dichos elementos 
         quedaran con 0.0 de probabilidad.
       - Si el total(1.0) no es alcanzado, se debe repetir la operacion desde el
         primer elemento.
    
    - cargarTodoDesdeArchivo(self,ruta)
    -- Levanta el archivo indicado en "ruta" y realiza un cargarTodo()
       con los datos que estan cargados ahi.
       El formato del archivo debe ser el siguiente: (Para cuatro elementos, "a" "b" "c" y "d") 
     ---------
       a 0.3
       b 0.1
       c 0.5
       d 0.2
     ---------
       Como se aprecia, la estructura es item (un espacio) valor entre 0.0 y 1.0.
    
    - cargarTodo(self, *datos)
    -- permite cargar datos y probabilidades en una sola invocacion.
       recibe una lista del tipo [[elemento,probabilidad], ...] y actualiza
       self.conjunto con los nuevos datos.
       De manera similar que en cargarProbabilidades(), si en los datos llegan 
       una suma total de probabilidades mayor a 1.0, se truncaran los valores a partir del elemento
       que haya sumado mas de 1.0.
    
    - generar(self)
    -- Devuelve un elemento de la lista de forma aleatoria, considerando las 
       probabilidades asignadas a cada uno.
       
    - chequearValores(self)
    -- Este metodo sirve a modo de prueba para comprobar que las probabilidades se
       cumplen, ejecuta el metodo generar() repetidas veces, y cuenta las veces 
       que cada item fue elegido.
    
    - _agregarItemConDelta(self,dato,desde,hasta)
    -- Metodo unificado para agregar items con "valor" "desde" y "hasta" a self.conjunto.
       Es para uso interno de la clase.
    
    - reestablecerDatos(self):
    -- Invoca al metodo self.cargarDatos() con el parametro self.listarItems()
       listarItems devuelve todos los items sin probabilidad, y cargarDatos reparte equitativamente
       la probabildad entre todos los items recibidos por parametro. de modo que "reinicia" los 
       elementos.
    
    - compensar(self,item)
    -- Permite actualizar probabilidades para toda la tabla de la siguiente manera:
         Recibe un item con un valor de probabilidad asociado (Este item debe existir entre los datos actuales).        
         Actualiza el valor de prob. del item en la tabla con el valor recibido por parametro.
         Actualiza el resto de los elementos quitandoles una cantidad igual para que se mantenga
         la probabilidad total = 1.
    
    - esLista(self,objeto)
    -- Funcion auxiliar que devuelve True si objeto es el tipo lista, tupla o set.
    
    - obtenerIndex(self,item)
    -- Devuelve el indice del "item" pasado por parametro.
    
    - obtenerItem(self,index)
    -- Devuelve el item (ej. ["a",0.3]) a partir del indice.
    
    - listarItems(self)
    -- Devuelve una lista con los elementos cargados, sin su probabilidad asociada.
       Por ej: ["a","b","c"]
    
    - listarProbabilidades(self)
    -- Devuelve una lista con los elementos y su probabilidad asociada.
       Por ej: [["a", 0.5], ["b", 0.3], ["c", 0.2]]
    
    - mostrarProbabilidades(self)
    -- Imprime en pantalla todos los elementos y sus probabilidades asociadas.
    """
    
    def __init__(self):
        self.conjunto=[]
        self.precision = 6 # precision de redondeo
                    
    def cargarDatos(self,*datos):
        #cargar datos distribuye la misma probabilidad a todos los elementos.
        if(self.esLista(datos[0])):
            datosNuevos = datos[0]
        else:
            datosNuevos = datos
            
        self.conjunto = []
        probabilidad = 1.0/len(datosNuevos)
        desde = 0.0
        hasta = 0.0
        for dato in datosNuevos:
            hasta = probabilidad
            self._agregarItemConDelta(dato,desde,hasta + desde)
            desde += hasta
            
    def cargarProbabilidades(self):
        correcto = False
        for dato in self.conjunto:
            dato[1] = [-1,-1]
            
        while not(correcto):
            restante = 1.0
            desde = 0.0
            hasta = 0.0
            for i,dato in enumerate(self.conjunto):
                if(restante > 0.0):
                    print "porcentaje restante: " + str(restante)
                    print "item: " + str(dato[0])
                    probabilidad = validador.ingresar(float,validador.entre,0.0,restante)
                    
                    if(probabilidad == 0.0):
                        dato[1] = [-1,-1]
                    else:
                        dato[1] = [desde,probabilidad + desde]
                        
                    restante = round(restante - probabilidad, self.precision)
                    print restante
                    desde += probabilidad 
                else:
                    # esto es: si me quede sin porcentaje a repartir y me faltan elementos por asignar
                    if(i == len(self.conjunto) - 1):
                        correcto = True
                        break
            
            if(restante == 0.0):            
                correcto = True
            
            if (restante > 0.0):
                print "----------------------------------------"
                print "Error al cargar probabilidades"
                print "El total debe ser exactamente igual a 1" 
                print "----------------------------------------"
                
        print self.conjunto
    
    def cargarTodoDesdeArchivo(self,ruta):
        try:
            archivo = open(ruta, "r")

            nuevosItems = [[linea.split(" ")[0], float(linea.split(" ")[1])] for linea in archivo.readlines()]
            
            probTotal = reduce(lambda x,y: x+y, [item[1] for item in nuevosItems])
            if (probTotal != 1.0):
                print "La probabilidad total difiere de 1.0, la actualizacion es ignorada. \n por favor revisar el documento."
                
            else:
                self.cargarTodo(nuevosItems)
            
            archivo.close()  
            
        except IOError:
            print "no pudo abrirse el archivo: " + ruta
        
    def cargarTodo(self,*datos):
        if(self.esLista(datos[0])):
            datosNuevos = datos[0]
        else:
            datosNuevos = datos
            
        self.conjunto = []
        restante = 1.0
        desde = 0.0
        hasta = 0.0
        
        for dato in datosNuevos:
            if(restante > 0.0): # si todavia tengo probabilidad para repartir
                if(dato[1] == 0.0): # si me llega una probabilidad de 0.0, el elemento se marca con -1 -1 para que no sea tenido en cuenta.
                    self._agregarItemConDelta(dato[0],-1,-1)
                    
                else:
                    if(round(restante - dato[1], self.precision) < 0.0): # Si algun elemento sobrepasa el 1.0, lo trunco.
                        print "------------------------------------------------------"
                        print "guarda!, se trunco el elemento: " + str(dato[0]) + " a un valor de " + str(restante)
                        print "los siguientes elementos tendran probabilidad = 0.0"
                        print "------------------------------------------------------"
                        dato[1] = restante
                        
                    hasta = dato[1] + desde
                    self._agregarItemConDelta(dato[0],desde,hasta)
                    desde = hasta
                    restante -= dato[1]
            else:
                self._agregarItemConDelta(dato[0],-1,-1)
                
    def generar(self):
        choice = random.random()
        for dato in self.conjunto:
            if(choice >= dato[1][0] and choice < dato[1][1]):
                return dato[0]

    def calcularDistribucion(self,conjunto,ruta):
        listado = []
        for dato in conjunto:
            listado.append([dato.lower(),0])
        
        try:
            archivo = open(ruta, "r")
            contenido = archivo.read().lower()
            
            for item in listado:
                item[1] = contenido.count(item[0])
                
            archivo.close()
            
        except IOError:
            print "no pudo abrirse el archivo: " + ruta
            
        total = reduce(lambda x, y: x + y, [item[1] for item in listado])
        print total
        listadoProbs = map(lambda x: [x[0], x[1]/float(total)],listado)
        
        self.cargarTodo(listadoProbs)
        
    def chequearValores(self):
        vueltas = 1000000
        listado = []
        for dato in self.conjunto:
            listado.append([dato[0],0])
        
        startTime = time.time()
        
        for i in range(0, vueltas):
            resultado = self.generar()
            for dato in listado:
                if (resultado == dato[0]):
                    dato[1] += 1
                    
                    
        endTime = time.time()
        elapsedTime = endTime-startTime
        print "----------------------------------------------------------------"
        for dato in listado:
            print "Elemento: " + str(dato[0]), "Ocurrencias: " + str(dato[1]) , "Porcentaje: " + str(dato[1]/float(vueltas) * 100) + "%"
            
        print "casos de prueba: " + str(reduce(lambda x, y: x+y, [cont[1] for cont in listado]))
        print "Tiempo de generacion: " + str(elapsedTime)
        print "----------------------------------------------------------------"
            
    def _agregarItemConDelta(self,dato,desde,hasta):
        self.conjunto.append([dato,[round(desde,self.precision),round(hasta,self.precision)]])
        
    def reestablecerDatos(self):
        self.cargarDatos(self.listarItems())
    
    def compensar(self,item):
        #item = ["a",0.3]
        indiceValorViejo = self.obtenerIndex(item[0])                  # encuentro el index del item en self.conjunto
        valorViejo = self.listarProbabilidades()[indiceValorViejo][1]  # obtengo la probabilidad actual
        probASumar = (valorViejo - item[1]) / (len(self.conjunto) - 1) # calculo el valor a restar a los elementos restantes
        
        nuevoConjunto = map(lambda x: [x[0], x[1] + probASumar if x[0] != item[0] else item[1]], self.listarProbabilidades())
        
        self.cargarTodo(nuevoConjunto)
    
    def esLista(self,objeto):
        if(type(objeto) == type([]) or type(objeto) == type(()) or type(objeto) == type(set())):
            return True
            
        return False
        
    def obtenerIndex(self,item):
        return self.listarItems().index(item)
    
    def obtenerItem(self,index):
        return self.listarProbabilidades()[index]
    
    def listarItems(self):
        return [elemento[0] for elemento in self.conjunto]
    
    def listarProbabilidades(self):
        return [[elemento[0], elemento[1][1] - elemento[1][0]] for elemento in self.conjunto]
 
    def mostrarProbabilidades(self):
        Generales.enumerarLista(map(lambda x: str(x[0]) + " --> " + str(x[1]),self.listarProbabilidades()))
 
# a = Probabilidad()

# a.cargarDatos("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z")
# print a.conjunto

# a.cargarTodo(["a",0.5],["b",0.0],["c",0.4],["d",0.1],["e",0.5])
# print a.conjunto

# a.cargarTodo(["a",0.5],["b",0.1],["c",0.4])
# print a.conjunto

# a.cargarProbabilidades()

# word = ""
# for i in range(0,7):
    # word += a.generar()
# print word    

# a.chequearValores()
