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
        
        self.reglasActuales = ["tresVocales","dosConsonantes","qSiempreConU","quSiempreConEI"]
        
        self.motor = Reglas.MotorReglas()
        self.motor.agregarReglas([self.listado.obtenerItem(regla) for regla in self.reglasActuales])
        
        #variables de usuario   
        self.vars["longitud"] = Variable(5,self.modifGenerico,minimo=0,maximo=20,orden=0)
        self.vars["archivoExterno"] = Variable("Probabilidades.txt",self.modifGenerico,orden=1)
        
        #Items del Menu
        self.agregarMenu(0,Leaf("Crear nombre","Genera un nombre aleatorio en base a las reglas seteadas",self.crearNombre))
        self.agregarMenu(1,Leaf("Ver reglas","Listar reglas vigentes",self.verTodasReglas))
        self.agregarMenu(2,Leaf("Modificar reglas","agregar/quitar reglas para la generacion de nombres",self.modifReglas))
        self.agregarMenu(3,Leaf("Ver distribucion de letras","Distribucion de probabilidades asignada a cada letra",self.verDistribucion))
        
        self.agregarMenu(4,Nodo("Modificar distribucion de letras","",
                            Leaf("Manual","Modificar los valores de probabilidad de forma manual",self.modificarDistribucionManual),
                            Leaf("Desde archivo","Actualizar los valores de probabilidad levantando la informacion cargada en un archivo externo",self.modificarDistribucionArchivo)))
        
        #Funciones que se ejecutan luego de llamar a Modificar.
        #self.agregarPostFunciones()

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
                
            print "-> " + nombre
            print "otro nombre?"
            seguir = validador.ingresarSINO()
    
    def generarNombre(self,longitud):
        nombre = ""
        try:
            for i in range(0,longitud):
                nombre += self.motor.nuevaLetra(nombre)         
                
        except Exception as exc:
            # print exc.args[0] # mensaje de error que trae la exception
            traceback.print_exc()
        
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
                
    def verDistribucion(self):
        self.espaciador()
        listado = self.motor.probabilidades.listarProbabilidades()
        Generales.enumerarLista(map(lambda x: str(x[0]) + " --> " + str(x[1]),listado))
        
    def modificarDistribucionManual(self):
        menu = ["Restaurar Valores por defecto","Confirmar","Volver"]
        termine = False
        probs = pr.Probabilidad()
        probs.cargarTodo(list(self.motor.probabilidades.listarProbabilidades()))

        while not termine:
            self.espaciador()
            
            listado = map(lambda x: str(x[0]) + " --> " + str(x[1]), probs.listarProbabilidades()) + menu
            Generales.enumerarLista(listado)
            self.espaciador()
            
            print "Seleccione el item a modificar (por numero de orden)"
            indice = validador.ingresar(int,validador.entre, 1, len(listado))
            
            if(indice != len(listado)):         # -- Volver
                if(indice == len(listado) - 1): # -- Confirmar
                    self.motor.probabilidades.cargarTodo(probs.listarProbabilidades()) #Actualizo los datos
                    termine = True
                    
                else:
                    if(indice == len(listado) - 2): # -- Restaurar Valores por defecto
                        probs.reestablecerDatos()
                    else:
                        print "Cargue el nuevo valor: (entre 0 y 1)"
                        
                        elemento = probs.obtenerItem(indice - 1)
                        
                        valor = validador.ingresar(float, validador.entre, 0.0,1.0)
                        probs.compensar([elemento[0],valor])
                        print probs.mostrarProbabilidades()
            else:
                termine = True
            
    def modificarDistribucionArchivo(self):
        file = self.vars["filesPath"].valor + "\\" + self.vars["archivoExterno"].valor
        self.motor.probabilidades.cargarTodoDesdeArchivo(file)
        self.espaciador()
        print "Archivo utilizado: " + file
        self.espaciador()
        print "Nuevos valores:"
        self.motor.probabilidades.mostrarProbabilidades()

    def ayuda(self):
        self.espaciador()
        print " La parte mas dificil de cualquier proyecto/idea/cosa es ponerle nombre."
        print " " + self.appNombre + " toma la dificil tarea por vos,"
        print " y te genera aleatoriamente nombres para que puedas elegir"
        print " el que mas te guste."
        print " Configura las reglas que mejor te plazcan, y listo."
        self.espaciador()
    
    #Texto personalizado de salida. 
    def salirPrint(self):
        self.espaciador()
        print "Siempre lleva un nombre contigo:"
        print self.generarNombre(random.randint(self.vars["longitud"].minimo + 3, self.vars["longitud"].maximo))
        
if __name__ == '__main__':
    a = CreadorNombres("GeneradorDeNombres","2.0.0",False)
                    
    a.menuPrincipal()       
