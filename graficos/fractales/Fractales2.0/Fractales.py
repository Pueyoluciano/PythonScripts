# para cada pixel de la pantalla:	
	# se va a iterar la funcion fractal seteada, la cual devuelve un valor entre 0 y la maxima resolucion (iteraciones).
		# para cada valor de salida de la funcion fractal, hay un color asignado en la paleta de colores.
	# se pinta el pixel actual con el color obtenido de la paleta en funcion de la salida de la funcion fractal.

# la funcion fractal es una funcion recursiva que cuenta cada iteracion que realiza. para empezar se setea un elemento incial, que es el pixel sobre el que se va a evaluar (el pixel representa un punto en el plano complejo).
 # el paso iterativo esta dado por una ecuacion de la pinta Z(n+1) = (Z(n))**2 + C . 
 # donde Zn es el termino enesimo, y C es el punto inicial(el pixel en nuestro caso).
 # existe una propiedad sobre esta funcion (el conjunto de Mandelbrot), y es que si el modulo de Zn (un termino de la sucesion)es mayor o igual a 2, entonces el punto sobre el cual estamos iterando (de nuevo, un pixel de la pantalla) esta excluido del conjunto de mandelbrot, y en ese caso no necesitamos seguir iterando la funcion. Si despues de una cierta cantidad de pasos(definido por la resolucion, o iteraciones, como mas guste llamarlo) el |Zn| no cumple con lo antedicho, entonces se considera a ese pixel dentro del conjunto. en cualquier caso siempre contamos la cantidad de iteraciones que nos llevo comprobarlo. de ese modo tenemos una referencia para el color.
 
# la paleta de colores es una biyeccion entre una lista con igual cantidad de elementos que el valor de la resolucion y una progresion de colores. 
	# la paleta tiene cuatro modos de ser poblada, un color solido, n-colores solidos, monocromatico, n-colores monocromatico. para los casos monocromatico y n-colores cromatico las interpolaciones son lineales.

# habra una clase pantalla, que va a gestionar su grilla de pixeles, done para cada uno va a correr una funcion elegida(que no tiene porque ser una funcion fractal).

# por medio de una interfaz(en princpio por consola de comandos) se van a poder ingresar tdos los datos necesarios para la configuracion de las distintas variables, y tendra un menu navegable con todas las acciones posibles, ademas del seteo de variables, tales como graficar, cambiar de funcion, setear una paleta de colores, etc.

import os
from paletaColores import Paleta	
from Funcionesfractales import *
from validador import *
from fractions import gcd
from datetime import datetime
from Menu import *
from Variable import *
		
class Pantalla:
	def __init__(self,ratio=[1,1],
					factorRatio=50,
					zoom=1.0,
					deltax=0.0,
					deltay=0.0,
					resolucion=15,
					norma=2.0,
					exponente=2.0+0j,
					parametro=0j,
					funcion="mandelbrot",
					directorio=os.getcwd(),
					colorFondo=[0,0,0],
					listaColores=[[[0,0,0],[255,0,255],15]],
					asciiFile=os.getcwd() + "\AsciiOut.txt",
					grafcDir=os.getcwd() + "\GraficOuts"):
					
		self.vars = {} 			             # vars es un diccionario de variables.
		self.listaFunciones= Funcion.listado # listado de funciones.
		
		# variables de programa
		self.ancho = 0  # ancho = ratio[0]*factorRatio
		self.alto = 0   # alto = ratio[1]*factorRatio
		self.xmin = 0.0 # minimo valor del plano complejo, en el eje x
		self.xmax = 0.0 # maximo valor del plano complejo, en el eje x
		self.ymin = 0j  # minimo valor del plano complejo, en el eje y
		self.ymax = 0j  # maximo valor del plano complejo, en el eje y 
		self.sesionPasosMaximos = 256 # variable para definir el maximo nivel de iteraciones en la funcion sesion.
		self.pixeles = [] # pixelArray
		self.logFile = "\FractalesLog.txt"
		
		#variables de usuario
		self.vars["ratio"]  = Variable(ratio,{"iterable":False},self.modifTamano,[1,1])
		self.vars["factorRatio"] = Variable(factorRatio,{"iterable":False},self.modifTamano,2)
		self.vars["zoom"] = Variable(zoom,{"iterable":True},self.modifZoom,0)
		self.vars["deltax"] = Variable(deltax,{"iterable":True},self.modifEje)
		self.vars["deltay"] = Variable(deltay,{"iterable":True},self.modifEje)
		self.vars["resolucion"] = Variable(resolucion,{"iterable":True},self.modifResolucion,1)
		self.vars["norma"] = Variable(norma,{"iterable":True},self.modifGenerico,0.0)
		self.vars["exponente"] = Variable(exponente,{"iterable":True},self.modifGenerico)
		self.vars["parametro"] = Variable(parametro,{"iterable":True},self.modifGenerico)
		self.vars["funcion"] = Variable(self.listaFunciones[funcion],{"iterable":False},self.modifFuncion)
		self.vars["directorio"] = Variable(directorio,{"iterable":False},self.modifGenerico)
		self.vars["colorFondo"] = Variable(colorFondo,{"iterable":False},self.modifColor,[0,0,0],[255,255,255])
		self.vars["listaColores"] = Variable(listaColores,{"iterable":False},self.modifListaColor) #[[self.vars["colorFondo"].valor,[255,0,255],self.vars["resolucion"].valor]]
		self.vars["asciiFile"] = Variable(asciiFile,{"iterable":False},self.modifGenerico)
		self.vars["grafcDir"] = Variable(grafcDir,{"iterable":False},self.modifGenerico)
		
		self.paleta = Paleta(self.vars["listaColores"].valor,self.vars["resolucion"].valor) #Paleta de colores para manejar el pintado de las funciones.
		
		self.menu = Nodo("-- Fractales -- V2.0 --","-----------------------",
					     Leaf("graficar","genera la salida en la pantalla",self.graficar),
						 Leaf("toAscii","",self.ascii),
						 Leaf("Modificar parametros","Parametros modificables por el usuario",self.modificar),
						 Leaf("Ver parametros","", self.variables),
						 Leaf("Foto","Tomar una foto",self.foto),
						 Leaf("Sesion","Secuencia de fotos iterando algunas variables",self.sesion),
						 Leaf("Que es esto?","",self.ayuda),
						 Leaf("Salir",":D",self.salir)
						 )
		
		self.recalcular()
		self.graficar()
		
	def variables(self):
		keys = self.vars.keys()
		keys.sort()
		for key in keys:
			print "-" + key + ":",self.vars[key].valor

	def recalcular(self):
		self.calcularAnchoAlto()
		self.calcularBounds()
		self.temporal()
		
	def calcularAnchoAlto(self):
		self.ancho = self.vars["ratio"].valor[0] * self.vars["factorRatio"].valor 
		self.alto  = self.vars["ratio"].valor[1] * self.vars["factorRatio"].valor
	
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
				#self.pixeles[x,y] = color
	
	def __log(self,*datos):
		archivo  = open(os.getcwd()+self.logFile,"a")
		
		timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " -- "
		archivo.write(timestamp)
		
		for i in range(0,len(datos)):
		
			
			if (i == len(datos)-1):
				archivo.write(datos[i])
			else:
				archivo.write(datos[i] + ", ")
		archivo.write("\n")	
		archivo.close()
	
	def ascii(self):
		#setear resolucion a 16
		aux = self.vars["resolucion"].valor
		self.modifResolucion("resolucion",16)
		
		caracteres = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"]
		
		archivo = open(self.vars["asciiFile"].valor,"w")
		
		variables = str(self.vars)
		timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
		
		archivo.write(variables + "\n"+ timestamp + "\n")
		self.__log(variables)
		
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
		print "**Cachssggg**"

	def sesion(self):
		print "Sesion de fotos"
		
		seguir = True
		primera = True
		listado = [] # en listado me voy a guardar tuplas de 3, donde cada una tiene la key de la variable a iterar, valor incial y el salto que se da.
					 # listado = [[norma,2,1],[parametro,3j,1+1j]]
		pasos = 0
		disponibles = [item for item in self.vars if self.vars[item].flags["iterable"]] # lista por comprension de variables iterables
		
		while (seguir):
			print "variable a iterar?"
			print disponibles
			variable = validador.ingresar(str,validador.igual,disponibles)
			
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
	
		for i in range(0,pasos):
			for key in listado:
				var = key[0]
				desdeaux = key[1]
				saltoaux = key[2]
				self.vars[var].valor = desdeaux + (saltoaux * pasos)
			
			self.graficar()
			self.foto()
			      
	def modificar(self):
	# Si uso el metodo modificar; para que el usuario ingrese valores, params estara vacio.
	# Si por el contrario llamo directamente a la funcion modificadora (por ej modifZoom) hay que pasarle el valor nuevo. el dato key en ese caso no cumple funcion.
		print "variable a modificar:"
		for (i,clave) in enumerate(self.vars.keys()):
			print str(i+1) + ") " + clave, ":",self.vars[clave].valor 

		# key = validador.ingresar(str,validador.igual,self.vars.keys())
		key = validador.seleccionar(self.vars.keys())
		
		print key
		print "valor actual: ", self.vars[key].valor
		self.vars[key].modificador(key)
		self.recalcular()
		self.graficar()
		
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
			print "Resolucion: ",self.vars["resolucion"].valor
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
			print self.listaFunciones.keys()
			clave = validador.ingresar(str,validador.igual,self.listaFunciones.keys())
		else:
			clave = params[0]
			
		self.vars["funcion"].valor = self.listaFunciones[clave]	
		
	def modifGenerico(self,key):
		tipo = type(self.vars[key].valor)
		self.vars[key].valor = validador.ingresar(tipo,validador.entre,self.vars[key].minimo,self.vars[key].maximo)
	
	def menuPrincipal(self):
		salir = False
		while (not salir):
			salir = self.menu.evaluar()
	
	def ayuda(self):
		print "Manual de usuario."
		print "--------------------------"
		print "-- en construcion vio ----"
		print "--------------------------"
	
	def salir(self):
		return True

		
if __name__ == '__main__':	
	p = Pantalla()
	p.menuPrincipal();

		
			
			
			
			
			
		