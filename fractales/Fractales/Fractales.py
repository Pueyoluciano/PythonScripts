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

from paletaColores import Paleta	
from Funcionesfractales import *
from validador import *
from fractions import gcd


class Variable:
	def __init__(self,valor,iterable,modificador,minimo = None,maximo = None):
		self.valor = valor
		if(type(valor) == int or type(valor) == float):
			if(minimo == None):
				minimo = -float("inf")

			if(maximo == None):
				maximo = float("inf")

		self.minimo = minimo
		self.maximo = maximo
		self.modificador = modificador
		self.iterable = iterable

		
class Pantalla:
	def __init__(self):
		self.vars = {} 			             # vars es un diccionario de variables.
		self.listaFunciones= Funcion.listado # listado de funciones.
		
		# variables de programa
		self.ancho = 0
		self.alto = 0
		self.xmin = 0.0
		self.xmax = 0.0
		self.ymin = 0j
		self.ymax = 0j
		self.sesionPasosMaximos = 256
		self.pixeles = []
		
		#variables de usuario
		self.vars["ratio"]  = Variable([1,1],False,self.modifTamano,[1,1])
		self.vars["factorRatio"] = Variable(2,False,self.modifTamano,2)
		self.vars["zoom"] = Variable(1.0,True,self.modifZoom,0)
		self.vars["deltax"] = Variable(0.0,True,self.modifEje)
		self.vars["deltay"] = Variable(0.0,True,self.modifEje)
		self.vars["resolucion"] = Variable(15,True,self.modifResolucion,1)
		self.vars["norma"] = Variable(2.0,True,self.modifGenerico,0.0)
		self.vars["exponente"] = Variable(2.0,True,self.modifGenerico)
		self.vars["parametro"] = Variable(0j,True,self.modifGenerico)
		self.vars["funcion"] = Variable(self.listaFunciones["mandelbrot"],False,self.modifFuncion)
		self.vars["directorio"] = Variable("C:/fotosFractales",False,self.modifGenerico)
		self.vars["colorFondo"] = Variable([0,0,0],False,self.modifColor,[0,0,0],[255,255,255])
		self.vars["listaColores"] = Variable([[self.vars["colorFondo"].valor,[255,0,255],self.vars["resolucion"].valor]],False,self.modifListaColor)
		
		# self.vars["ancho"] = 0
		# self.vars["alto"]= 0
		# self.vars["ratio"]  = [4,3]
		# self.vars["factorRatio"] = 2
		# self.vars["xmin"] = 0
		# self.vars["xmax"] = 0
		# self.vars["ymin"] = 0
		# self.vars["ymax"] = 0
		# self.vars["zoom"] = 1.0
		# self.vars["deltax"] = 0.0
		# self.vars["deltay"] = 0.0
		# self.vars["resolucion"] = 15
		# self.vars["norma"] = 2
		# self.vars["exponente"] = 2.0
		# self.vars["parametro"] = 0j
		# self.vars["funcion"] = self.listaFunciones["mandelbrot"]
		# self.vars["directorio"] = "C:/fotosFractales"
		# self.vars["pixeles"] = [] # pixelArray
		# self.vars["colorFondo"] = [0,0,0]
		# self.vars["listaColores"] = [[self.vars["colorFondo"],[255,0,255],self.vars["resolucion"]]]
				
		self.paleta = Paleta(self.vars["listaColores"].valor,self.vars["resolucion"].valor)
		
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
	
	def ascii(self):
		#setear resolucion a 16
		aux = self.vars["resolucion"].valor
		self.modifResolucion("resolucion",16)
		caracteres = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
		caracteres = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"]
		
		archivo = open("FractalesOut.txt","w")
		
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
		# disponibles = self.iterables[:]
		disponibles = [item for item in self.vars if self.vars[item].iterable]
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
		for clave in self.vars.keys():
			print clave, ":",self.vars[clave].valor 

		key = validador.ingresar(str,validador.igual,self.vars.keys())
		
		print "valor actual: ", self.vars[key].valor
		self.vars[key].modificador(key)
		self.recalcular()
		self.graficar()
		
	def modifZoom(self,key,*params):
		if(len(params) == 0):
			print self.vars["zoom"].minimo
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
		self.vars[key].valor = validador.ingresar(tipo)
		

class Menu:
	pass
	# menu Principal:
	# 1) Modificar Parametros
	# 2) ver parametros
	# 3) tomar foto
	# 4) sesion
	# 5) salir
	#
			
			
			
			
			
		