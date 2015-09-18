import os
import time
import pygame
import Aplicacion
from fractions import gcd
from datetime import datetime
from paletaColores import Paleta	
from Menu import *
from Variable import *
from validador import *
from Funcionesfractales import *
#------------------------------------------------
#--------------- TODO ---------------------------
#------------------------------------------------
# 1) EJECUCION EN PARARELO

# 2) IMPLEMENTAR LOGGING

# 3) MOSTRAR TIEMPOS DE EJECUCION:
# 3.1) CADA CIERTA CANTIDAD DE TIEMPO MOSTRAR EL PROGRESO.
# 3.2) CADA UN 25% LOGUEAR PROGRESO LOGRADO.

# 4) TESTER DE VEOLICDAD
# 4.1) CREAR UNA FUNCION QUE DEVUELVA SIEMPRE MAXIMAS ITERACIONES- PARA UN SET FIJO DE VARIABLES TOMAR TIEMPO.
# 4.2) IDEM 4.1) PERO CON FUNCION QUE DEVUELVA MINIMAS ITERACIONES.

# 5) SCHEDULER - PARA CREAR LISTAS DE EJECUCION.

#------------------------------------------------
#------------------------------------------------
#------------------------------------------------

def graficarPorcion(self,funcion,desdex,hastax,alto,planoComplejo,grilla,params):
	pixelArrayTemporal = []
	for x in range(desdex,hastax):
		pixelArrayTemporal.append([])
		for y in range(0,alto):
			# valor = funcion.calcular(planoComplejo[x][y],params)
			# pixelArrayTemporal[x-desdex].append(grilla[valor-1])
			print "asd"

	return pixelArrayTemporal
		

class Fractales(Aplicacion.Aplicacion):
	def iniciar(self,**args):	
		# self.listaFunciones= Funcion.listado # Diccionario con el listado de funciones.
		self.listaFunciones = Funciones()

		# Acciones scheduleables.
		self.scheduleables =[
		["graficar",self.graficar],
		["foto",self.foto],
		["sesion",self.sesion],
		["ascii",self.ascii],
		["modificarX",self.modifEjeX],
		["modificarY",self.modifEjeY],
		["modificarZoom",self.modifZoom],
		["modificarParametro",self.modifParametro],
		["modificarNorma",self.modifNorma],
		["modificarExponente",self.modifExponente],
		["modificarColor",self.modifListaColor],
		["modificarFuncion",self.modifFuncion],
		["volver"]
		]
		
		# variables de programa
		self.xmin = 0.0 # minimo valor del plano complejo, en el eje x
		self.xmax = 0.0 # maximo valor del plano complejo, en el eje x
		self.ymin = 0j  # minimo valor del plano complejo, en el eje y
		self.ymax = 0j  # maximo valor del plano complejo, en el eje y 
		self.planoComplejo = [] # matriz donde se guardan todos los puntos del plano complejo.
		self.sesionPasosMaximos = 256 # variable para definir el maximo nivel de iteraciones en la funcion sesion.
		self.formatos = [".jpg",".bmp",".png"] # Formatos disponibles para imagenes.
		self.elapsedTime = 0.0
		
		#variables de usuario	
		self.vars["funcion"] = Variable(self.listaFunciones.obtenerFuncion(args["funcion"]),self.modifFuncion,orden=0)
		self.vars["parametro"] = Variable(args["parametro"],self.modifGenerico,flags={"iterable":True},orden=1)
		self.vars["norma"] = Variable(args["norma"],self.modifGenerico,minimo=0.0,flags={"iterable":True},orden=2)
		self.vars["exponente"] = Variable(args["exponente"],self.modifGenerico,flags={"iterable":True},orden=3)
		self.vars["resolucion"] = Variable(args["resolucion"],self.modifResolucion,minimo=2,flags={"iterable":True},orden=4)
		self.vars["listaColores"] = Variable(args["listaColores"],self.modifListaColor,orden=5)		
		self.vars["zoom"] = Variable(args["zoom"],self.modifZoom,minimo=0,flags={"iterable":True},orden=6)
		self.vars["deltax"] = Variable(args["deltax"],self.modifEjeX,flags={"iterable":True},orden=7)
		self.vars["deltay"] = Variable(args["deltay"],self.modifEjeY,flags={"iterable":True},orden=8)
		self.vars["extension"] = Variable(args["extension"],self.modifValoresPosibles,valoresPosibles=self.formatos,orden=9)
		self.vars["asciiFile"] = Variable("asciiOut.txt",self.modifGenerico,orden=10)
		
		#Paleta de colores
		self.paleta = Paleta(self.vars["listaColores"].valor,self.vars["resolucion"].valor) #Paleta de colores para manejar el pintado de las funciones.
		
		#Items del Menu
		self.agregarMenu(0,Leaf("graficar","genera la salida en la pantalla",self.graficar))
		self.agregarMenu(1,Leaf("toAscii","",self.ascii))
		self.agregarMenu(2,Leaf("Foto","Foto Tomada",self.foto))
		self.agregarMenu(3,Leaf("Sesion","Secuencia de fotos iterando algunas variables",self.sesion))
		self.agregarMenu(4,Nodo("Scheduler","Ejecucion por lotes",Leaf("Ejecutar Scheduler","",self.ejecutarScheduler),Leaf("Cargar Scheduler","",self.cargarScheduler)))
		self.agregarMenu(5,Leaf("tiempos de ejecucion","Mediciones de tiempo de la ultima ejecucion",self.tiempos))
		
		#Funciones que se ejecutan luego de llamar a Modificar.
		self.agregarPostFunciones(self.calcularBounds,self.graficar,self.foto)
		
		self.actualizarTamanoPantalla()
		self.calcularBounds()	
		self.graficar()
		
	def calcularBounds(self):
		# Este es el mapeo de pixeles al plano complejo. 
		# por ej: X/[0,199] -> [-4,4]
		#         Y/[0,149] -> [-3i,3i]
		# tambien incluye los corrimientos y el zoom.
		# xmin = (-(ancho/mcd) * zoom) + deltax
		# xmax = ((ancho/mcd) * zoom) + deltax
		# ymin = ((alto/mcd) * zoom) + deltay
		# ymax = ((-alto/mcd) * zoom) + deltay
		
		mcd = gcd(self.ancho,self.alto)
		
		self.xmin   = (-(self.ancho/mcd))*self.vars["zoom"].valor + self.vars["deltax"].valor
		self.xmax   = (self.ancho/mcd)*self.vars["zoom"].valor + self.vars["deltax"].valor
		self.ymin   = (-(self.alto/mcd))*self.vars["zoom"].valor + self.vars["deltay"].valor
		self.ymax   = (self.alto/mcd)*self.vars["zoom"].valor + self.vars["deltay"].valor 

		deltax = abs(self.xmin - self.xmax) / (float(self.ancho) - 1)
		deltay = abs(self.ymin - self.ymax) / (float(self.alto) - 1)
		
		self.planoComplejo = []
		for x in range(0,self.ancho):	
			self.planoComplejo.append([])
			for y in range(0,self.alto):
				self.planoComplejo[x].append(self.convertirPC(x,y,deltax,deltay))

	def cargarScheduler(self):	
		opciones = [schedule[0] for schedule in self.scheduleables]
		self.enumerarLista(opciones)
		
		eleccion = validador.seleccionar(opciones)
		if(eleccion != "volver"):
			print "schedule!"
		
	def ejecutarScheduler(self):
		print "schedule!"		
		
	def tiempos(self,*tiempoTotal):
		if (len(tiempoTotal) == 0):
			tiempoTotal = [self.elapsedTime]
			
		print "-----------------------------------------------------------------"
		print "Tiempo Total: " + str(tiempoTotal[0])[:12]
		print "Funcion: " + str(self.vars["funcion"].valor)
		print "dimensiones: " + str(self.vars["ratio"].valor[0]*self.vars["factorRatio"].valor) + "x" + str(self.vars["ratio"].valor[1]*self.vars["factorRatio"].valor)
		print "resolucion: " + str(self.vars["resolucion"].valor)
		print "-----------------------------------------------------------------"
		self.log("-----------------------------------------------------------------")
		self.log("Tiempo Total: " + str(tiempoTotal[0])[:12])
		self.log("Funcion: " + str(self.vars["funcion"].valor))
		self.log("dimensiones: " + str(self.vars["ratio"].valor[0]*self.vars["factorRatio"].valor) + "x" + str(self.vars["ratio"].valor[1]*self.vars["factorRatio"].valor))
		self.log("resolucion: " + str(self.vars["resolucion"].valor))
		self.log("-----------------------------------------------------------------")

	def convertirPC(self,x,y,deltax,deltay): # convertir de pixel a complejo
	# def convertirPC(self,x,y):# convertir de pixel a complejo
		# equis = self.xmin + (x * (abs(self.xmin - self.xmax) / (float(self.ancho) - 1)))
		# ygrie = self.ymin + (y * (abs(self.ymin - self.ymax) / (float(self.alto) - 1)))
		equis = self.xmin + (x * deltax)
		ygrie = self.ymin + (y * deltay)
		
		return complex(equis,ygrie)
			
	def graficar(self):
		# primero que todo se obtienen los valores concretos para los parametros de la funcion a ejecutar
		# luego para cada pixel de la pantalla:
		# primero se convierte el pixel con coordenadas [x,y] a su valor en el plano complejo.
		# despues se ejecuta la funcion seteada para ese punto y los parametros seteados(obtenidos en el primer paso).
		# el color se obtiene desde la grilla de la paleta de colores.
		# por ultimo el pixel se acutaliza con el nuevo color.
		
		#recojo los parametros para pasarle a la funcion
		params = []
		for key in self.vars["funcion"].valor.parametros:
			params.append(self.vars[key].valor)
			
		#medicion de tiempo	
		startTime = time.time()	
		
		cuarto = self.ancho/4
		
		#Esto es para hacer el pasaje de pixel a complejo, esta aca para que no se hagan tantas cuentas en el loop.
		deltax = abs(self.xmin - self.xmax) / (float(self.ancho) - 1)
		deltay = abs(self.ymin - self.ymax) / (float(self.alto) - 1)
		
		# version 1
		#loop Principal del metodo, barre todo el plano calculando las intensidades
		# for x in range(0,self.ancho):	
			# for y in range(0,self.alto):
				# complejo = self.convertirPC(x,y,deltax,deltay)
				# # complejo = self.convertirPC(x,y)
				# valor = self.vars["funcion"].valor.calcular(complejo,params)
				# self.pixelArray[x,y] = self.paleta.grilla[valor-1]	#en grilla tengo el valor de color para la intensidad=valor-1
				
		# version 2
		# [[self.cargarPixelArray(x,y,self.paleta.grilla[self.vars["funcion"].valor.calcular(self.convertirPC(x,y,deltax,deltay),params) - 1]) for y in rangoy] for x in rangox]
		
		# version 3
		# rangox = range(0,self.ancho)
		# rangoy = range(0,self.alto)		
		# [[self.cargarPixelArray(x,y,self.paleta.grilla[self.vars["funcion"].valor.calcular(self.planoComplejo[x][y],params) - 1]) for y in rangoy] for x in rangox]
		
		# version 3 con fors por ahora esta es la mas rapida.
		for x in range(0,self.ancho):	
			for y in range(0,self.alto):
				valor = self.vars["funcion"].valor.calcular(self.planoComplejo[x][y],params)
				self.pixelArray[x,y] = self.paleta.grilla[valor-1]	#en grilla tengo el valor de color para la intensidad=valor-1	
		
		#medicion de tiempo		
		endTime = time.time()
		self.elapsedTime = endTime-startTime
		
		self.actualizarPantalla()
		#self.foto()
		self.tiempos(self.elapsedTime)

	def cargarPixelArray(self,x,y,color):
		self.pixelArray[x,y] = color
	
	def ascii(self):
		#setear resolucion a 16
		aux = self.vars["resolucion"].valor
		self.modifResolucion("resolucion",16)
		
		caracteres = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"]
		
		archivo =  open(self.vars["filesPath"].valor + "\\" + self.vars["outFile"].valor,"w")
		
		variables = str(self.vars)
		timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
		
		archivo.write(variables + "\n"+ timestamp + "\n")
		self.log(variables)
		
		params = []
		for key in self.vars["funcion"].valor.parametros:
			params.append(self.vars[key].valor)
		
		# for x in range(0,self.ancho):
			# for y in range(0,self.alto):
				# complejo = self.convertirPC(y,x)
				# valor = self.vars["funcion"].valor.calcular(complejo,params)
				# archivo.write(caracteres[valor-1])
			# archivo.write("\n")
	
		for x in range(0,self.ancho):	
			for y in range(0,self.alto):
				valor = self.vars["funcion"].valor.calcular(self.planoComplejo[y][x],params)
				archivo.write(caracteres[valor-1])
			archivo.write("\n")

		self.modifResolucion("resolucion",aux)
		
		archivo.close()

	def foto(self):
		panta = pantall = self.screen.copy()
		
		params = str(self.vars["funcion"].valor) + "-p" + str(self.vars["parametro"].valor) +"-e" + str(self.vars["exponente"].valor) +"-n" + str(self.vars["norma"].valor) +"-dx" + str(self.vars["deltax"].valor) +"-dy" + str(self.vars["deltay"].valor) +"-z" + str(self.vars["zoom"].valor) +"-r" + str(self.vars["resolucion"].valor)
				
		nombre = self.generarNombreValido(os.getcwd() +"\\"+ params + self.vars["extension"].valor)
		pygame.image.save(panta, nombre)
		self.log("foto Tomada",nombre,str(self.vars))

	def sesion(self):
		print "Sesion de fotos"
		
		volver = False
		seguir = True
		primera = True
		listado = [] # en listado me voy a guardar tuplas de 3, donde cada una tiene la key de la variable a iterar, valor incial y el salto que se da.
					 # listado = [[norma,2,1],[parametro,3j,1+1j]]
		pasos = 0
		
		# lista por comprension de variables iterables
		# Ordena la lista de variables por su flag de orden, y se queda con las que tengan flag iterable y sea true.
		disponibles = [variable[0] for variable in sorted(self.vars.items(),key=lambda x: x[1].orden) if "iterable" in variable[1].flags.keys() and variable[1].flags["iterable"]]

		while (seguir):
			print "variable a iterar?"
			self.enumerarLista(disponibles + ["Volver"])
			variable = validador.seleccionar(disponibles + ["Volver"])
			
			if(variable == "Volver"):
				seguir = False
				volver = True
			else:
			
				print "valor actual:"
				print str(self.vars[variable].valor) + "\n"
				
				print "desde:"
				# desde = validador.ingresar(type(self.vars[variable].valor),validador.entre,self.vars[variable].minimo,self.vars[variable].maximo)
				desde = validador.ingresarVariable(self.vars[variable])
				
				print "hasta:"
				# hasta = validador.ingresar(type(self.vars[variable].valor),validador.entre,self.vars[variable].minimo,self.vars[variable].maximo)
				hasta = validador.ingresarVariable(self.vars[variable])
					
				if(primera):
					print "en cuantos pasos:"
					pasos = validador.ingresar(int,validador.entre,2,self.sesionPasosMaximos)
					primera = False
					
				salto = (hasta - desde) / (pasos - 1)
				listado.append([variable, desde, salto])
				disponibles.remove(variable)
				
				if (len(disponibles) == 0):
					seguir = False
				else:
					print "otra variable?"
					seguir = validador.ingresarSINO()

		if(not volver):
			# Genero el nombre de la Carpeta
			nombreCarpeta = self.vars["filesPath"].valor + "\\Sesion-" + str(self.vars["funcion"].valor)
			for item in listado:
				# item[1] + item[2] * (pasos-1) = HASTA!
				nombreCarpeta += "_" + str(item[0]) + str(item[1]) + "-" + str(item[1] + item[2] * (pasos-1))
			
			nombreCarpeta = self.generarNombreValido(nombreCarpeta)
			
			if not os.path.isdir(nombreCarpeta):
				os.mkdir(nombreCarpeta)
			os.chdir(nombreCarpeta)	
					
			#medicion de tiempo	
			startTime = time.time()
		
			#Loop de la sesion
			for i in range(0,pasos):
				for key in listado:
					var = key[0]
					desdeaux = key[1]
					saltoaux = key[2]
					self.vars[var].modificador(var,desdeaux + (saltoaux * i))
					# self.vars[var].valor = desdeaux + (saltoaux * i)
	
					self.graficar()
					self.foto()
					
				print str(i+1) + "/" + str(pasos)
			
			#medicion de tiempo	
			endTime = time.time()
			
			self.log("-----------------------------------------------------------------")
			self.log("--- Sesion ------------------------------------------------------")
			print "-----------------------------------------------------------------"
			print "--- Sesion ------------------------------------------------------"
			self.tiempos(endTime - startTime)
			
			os.chdir(self.vars["filesPath"].valor)		
	
	def modifNorma(self,key,*params):
		if(len(params) == 0):
			self.vars["norma"] = validador.ingresarVariable(self.vars["norma"])
	
	def modifExponente(self,key,*params):
		if(len(params) == 0):
			self.vars["exponente"] = validador.ingresarVariable(self.vars["exponente"])
	
	def	modifParametro(self,key,*params):
		if(len(params) == 0):
			self.vars["parametro"] = validador.ingresarVariable(self.vars["parametro"])
			
	def modifZoom(self,key,*params):
		if(len(params) == 0):			
			self.vars["zoom"].valor = validador.ingresarVariable(self.vars["zoom"])
		else:
			self.vars["zoom"].valor = float(params[0])
		self.calcularBounds()
	
	def modifEjeX(self,key,*params):
		if(len(params) == 0):
			print "valores positivos dezplazan la imagen hacia izquierda y valores negativos hacia la derecha"
			print "corrimiento en x"
			self.vars["deltax"].valor = validador.ingresarVariable(self.vars["deltax"])# obtengo el delta en x
			
		else:
			self.vars["deltax"].valor = float(params[0])
		self.calcularBounds()
		
	def modifEjeY(self,key,*params):
		if(len(params) == 0):
			print "valores positivos dezplazan la imagen hacia arriba y valores negativos hacia la abajo"			
			print "corrimiento en y"
			self.vars["deltay"].valor = validador.ingresarVariable(self.vars["deltay"])# obtengo el delta en y
			
		else:
			self.vars["deltay"].valor = float(params[0])
		self.calcularBounds()

	def modifColor(self,key,*params):
		if(len(params) == 0):
			self.vars[key].valor = self.pickColor()
		else:
			self.vars[key].valor = params[0]
	
	def pickColor(self):
		print "rojo:"
		r= validador.ingresar(int,validador.entre,0,255)
		
		print "verde:"
		g = validador.ingresar(int,validador.entre,0,255)
		
		print "azul:"
		b = validador.ingresar(int,validador.entre,0,255)
		
		return [r,g,b]
	
	def modifListaColor(self,key,*params):
		#Lista Colores
		if(len(params) == 0):
			self.vars["listaColores"].valor = []
			print "-- Lista de colores--"
			print "Como armar la lista de colores:"

			print "En este modo se van a setear una cantidad de colores en puntos de la paleta, todos los puntos intermedios son interpolados linealmente."
			print "Para ello se eligen de a dos colores RGB y hasta donde abarca ese tramo."
			print "si la paleta no es llenada hasta el final, el ultimo color ingresado sera el que complete la misma, de igual modo si por error se ingresa un valor hasta mas grande que el que permite la paleta, este se trunca."
			
			print "resolucion:", self.vars["resolucion"].valor
			
			seguir = True
			previo = 0
			while(seguir):
				print "Color Desde:"
				colord = self.pickColor()
				
				print "Color Hasta:"
				colorh = self.pickColor()
				
				print "Hasta:"
				hasta = validador.ingresar(int,validador.entre,previo,self.vars["resolucion"].valor)
				
				print "otro tramo?"
				resp = validador.ingresarSINO()		

				if (resp): # SI quiero otro color
					if(hasta == self.vars["resolucion"].valor):
						seguir = False
						
				else: # NO quiero otro color
					if(hasta < self.vars["resolucion"].valor):
						hasta = self.vars["resolucion"].valor
					seguir = False			

				color = [colord,colorh,hasta]
				self.vars["listaColores"].valor.append(color)		
			
			# print self.vars["listaColores"].valor
			# self.paleta.setear(self.vars["listaColores"].valor)
			
		else:
			self.vars["listaColores"].valor = params[0]
			
		print self.vars["listaColores"].valor
		self.paleta.setear(self.vars["listaColores"].valor)
	
	def modifResolucion(self,key,*params):
		if(len(params) == 0):
			self.vars["resolucion"].valor = validador.ingresarVariable(self.vars["resolucion"])
		else:
			self.vars["resolucion"].valor = int(params[0])
			
		self.vars["listaColores"].valor = self.paleta.ajustarResolucion(self.vars["listaColores"].valor, self.vars["resolucion"].valor)
		
	def modifTamano(self,key,*params): 
		#ajustar el tamano pantalla, hay que ingresar la relacion de aspecto.
		# por ejemplo, 4:3 factorRatio = 2 nos da una pantalla de 8 x 6 pixeles
		if(len(params) == 0):
			print "---relacion de aspecto de la pantalla---"
			print "se debe ingresar cuantos pixeles de ancho por cuantos de alto por ej 4:3, 16:9"
			print "Luego el factor multiplica ambos terminos (al 4 y al 3 por ej) para dar la resolucion final de la pantalla"
			print "ancho:"
			ancho = validador.ingresar(int,validador.mayor,0)
			print "alto:"
			alto = validador.ingresar(int,validador.mayor,0)
		else:
			ancho = int(params[0])
			alto = int(params[1])
			
		mcd = gcd(ancho,alto)
		self.vars["ratio"].valor[0] = ancho/mcd
		self.vars["ratio"].valor[1] = alto/mcd
	
		if(len(params) == 0):
			print "factor:"
			self.vars["factorRatio"].valor = validador.ingresarVariable(self.vars["factorRatio"])
		else:
			self.vars["factorRatio"].valor = int(params[2])
	
	def modifFuncion(self,key,*params):
		if(len(params) == 0):
			self.enumerarLista(self.listaFunciones.nombres+["volver"])
			funcion = validador.seleccionar(self.listaFunciones.nombres + ["volver"])
			if(funcion !="volver"):
				self.vars["funcion"].valor = self.listaFunciones.obtenerFuncion(funcion)
		else:
			self.vars["funcion"].valor = self.listaFunciones.obtenerFuncion(params[0])	
	
	def ayuda(self):
		print "-----------------------------------------------------------------"
		print "PROXIMAMENTE MANUAL DE INSTRUCCIONES E INTRODCCION A GEOMETRIA"
		print "FRACTAL."	
		print "-----------------------------------------------------------------"	
		
	def salirPrint(self):
		print "--- \\m/ ---"

		
if __name__ == '__main__':
	a = Fractales("Fractaloides","2.0.0",True,
					ratio=[1,1],
					factorRatio=100,
					zoom=1.0,
					deltax=0.0,
					deltay=0.0,
					resolucion=15,
					norma=2.0,
					exponente=2.0+0j,
					parametro=0j,
					funcion="mandelbrot",
					colorFondo=[0,0,0],
					listaColores=[[[0,0,0],[0,0,255],15]],
					extension=".png")
					
	a.menuPrincipal()		
