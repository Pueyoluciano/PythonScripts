import os
import threading
import Queue
import pygame
from validador import *
from fractions import gcd
from datetime import datetime
from Menu import *
from Variable import *
        
        
class Polling:  
    def __init__(self,accion,**parametros):
        self.accion = accion
        self.parametros = parametros
    

class Pantalla(threading.Thread):
    def __init__(self,ancho,alto,titulo,colorfondo,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        pygame.init()
        self.screen = pygame.display.set_mode((ancho,alto))
        pygame.display.set_caption(titulo)
        self.pixelArray = pygame.PixelArray(self.screen)
        self.clock = pygame.time.Clock()
        self.colorfondo = colorfondo
        self.acciones = {"actualizar":self.actualizar,"resize":self.resize}
        
    def run(self):
        Salir = False
        
        while not Salir:
            self.tick = self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Salir = True
                    
            polling = self.queue.get()
            if (polling.accion in self.acciones):
                self.acciones[polling.accion](polling.parametros)           
            
    def actualizar(self,parametros):
        if(parametros["refresco"]):
            self.screen.fill(self.colorfondo)
        
        # self.screen.blit(parametros["pixelarray"].surface,(0,0))
        self.pixelArray = parametros["pixelarray"]
        pygame.display.flip()
    
    def resize(self,parametros):
        self.screen = pygame.display.set_mode((parametros["ancho"],parametros["alto"]))
        self.pixelArray = pygame.PixelArray(self.screen)
    
        
class Aplicacion:

    """
    Clase Aplicacion es un esqueleto para armar aplicaciones con manejo a traves de la consola.
    provee manejo de variables modificables por el usuario, pudiendo listarlas y/o modificarlas,
    y un menu que recorre todas las acciones posibles.

    Los componentes principales son:
    - Variables no modificables por el usuario, como appNombre y Version.
    - Variables modificables por el usuario, como filesPath y outFile.
    |- Cada variable tiene una estructura donde se guarda su valor actual, un diccionario con flags,
       su funcion modificadora, y si corresponde, minimo y/o maximo.
    - Menu con acciones basicas, como ver y modificar parametros, un texto de ayuda.
      A su vez tiene para abrir el archivo de logs y el archivo de salida, si es que tiene.
      
    Para crear una nueva Aplicacion:
    -1) hay que crear una nueva clase que herede de Aplicacion.
    -2) el metodo init NO debe ser sobreescrito.
    -3) agregar el metodo iniciar con la siguiente cabecera:
    |
    |-  def iniciar(self,**args):
    |
    |-  en este metodo hay que crear las variables de usuario y de programa.
    |-  las variables de usuario se agregan a self.vars de la siguiente forma:
    |
    |-- self.vars["varibleUsuario1"] = Variable("valorDelaVariable",self.modificadorVariable1,flags={"bandera1":true})
    |-- para detalles sobre Variable.py ver la documentacion.
    
    -4) Luego hay que crear los items del menu: 
    |- se crean los Leaf y Nodos que sean necesarios.
    |- para agregar items al menu:
    |
    |-  self.agregarMenu(0,Leaf("accion1","descripcion de la accion1",self.metodoQueCumpleLaAccion))
    |-  para detalles sobre Menu.py ver la documentacion.
    
    -5) Por ultimo se agregan las PostFunciones, que son las que se ejecutan luego de realizar modificaciones a las variables de usuario.
    |- para agregar postFunciones:
    |
    |-   self.agregarPostFunciones(self.postFuncion1,self.postFuncion2)
    
    -6) Todas las funciones de modificacion deben tener como parametros de entrada una de estas posibilidades:
    |
    |-  self.modificador1(self,key,*params):
    |-  self.modificador2(self,key):
    
    -7) Para mostrar un mensaje personalizado al salir hay que sobreescribir el metodo salirPrint.
    |
    |-  self.salirPrint(self): print "texto que se muestra al salir"

    -8) Para que la aplicacion pueda ser ejecutada:
    |
    |-  if __name__ == '__main__':
    |-      a = NombreClase("NombreAPP","Version",esAplicacionGrafica?,param1=1,param2=2)
    |-      a.menuPrincipal()   
    |
    |-  param1 y param2 son los que va a recibir el metodo iniciar detallado arriba,en forma de diccionario.
    |- esAplicacionGrafica es un Boolean, si esta en True levanta un pygame.
    
    -9) Si es una aplicacion Grafica:
    |- en la instanciacion de la clase hay que indicarselo con un True(Ver item anterior).
    |- la variable de programa self.pixelArray[x,y] es el mapa de pixeles de la pantalla.
    |- para actualizar la pantalla se llama al metodo:
    |
    |-  self.actualizarPantalla()
    
    -El metodo self.log(self,*datos) permite loguear, guardando en el archivo referenciado en self.vars["logFile].
    -El metodo self.ayuda(self) debe ser sobreescrito para mostrar un manual de usuario o cualquier referencia que se quiera, no es obligatorio.
    -El metodo self.generarNombreValido(self,nombre) sirve para no pisar archivos al crearlos. recibe un nombre y devuelve el nombre con el numero
        de repeticion que corresponda, por ejemplo, si tenemos pruebas.txt, devuelve pruebas(1).txt.
    -El metodo self.funcionDeInicioLoop(self) se ejecuta antes de graficar el menu, sirve para mostrar datos o informacion relevante que tiene que ser
        vista repetidamente. la funcion que hereda de Aplicacion.py tiene que sobreescribirla para hacer uso de la misma.
    -El metodo verArchivo(self,nombre,*ruta) permite editar archivos. si no le pasas ruta, abre nombre desde filespath, sino lo abre desde la ruta.
    -El metodo pausa(self) sirve para esperar una confirmacion del usuario.
    -El metodo funcionDeInicioLoop(self) debe ser sobreescrito por la aplicacion hija, y se ejecuta al principio de cada Loop,
    permitiendo mostrar algun tipo de info en cada vuelta.
    """
    
    def __init__(self,appnombre,version,aplicacionGrafica=False,**args):
        #Variables de programa
        self.appNombre = appnombre
        self.version = version
        self.vars = {}
        self.postFunciones = [] 
        self.ancho = 0
        self.alto = 0
        self.appGrafica = aplicacionGrafica
        
        #Variables de usuario
        if(self.appGrafica):
            self.colorFondo = [0,0,0]
            fratio = args["factorRatio"] if "factorRatio" in args.keys() else 50
            ratio = args["ratio"] if "ratio" in args.keys() else [1,1] 
            self.vars["ratio"]  = Variable(ratio,self.modifTamano,minimo=[1,1],orden=200)
            self.vars["factorRatio"] = Variable(fratio,self.modifTamano,minimo=2,orden=201)

        self.vars["rootPath"] = Variable(os.getcwd() + "\ArchivosGenerados" + self.appNombre,self.modifPath,orden=202)
        self.vars["filesPath"] = Variable(self.vars["rootPath"].valor,self.modifPath,orden=203)
        self.vars["outFile"] = Variable(self.appNombre + "Out.txt",self.modifPath,orden=204)
        self.vars["logFile"] = Variable(self.appNombre + "Log.txt",self.modifPath,orden=205)
        
        #Genero el menu
        titulo = "--- " +self.appNombre + " " + self.version + " ---"
        subtitulo = "-" * len(titulo)
        self.menu = Nodo(titulo,subtitulo,
                    Leaf("Ver parametros","Parametros actuales de la aplicacion", self.mostrarVariables),
                    Leaf("Modificar parametros","Parametros modificables por el usuario",self.modificar),
                    Nodo("Ver Archivos","Archivos generados por " + self.appNombre + ":",
                        Leaf("Archivo de Salida","Archivo generado por el programa",self.verFile),
                        Leaf("Archivo de Logs","Archivo con todos los logs del programa",self.verLog),
                        ),
                    Leaf("Que es esto?","",self.ayudaAplicacion),
                    Leaf("Salir","Cerrando " + self.appNombre,self.salir)
                    ,root=True
                )
        # Crea el directorio de trabajo
        self.crearFilesPath()
        
        if(self.appGrafica):
            # Calcular ancho y alto en pixeles a partir del ratio y factorRatio
            self.calcularAnchoAlto()
            
            #Creo un pixelArray     
            self.screen = pygame.Surface((self.ancho,self.alto))
            self.pixelArray = pygame.PixelArray(self.screen)
                    
            #Creo el Queue
            self.queue = Queue.Queue()      

            #Thread de Pantalla
            self.pantalla = Pantalla(self.ancho,self.alto,self.appNombre,self.colorFondo,self.queue)
            self.pantalla.daemon = True
            self.pantalla.start()
            self.log("Iniciando Thread Pantalla")
        
            self.agregarPostFunciones(self.calcularAnchoAlto,self.actualizarTamanoPantalla)
        
        self.iniciar(**args)

        self.log("Iniciando" + self.appNombre)
    
    def iniciar(self,**args):
        # Este metodo tiene que ser sobreescrito en la clase que herede de Aplicacion.
        pass

    def crearFilesPath(self):
        if not os.path.isdir(self.vars["filesPath"].valor):
            os.mkdir(self.vars["filesPath"].valor)
        os.chdir(self.vars["filesPath"].valor)
    
    def actualizarTamanoPantalla(self):
        self.screen = pygame.Surface((self.ancho,self.alto))
        self.pixelArray = pygame.PixelArray(self.screen)
        self.queue.put(Polling("resize",pixelarray=self.pixelArray,ancho=self.ancho,alto=self.alto))
        
    def calcularAnchoAlto(self):
        self.ancho = self.vars["ratio"].valor[0] * self.vars["factorRatio"].valor 
        self.alto  = self.vars["ratio"].valor[1] * self.vars["factorRatio"].valor
    
    def actualizarPantalla(self,refresh=True):
        self.queue.put(Polling("actualizar",pixelarray=self.pixelArray,refresco=refresh))
    
    def agregarPostFunciones(self,*funciones):
        for funcion in funciones:
            self.postFunciones.append(funcion)

    def agregarMenu(self,posicion,nodo):
        self.menu.agregar(posicion,nodo)
    
    def log(self,*datos):
        # archivo  = open(self.vars["filesPath"].valor + "\\" + self.vars["logFile"].valor,"a")
        archivo  = open(self.vars["rootPath"].valor + "\\" + self.vars["logFile"].valor,"a")
        
        timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " -- "
        archivo.write(timestamp)
        
        for i in range(0,len(datos)):           
            if (i == len(datos)-1):
                archivo.write(datos[i])
            else:
                archivo.write(datos[i] + ", ")
                
        archivo.write("\n") 
        archivo.close()
    
    #Obtener tupla de nombres y valores del diccionario de variables
    def obtenerNombreValorVariables(self):
        return sorted(self.vars.items(), key=lambda x: x[1].orden)
        
    #Obtener solo el nombre del diccionario de variables en una lista
    def obtenerNombreVariables(self):
        return [key[0] for key in self.obtenerNombreValorVariables()]
    
    #Obtener solo el valor del diccionario de variables en una lista
    def obtenerValorVariables(self):
        return [value[1] for value in self.obtenerNombreValorVariables()]
        
    def mostrarVariables(self):
        print "\n"
        self.espaciador()
        variables = self.obtenerNombreValorVariables()
        for i in range(0,len(variables)):
            print str(i+1) + ") " + str(variables[i][0]) + ":",(variables[i][1])
        print str(i+2) + ") Volver" 
        self.espaciador()
    
    def modificar(self):
    # Si uso el metodo modificar; para que el usuario ingrese valores, params estara vacio.
    # Si por el contrario llamo directamente a la funcion modificadora (por ej modifZoom) hay que pasarle el valor nuevo. el dato key en ese caso no cumple funcion.
    
        salir = False
        while(not salir):
            self.mostrarVariables()
            # for (i,clave) in enumerate(self.vars.keys()):
                # print str(i+1) + ") " + clave, ":",self.vars[clave].valor 
            
            # key = validador.ingresar(str,validador.igual,self.vars.keys())
            key = validador.seleccionar(self.obtenerNombreVariables()+["Volver"])
            if(key == "Volver"):
                salir = True
            else:
                print key
                print "valor actual: ", self.vars[key].valor
                self.vars[key].modificador(key)
        self.ejecutarPostFunciones()

    def ejecutarPostFunciones(self):
        for funcion in self.postFunciones:
            funcion()               

    def modifGenerico(self,key,*params):
        if(len(params) == 0):
            tipo = type(self.vars[key].valor)
            self.vars[key].valor = validador.ingresar(tipo,validador.entre,self.vars[key].minimo,self.vars[key].maximo)     
        else:
            self.vars[key].valor = params[0]
        
    def modifValoresPosibles(self,key):
        print "valores posibles: "
        for i in range(0,len(self.vars[key].valoresPosibles)):
            print str(i+1) + ") " + str(self.vars[key].valoresPosibles[i])  
        
        self.vars[key].valor = validador.seleccionar(self.vars[key].valoresPosibles)
    
    def modifPath(self,key):
        path = validador.ingresar(str)
        if not os.path.isdir(path):
            os.mkdir(path)
            # os.chdir(nombreCarpeta)   
        self.vars[key].valor = path
    
    def funcionDeInicioLoopAplicacion(self):
        self.espaciador()
        self.funcionDeInicioLoop()
        self.espaciador()
    
    def funcionDeInicioLoop(self):
        pass

    def menuPrincipal(self):
        salir = False
        while (not salir):
            self.funcionDeInicioLoopAplicacion()
            salir = True if self.menu.evaluar() == "SALIR" else False
    
    def ayudaAplicacion(self):
        self.espaciador()
        print "--- Que es esto? ---"
        print self.appNombre
        print "Version: " + self.version
        self.ayuda()
        self.pausa()
    
    def ayuda(self):
        print "Manual de usuario."
        print "--------------------------"
        print "------ FILL ME PLZ -------"
        print "--------------------------"
    
    def verArchivo(self,nombre,*ruta):
        self.espaciador()
        print ruta
        if(ruta == ()):
            if(os.path.isfile(self.vars["filesPath"].valor + "\\" + nombre)):
                os.startfile(self.vars["filesPath"].valor + "\\" + nombre)
            else:
                print "Archivo no encontrado"
        else:   
            if(os.path.isfile(ruta[0] + "\\" + nombre)):
                os.startfile(ruta[0] + "\\" + nombre)
            else:
                print "Archivo no encontrado"
        self.espaciador()
        
    def verFile(self):
        self.espaciador()
        fname = self.vars["rootPath"].valor + "\\" +  self.vars["outFile"].valor
        if(os.path.isfile(fname)):
            os.startfile(fname)
        else:
            print "Archivo no encontrado"
        self.espaciador()
        
    def verLog(self):
        fname = self.vars["rootPath"].valor + "\\" +  self.vars["logFile"].valor
        if(os.path.isfile(fname)):
            os.startfile(fname)
        else:
            print "Archivo no encontrado"
    
    def generarNombreValido(self,nombre):
        seguir = True
        contador = 0
        path,ext = os.path.splitext(nombre)
        aux = path
        
        while(seguir):
            if(not os.path.exists(aux+ext)):
                seguir = False
            else:
                contador +=1
                aux = path + "(" + str(contador) + ")"
                
        if(contador != 0):
            nombre = aux+ext
            
        return nombre

    def pausa(self):
        raw_input("...")
        
    def espaciador(self):
        print "-----------------------------------------------------------------"
        
    def salir(self):
        self.log("cerrando" + self.appNombre)
        self.salirPrint()
        if(self.appGrafica):
            self.queue.put(Polling("salir"))
        return "SALIR"
                
    def salirPrint(self):
        print "adios"
    
    
if __name__ == '__main__':  
    a = Aplicacion("App","1.0.0")
    a.menuPrincipal();      
        
