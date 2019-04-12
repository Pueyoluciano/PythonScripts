import os
import random
import traceback
import Aplicacion
import Reglas
import Probabilidades as pr
from Letras import Letras
from Generales import Generales
from Menu import *
from Variable import *
from validador import *
#------------------------------------------------
#--------------- TODO ---------------------------
#------------------------------------------------


#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
class CreadorNombres(Aplicacion.Aplicacion):

    """
    FILLME
    """
    
    def iniciar(self,**args):   
        #variables de programa
        self.vocales = Letras.vocales
        self.consonantes = Letras.consonantes
        self.letras = Letras.letras
        self.listado = Reglas.ListadoReglas.contenido
        
        self.reglasActuales = ["dosVocales","unaConsonante","qSiempreConU","quSiempreConEI"]
        
        self.motor = Reglas.MotorReglas()
        self.motor.agregarReglas([self.listado.obtenerItem(regla) for regla in self.reglasActuales])
        
        #variables de usuario   
        self.vars["longitud"] = Variable(5,self.modifGenerico,minimo=0,maximo=20,orden=0)
        self.vars["archivoExterno"] = Variable("Mapeo_Probabilidades.txt",self.modifGenerico,orden=1)
        self.vars["archivoExclusiones"] = Variable("Exclusiones.txt",self.modifGenerico,orden=2)
        
        #Items del Menu
        self.agregarMenu(0,Leaf("Crear nombre","Genera un nombre aleatorio en base a las reglas seteadas",self.crearNombre))
        self.agregarMenu(1,Leaf("Ver reglas","Listar reglas vigentes",self.verTodasReglas))
        self.agregarMenu(2,Leaf("Modificar reglas","agregar/quitar reglas para la generacion de nombres",self.modifReglas))
        self.agregarMenu(3,Leaf("Ver distribucion de letras","Distribucion de probabilidades asignada a cada letra",self.verDistribucion))
        self.agregarMenu(4,Nodo("Modificar distribucion de letras","Elija una de las formas de modificar la distribucion",
                            Leaf("Manual","Modificar los valores de probabilidad de forma manual",self.modificarDistribucionManual),
                            Leaf("Desde archivo","Actualizar los valores de probabilidad levantando la informacion cargada en un archivo externo",self.modificarDistribucionArchivo),
                            Leaf("Calcular distribucion", "Toma un archivo y calcula la distribucion de letras en el mismo",self.calcularDistribucion)
                            ))
                            
        self.agregarMenu(5,Leaf("Exportar distribucion de letras","Escribe el archivo " + self.vars["archivoExterno"].valor +" con la distribucion actual",self.exportarDistribucion))
        
        self.agregarMenu(6,Leaf("Ver Strings excluidos","Lista de Strings no permitidos",self.verExclusiones))
        self.agregarMenu(7,Nodo("Modificar Strings excluidos","Selecciones el modo de modificacion",
                            Leaf("Manual","",self.cargarExclusionesManual),
                            Leaf("Desde archivo","",self.cargarExclusionesArchivo),
                            Leaf("Quitar todo","",self.quitarTodasExlcusiones)
                            ))
        
        #Funciones que se ejecutan luego de llamar a Modificar.
        self.agregarPostFunciones(self.logParametrosActuales)
        
        self.logParametrosActuales()

    def logParametrosActuales(self):
        self.log(self.textoEspaciador)
        self.log("--- Actualizacion de datos --------------------------------------")
        
        self.log("--- Variables de programa ---------------------------------------")
        for nombre, valor in self.vars.items():
            self.log(nombre, str(valor))

        self.log("--- Reglas ------------------------------------------------------")
        for regla in self.motor.reglasActivas():
            self.log(regla)
        
        self.log("--- Distribucion ------------------------------------------------")
        for probs in self.motor.probabilidades.listarProbabilidades():
            self.log(probs[0], str(probs[1]))
        
        self.log(self.textoEspaciador)     
        
    def crearNombre(self):
        seguir = True
        while(seguir):
            #Si la Longitud es 0 elije una longitud Random
            if (self.vars["longitud"].valor == 0):
                longitud = random.randint(self.vars["longitud"].minimo + 3, self.vars["longitud"].maximo)
            else:
                longitud = self.vars["longitud"].valor
            
            #Genero todo el nombre
            nombre = self.generarNombre(longitud)
            nombre = nombre[0].upper() + nombre[1:]
            print("-> " + nombre)
            print("otro nombre?")
            seguir = validador.ingresarSINO()
    
    def generarNombre(self,longitud):
        nombre = ""
        try:
            for i in range(0,longitud):
                nombre += self.motor.nuevaLetra(nombre)         
                
        except Exception as exc:
            # print(exc.args[0]) # mensaje de error que trae la exception
            traceback.print_exc()
        
        self.log("Nuevo nombre: " + nombre)
        
        return nombre
        
    def verTodasReglas(self):
        self.espaciador()
        Generales.enumerarLista(self.motor.reglasActivas())
        
    def modifReglas(self):
        listaTemp = self.reglasActuales[:]
        seguir = True
        menu = ["Confirmar", "volver"]
        
        self.espaciador()
        while(seguir):
        
            listadoTemporal = self.motor.reglasActivas(listaTemp) + menu
            Generales.enumerarLista(listadoTemporal)
            self.espaciador()
            
            respuesta = validador.seleccionar([regla.nombre for regla in self.listado.contenido] + menu)
            if(respuesta != menu[1]):
                if(respuesta != menu[0]):
                    if(respuesta in listaTemp):
                        listaTemp.remove(respuesta)
                    else:
                        listaTemp.append(respuesta)
                        
                else:
                    self.reglasActuales = listaTemp[:]
                    self.motor.limpiarReglas()
                    self.motor.agregarReglas([self.listado.obtenerItem(regla) for regla in self.reglasActuales])
                    seguir = False
            else:       
                seguir = False
        
        self.logParametrosActuales()
                
    def verDistribucion(self):
        self.espaciador()
        listado = self.motor.probabilidades.listarProbabilidades()
        Generales.enumerarLista(list(map(lambda x: str(x[0]) + " --> " + str(x[1]),listado)))
        
    def modificarDistribucionManual(self):
        menu = ["Restaurar Valores por defecto","Confirmar","Volver"]
        termine = False
        probs = pr.Probabilidad()
        probs.cargarTodo(list(self.motor.probabilidades.listarProbabilidades()))

        while not termine:
            self.espaciador()
            
            listado = list(map(lambda x: str(x[0]) + " --> " + str(x[1]), probs.listarProbabilidades()) + menu)
            Generales.enumerarLista(listado)
            self.espaciador()
            
            print("Seleccione el item a modificar (por numero de orden)")
            indice = validador.ingresar(int,validador.entre, 1, len(listado))
            
            if(indice != len(listado)):         # -- Volver
                if(indice == len(listado) - 1): # -- Confirmar
                    self.motor.probabilidades.cargarTodo(probs.listarProbabilidades()) #Actualizo los datos
                    termine = True
                    
                else:
                    if(indice == len(listado) - 2): # -- Restaurar Valores por defecto
                        probs.reestablecerDatos()
                    else:
                        print("elemento: " + str(probs.obtenerItem(indice - 1)[0]))
                        print("valor actual: " + str(probs.obtenerItem(indice - 1)[1]))
                        print("Cargue el nuevo valor: (entre 0 y 1)")
                        
                        elemento = probs.obtenerItem(indice - 1)
                        
                        valor = validador.ingresar(float, validador.entre, 0.0,1.0)
                        probs.compensar([elemento[0],valor])
                        print(probs.mostrarProbabilidades())
            else:
                termine = True
                
        self.logParametrosActuales()
        
    def modificarDistribucionArchivo(self):
        file = self.vars["filesPath"].valor + "\\" + self.vars["archivoExterno"].valor
        self.espaciador()
        # print("Archivo utilizado: " + file)
        print("Se utilizara el archivo: " + file)
        print("Desea continuar?")
        
        if(validador.ingresarSINO()):
            self.motor.probabilidades.cargarTodoDesdeArchivo(file)
            self.espaciador()
            print("Nuevos valores:")
            self.motor.probabilidades.mostrarProbabilidades()
            
            self.logParametrosActuales()
        
    def exportarDistribucion(self):
        self.espaciador()
        nombre = os.path.abspath(self.vars["archivoExterno"].valor)
        
        print("Se utilizara el archivo: " + nombre)
        print("Desea continuar?")
        if(validador.ingresarSINO()):
    
            archivo = open(nombre,"w")
            
            self.espaciador()
            for elemento in self.motor.probabilidades.listarProbabilidades():
                archivo.write(elemento[0] + " " + str(elemento[1]) + "\n")
                
            archivo.close()   
        
            print("Se cargo la nueva data en: " + os.path.abspath(self.vars["archivoExterno"].valor))
    
    def calcularDistribucion(self):
        self.espaciador()
        conjunto = self.motor.probabilidades.listarItems()
        print("Seleccione un archivo para calcular las ocurrencias de letras: \n")
        self.motor.probabilidades.calcularDistribucion(conjunto,Generales.seleccionarArchivo(self.vars["filesPath"].valor))
        
        self.logParametrosActuales()
    
    def verExclusiones(self):
        self.espaciador()
        Generales.enumerarLista(self.motor.stringsExcluidos)
    
    def cargarExclusionesManual(self):
        pass
    
    def cargarExclusionesArchivo(self):
        self.espaciador()
        ruta = os.path.abspath(self.vars["archivoExclusiones"].valor)
        
        print("Se utilizara el archivo: " + ruta)
        
        print("Desea continuar?")
        if(validador.ingresarSINO()):
            
            archivo = open(ruta, "r")
            
            self.motor.quitarTodasExlcusiones()
            self.motor.agregarExclusiones(list(map(lambda x: x[0:-1] if "\n" in x else x, archivo.readlines())))
                
            print(self.motor.stringsExcluidos)
            archivo.close()
        
    def quitarTodasExlcusiones(self):
        self.espaciador()
        print("Se quitaran todas las excepciones, Desea continuar?")
        if(validador.ingresarSINO()):
            self.motor.quitarTodasExlcusiones()
            print("Se quitaron todas las Exlcusiones.")
        
    def ayuda(self):
        self.espaciador()
        print(" La parte mas dificil de cualquier proyecto/idea/cosa es ponerle nombre.")
        print(" " + self.appNombre + " toma la dificil tarea por vos,")
        print(" y te genera aleatoriamente nombres para que puedas elegir")
        print(" el que mas te guste.")
        print(" Configura las reglas que mejor te plazcan, y listo.")
        self.espaciador()
    
    #Texto personalizado de salida. 
    def salirPrint(self):
        self.espaciador()
        print("Siempre lleva un nombre contigo:")
        print(self.generarNombre(random.randint(self.vars["longitud"].minimo + 3, self.vars["longitud"].maximo)))
        
if __name__ == '__main__':
    a = CreadorNombres("GeneradorDeNombres","2.0.0",False)
                    
    a.menuPrincipal()