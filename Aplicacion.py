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
					salir = True
					
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
	"""
	def __init__(self,appnombre,version,aplicacionGrafica=False,**args):
		#Variables de programa
		self.appNombre = appnombre
		self.version = version
		self.vars = {}
		self.postFunciones = []	
		self.ancho = 0
		self.alto = 0
		
		#Variables de usuario
		if(aplicacionGrafica):
			self.vars["ratio"]  = Variable([1,1],self.modifTamano,minimo=[1,1])
			self.vars["factorRatio"] = Variable(50,self.modifTamano,minimo=2)
			self.vars["colorFondo"] = Variable([0,0,0],self.modifColor,minimo=[0,0,0],maximo=[255,255,255])
		
		self.vars["filesPath"] = Variable("C:\\Python27\\" + "ArchivosGenerados" + self.appNombre,self.modifGenerico)
		self.vars["outFile"] = Variable(self.appNombre + "Out.txt",self.modifGenerico)
		self.vars["logFile"] = Variable(self.appNombre + "Log.txt",self.modifGenerico)
		
		#Genero el menu
		titulo = "--- " +self.appNombre + " " + self.version + " ---"
		subtitulo = "-" * len(titulo)
		self.menu = Nodo(titulo,subtitulo,
					Leaf("Modificar parametros","Parametros modificables por el usuario",self.modificar),
					Leaf("Ver parametros","", self.variables),
					Nodo("Ver Archivos","Archivos generados por " + self.appNombre + ":",
						Leaf("Archivo de Salida","Archivo generado por el programa",self.verFile),
						Leaf("Archivo de Logs","Archivo con todos los logs del programa",self.verLog),
						),
					Leaf("Que es esto?","",self.ayuda),
					Leaf("Salir",":D",self.salir)
					,root=True
				)
		# Crea el directorio de trabajo
		self.crearFilesPath()
		
		if(aplicacionGrafica):
			# Calcular ancho y alto en pixeles a partir del ratio y factorRatio
			self.calcularAnchoAlto()
			
			#Creo un pixelArray		
			self.screen = pygame.Surface((self.ancho,self.alto))
			self.pixelArray = pygame.PixelArray(self.screen)
					
			#Creo el Queue
			self.queue = Queue.Queue()		

			#Thread de Pantalla
			self.pantalla = Pantalla(self.ancho,self.alto,self.appNombre,self.vars["colorFondo"].valor,self.queue)
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
	
	def ejecutarPostFunciones(self):
		for funcion in self.postFunciones:
			funcion()
	
	def agregarMenu(self,posicion,nodo):
		self.menu.agregar(posicion,nodo)
	
	def log(self,*datos):
		# archivo  = open(self.vars["filesPath"].valor + "\\" + self.vars["logFile"].valor,"a")
		archivo  = open(self.vars["filesPath"].valor + "\\" + self.vars["logFile"].valor,"a")
		
		timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " -- "
		archivo.write(timestamp)
		
		for i in range(0,len(datos)):			
			if (i == len(datos)-1):
				archivo.write(datos[i])
			else:
				archivo.write(datos[i] + ", ")
				
		archivo.write("\n")	
		archivo.close()
	
	def variables(self):
		keys = self.vars.keys()
		keys.sort()
		for key in keys:
			print "-" + key + ":",self.vars[key].valor

	def modificar(self):
	# Si uso el metodo modificar; para que el usuario ingrese valores, params estara vacio.
	# Si por el contrario llamo directamente a la funcion modificadora (por ej modifZoom) hay que pasarle el valor nuevo. el dato key en ese caso no cumple funcion.
	
		salir = False
		while(not salir):
			print "variable a modificar:\n"
			for (i,clave) in enumerate(self.vars.keys()):
				print str(i+1) + ") " + clave, ":",self.vars[clave].valor 
			print str(i+2) + ") Volver" 
			# key = validador.ingresar(str,validador.igual,self.vars.keys())
			key = validador.seleccionar(self.vars.keys()+["Volver"])
			if(key == "Volver"):
				salir = True
			else:
				print key
				print "valor actual: ", self.vars[key].valor
				self.vars[key].modificador(key)
				self.ejecutarPostFunciones()
			

	def modifGenerico(self,key):
		tipo = type(self.vars[key].valor)
		self.vars[key].valor = validador.ingresar(tipo,validador.entre,self.vars[key].minimo,self.vars[key].maximo)		
	
	def modifValoresPosibles(self,key):
		print "valores posibles: "
		for i in range(0,len(self.vars[key].valoresPosibles)):
			print str(i+1) + ") " + str(self.vars[key].valoresPosibles[i])
		
		
		self.vars[key].valor = validador.seleccionar(self.vars[key].valoresPosibles)
	
	def menuPrincipal(self):
		salir = False
		while (not salir):
			salir = True if self.menu.evaluar() == "SALIR" else False
	
	def ayuda(self):
		print "Manual de usuario."
		print "--------------------------"
		print "-- en construsion vio ----"
		print "--------------------------"
	
	def verFile(self):
		fname = self.vars["filesPath"].valor + "\\" +  self.vars["outFile"].valor
		if(os.path.isfile(fname)):
			os.startfile(fname)
		else:
			print "Archivo no encontrado"
		
	def verLog(self):
		fname = self.vars["filesPath"].valor + "\\" +  self.vars["logFile"].valor
		if(os.path.isfile(fname)):
			os.startfile(fname)
		else:
			print "Archivo no encontrado"
	
	def enumerarLista(self,lista):
		for i in range(0,len(lista)):
			print str(i+1) + ") " + lista[i]
	
	def salir(self):
		self.log("cerrando" + self.appNombre)
		return "SALIR"
				
		
if __name__ == '__main__':	
	a = Aplicacion("App","1.0.0")
	print "antes de menu principal"
	a.menuPrincipal();		
		
