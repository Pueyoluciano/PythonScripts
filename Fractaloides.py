import os
import pygame
import Aplicacion
import flagsFactory
import threading as thr
from fractions import gcd
from datetime import datetime
from paletaColores import Paleta	
from Menu import *
from Variable import *
from validador import *
from Funcionesfractales import *


class Fractales(Aplicacion.Aplicacion):
	def iniciar(self,**args):	
		# pygame.init()
		self.listaFunciones= Funcion.listado # Diccionario con el listado de funciones.
		
		# variables de programa
		#self.ancho = 0  # ancho = ratio[0]*factorRatio
		#self.alto = 0   # alto = ratio[1]*factorRatio
		self.xmin = 0.0 # minimo valor del plano complejo, en el eje x
		self.xmax = 0.0 # maximo valor del plano complejo, en el eje x
		self.ymin = 0j  # minimo valor del plano complejo, en el eje y
		self.ymax = 0j  # maximo valor del plano complejo, en el eje y 
		self.sesionPasosMaximos = 256 # variable para definir el maximo nivel de iteraciones en la funcion sesion.
		self.formatos = [".jpg",".bmp",".png"] # Formatos disponibles para imagenes.
		self.pixeles = [] # pixelArray
		
		#variables de usuario	
		#self.vars["ratio"]  = Variable(args["ratio"],self.modifTamano,minimo=[1,1],flags={"iterable":False})
		#self.vars["factorRatio"] = Variable(args["factorRatio"],self.modifTamano,minimo=2,flags={"iterable":False})
		self.vars["ratio"].valor = args["ratio"]
		self.vars["factorRatio"].valor = args["factorRatio"]
		
		self.vars["asciiFile"] = Variable("asciiOut.txt",self.modifGenerico)
		self.vars["zoom"] = Variable(args["zoom"],self.modifZoom,minimo=0,flags={"iterable":True})
		self.vars["deltax"] = Variable(args["deltax"],self.modifEje,flags={"iterable":True})
		self.vars["deltay"] = Variable(args["deltay"],self.modifEje,flags={"iterable":True})
		self.vars["resolucion"] = Variable(args["resolucion"],self.modifResolucion,minimo=1,flags={"iterable":True})
		self.vars["norma"] = Variable(args["norma"],self.modifGenerico,minimo=0.0,flags={"iterable":True})
		self.vars["exponente"] = Variable(args["exponente"],self.modifGenerico,flags={"iterable":True})
		self.vars["parametro"] = Variable(args["parametro"],self.modifGenerico,flags={"iterable":True})
		self.vars["funcion"] = Variable(self.listaFunciones[args["funcion"]],self.modifFuncion)
		self.vars["colorFondo"] = Variable(args["colorFondo"],self.modifColor,minimo=[0,0,0],maximo=[255,255,255])
		self.vars["listaColores"] = Variable(args["listaColores"],self.modifListaColor)		
		self.vars["extension"] = Variable(args["extension"],self.modifValoresPosibles,valoresPosibles=self.formatos)
		
		self.paleta = Paleta(self.vars["listaColores"].valor,self.vars["resolucion"].valor) #Paleta de colores para manejar el pintado de las funciones.
		
		self.agregarMenu(0,Leaf("graficar","genera la salida en la pantalla",self.graficar))
		self.agregarMenu(1,Leaf("toAscii","",self.ascii))
		self.agregarMenu(2,Leaf("Foto","Tomar una foto",self.foto))
		self.agregarMenu(3,Leaf("Sesion","Secuencia de fotos iterando algunas variables",self.sesion))

		#Funciones que se ejecutan luego de llamar a Modificar.
		self.agregarPostFunciones(self.recalcular,self.graficar)
		
		self.recalcular()
				
		# self.screen = screen = pygame.display.set_mode((self.ancho,self.alto))
		# self.screen = pygame.display.set_mode((50,50))
		# pygame.display.set_caption("titulo")
		# self.pixelArray = pygame.PixelArray(self.screen)
		
		# self.pixelArray = pygame.Surface(self.ancho,self.alto)
		
		# self.clock = pygame.time.Clock()
		# self.tick = self.clock.tick(20)
		
		self.graficar()

	def recalcular(self):
		# self.calcularAnchoAlto()
		self.calcularBounds()
		self.temporal()
		
	# def calcularAnchoAlto(self):
		# self.ancho = self.vars["ratio"].valor[0] * self.vars["factorRatio"].valor 
		# self.alto  = self.vars["ratio"].valor[1] * self.vars["factorRatio"].valor
	
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

	def temporal(self): # carga el pixelArray, con pygame andando esto se va
		self.pixeles = []
		for x in range(0,self.ancho):
			self.pixeles.append([])
			for y in range(0,self.alto):
				self.pixeles[x].append(self.vars["colorFondo"].valor)
	
	def convertirPC(self,x,y): # convertir de pixel a complejo
		equis = self.xmin + (x * (abs(self.xmin - self.xmax) / (float(self.ancho) - 1)))
		ygrie = self.ymin + (y * (abs(self.ymin - self.ymax) / (float(self.alto) - 1)))
		
		return complex(equis,ygrie)
			
	def graficar(self):
		# primero que todo se obtienen los valores concretos para los parametros de la funcion a ejecutar
		# luego para cada pixel de la pantalla:
		# primero se convierte el pixel con coordenadas [x,y] a su valor en el plano complejo.
		# despues se ejecuta la funcion seteada para ese punto y los parametros seteados(obtenidos en el primer paso).
		# el color se obtiene desde la grilla de la paleta de colores.
		# por ultimo el pixel se acutaliza con el nuevo color.
		
		params = []
		for key in self.vars["funcion"].valor.parametros:
			params.append(self.vars[key].valor)
			
		for x in range(0,self.ancho):
			for y in range(0,self.alto):
				complejo = self.convertirPC(x,y)
				valor = self.vars["funcion"].valor.calcular(complejo,params)
				# print x,y, complejo, valor
				color = self.paleta.grilla[valor-1]
				self.cargarPixel([x,y],color)
				self.pixelArray[x,y] = color

		self.actualizarPantalla()
		
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
		
		for x in range(0,self.ancho):
			for y in range(0,self.alto):
				complejo = self.convertirPC(y,x)
				valor = self.vars["funcion"].valor.calcular(complejo,params)
				# print valor,
				# print caracteres[valor-1],
				archivo.write(caracteres[valor-1])
			archivo.write("\n")
	
		self.modifResolucion("resolucion",aux)
		
		archivo.close()
		
	def cargarPixel(self,pixel,color):
		#funcion que va a cambiar segun que se use para graficar, pygame,tkinter, etc.
		self.pixeles[pixel[0]][pixel[1]] = color
		
	def foto(self):
		panta = pantall = self.screen.copy()
		
		params = str(self.vars["funcion"].valor) + "-p" + str(self.vars["parametro"].valor) +"-e" + str(self.vars["exponente"].valor) +"-n" + str(self.vars["norma"].valor) +"-dx" + str(self.vars["deltax"].valor) +"-dy" + str(self.vars["deltay"].valor) +"-z" + str(self.vars["zoom"].valor) +"-r" + str(self.vars["resolucion"].valor)
				
		nombre = os.getcwd() +"\\"+ params + self.vars["extension"].valor
		pygame.image.save(panta, nombre)
		self.log("foto Tomada",nombre,str(self.vars))
		print "**Cachssggg**"

	def sesion(self):
		print "Sesion de fotos"
		
		seguir = True
		primera = True
		listado = [] # en listado me voy a guardar tuplas de 3, donde cada una tiene la key de la variable a iterar, valor incial y el salto que se da.
					 # listado = [[norma,2,1],[parametro,3j,1+1j]]
		pasos = 0
		
		disponibles = [item for item in self.vars if "iterable" in self.vars[item].flags.keys() and self.vars[item].flags["iterable"]] # lista por comprension de variables iterables
		
		while (seguir):
			print "variable a iterar?"
			self.enumerarLista(disponibles)
			
			variable = validador.seleccionar(disponibles)
			
			print "valor actual:"
			print str(self.vars[variable].valor) + "\n"
			
			print "desde:"
			desde = validador.ingresar(type(self.vars[variable].valor),validador.entre,self.vars[variable].minimo,self.vars[variable].maximo)
			
			print "hasta:"
			hasta = validador.ingresar(type(self.vars[variable].valor),validador.entre,self.vars[variable].minimo,self.vars[variable].maximo)
				
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

		nombreCarpeta = self.vars["filesPath"].valor + "\\Sesion"
		for item in listado:
			# item[1] + item[2] * (pasos-1) = HASTA!
			nombreCarpeta += "_" + str(item[0]) + str(item[1]) + "-" + str(item[1] + item[2] * (pasos-1))
	
		
		if not os.path.isdir(nombreCarpeta):
			os.mkdir(nombreCarpeta)
		os.chdir(nombreCarpeta)	
	
		for i in range(0,pasos):
			for key in listado:
				var = key[0]
				desdeaux = key[1]
				saltoaux = key[2]
				self.vars[var].valor = desdeaux + (saltoaux * i)
			
				self.graficar()
				self.foto()
		
		os.chdir(self.vars["filesPath"].valor)
			
	def modifZoom(self,key,*params):
		if(len(params) == 0):			
			self.vars["zoom"].valor = validador.ingresar(float,validador.mayor,self.vars["zoom"].minimo)
		else:
			self.vars["zoom"].valor = params[0]
		self.calcularBounds()
	
	def modifEje(self,key,*params):
		if(len(params) == 0):
			self.vars["deltax"].valor = validador.ingresar(int,validador.entre,self.vars["deltax"].minimo,self.vars["deltax"].maximo)# obtengo el delta en x
			self.vars["deltay"].valor = validador.ingresar(int,validador.entre,self.vars["deltay"].minimo,self.vars["deltay"].maximo)# obtengo el delta en y
		else:
			self.vars["deltax"].valor = params[0]
			self.vars["deltay"].valor = params[1]
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
	
	def modifListaColor(self,key):
		#Lista Colores
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
		
		print self.vars["listaColores"].valor
		self.paleta.setear(self.vars["listaColores"].valor)
	
	def modifResolucion(self,key,*params):
		if(len(params) == 0):
			self.vars["resolucion"].valor = validador.ingresar(int,validador.mayor,self.vars["resolucion"].minimo)
		else:
			self.vars["resolucion"].valor = params[0]
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
			ancho = params[0]
			alto = params[1]
			
		mcd = gcd(ancho,alto)
		self.vars["ratio"].valor[0] = ancho/mcd
		self.vars["ratio"].valor[1] = alto/mcd
	
		if(len(params) == 0):
			print "factor:"
			self.vars["factorRatio"].valor = validador.ingresar(int,validador.mayorigual,self.vars["factorRatio"].minimo)
		else:
			self.vars["factorRatio"].valor = params[2]
	
	def modifFuncion(self,key,*params):
		if(len(params) == 0):
			for (i,clave) in enumerate(self.listaFunciones.keys()):
				print str(i+1) + ") " + clave

			clave = validador.seleccionar(self.listaFunciones.keys())
		else:
			clave = params[0]
			
		self.vars["funcion"].valor = self.listaFunciones[clave]	

	
if __name__ == '__main__':
	a = Fractales("Fractaloides","2.0.0",True,
					ratio=[1,1],
					factorRatio=50,
					zoom=1.0,
					deltax=0.0,
					deltay=0.0,
					resolucion=15,
					norma=2.0,
					exponente=2.0+0j,
					parametro=0j,
					funcion="mandelbrot",
					colorFondo=[0,0,0],
					listaColores=[[[0,0,0],[0,0,0],3],[[0,0,0],[255,255,255],11],[[255,255,255],[0,0,255],15]],
					extension=".jpg")
					
	a.menuPrincipal()		
