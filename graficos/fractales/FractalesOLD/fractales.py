#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import pygame
import math
import os
import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica
import time
import random
from iniciarpy import *
from funcionesfractales import *

#-------------------------------------------------
# ------------------  Escala  --------------------
#-------------------------------------------------
# Define la escala para ancho y alto.
# Primero calcula la distancia entre xmin y xmax
# Luego reparte esta distancia en ancho/alto veces.
def escala(ancho,alto,xmin,ymin,xmax,ymax):
	xescala = (xmax - xmin) / ancho
	yescala = (ymax - ymin) / alto
	return xescala,yescala

#-------------------------------------------------
# -----------------  Escala2  --------------------
#-------------------------------------------------
# Hace lo mismo que Escala(), pero hay que ingresarle 3 listas
# con igual cantidad de elementos.
def escala2(dimensiones,minimos,maximos):
	tipo = type(list([]))
	nescala = []
	if ((type(dimensiones) == tipo) and (type(minimos) == tipo) and  (type(maximos) == tipo)):
		if (len(dimensiones) == len(minimos) and len(minimos) == len(maximos)):
			for i in range(0,len(dimensiones)):
				a = float(maximos[i] - minimos[i]) / dimensiones[i]
				nescala.append(a)
	return nescala
	
#-------------------------------------------------
# ------------  Clase Diccionario  ---------------
#-------------------------------------------------
class Diccionario():
	def __init__(self):
		self.contenido = {}
		
	def agregar(self,key,instancia):
		self.contenido[key] = instancia

	def quitar(self,key):
		del self.contenido[key]

	def subconjunto(self,lista):
		diccio = {}
		for i in range(0,len(lista)):
			try:
				diccio[lista[i]] = self.contenido[lista[i]]

			except(KeyError):
				pass
		
		return diccio

	def mostrar(self):
		keys = self.contenido.keys()
		keys.sort()
		for i in range(0,len(keys)):
			print '- '+ str(keys[i])
		print ''

	def extraer(self,modo):
		#-- modo = 0: devuelve el valor
		# -- modo = 1: devuelve la Key
		error = 1
		while (error == 1):
			key = raw_input("> ")
			error = 0
			try:
				resultado = self.contenido[key]

			except(KeyError):
				print "El item no existe"
				error = 1
		if (modo == 0):
			return resultado

		if (modo == 1):
			return key			

	def random(self):
		listakeys = self.contenido.keys()
		key = random.sample(listakeys,1)				

		return key[0], self.contenido[key[0]]
#-------------------------------------------------
# ---------------  Comprar Tipo  -----------------
#-------------------------------------------------
# Funcion que compara tipo de datos, cuando quiere modificarse una variable de la lista Variables
# se llama a esta funcion que decide que tipo de dato debe ser ingresado y luego lo devuelve en el Tipo correcto.
def comparartipo(valoracomparar):
	error = 1
	while (error == 1):
		error = 0
		valor = raw_input("> ")

		if (type(valoracomparar) == type(int())):
			try:
				valor = int(valor)

			except(ValueError):
				error = 1
		
		if (type(valoracomparar) == type(float())):
			try:
				valor = float(valor)

			except(ValueError):
				error = 1

		if (type(valoracomparar) == type(complex())):
			try:
				valor = complex(valor)

			except(ValueError):
				error = 1

		if (type(valoracomparar) == type(str())):
			try:
				valor = str(valor)

			except(ValueError):
				error = 1

		if (type(valoracomparar) == type(list())):
			try:
				valor = list(valor)

			except(ValueError):
				error = 1
		
	return valor

#-------------------------------------------------
# ---------  funciones para colorear  ------------
#-------------------------------------------------
def rojo(color):
	return [color,0,0]

def verde(color):
	return [0,color,0]

def azul(color):
	return [0,0,color]

def amarillo(color):
	return [color,color,0]

def celeste(color):
	return [0,color,color]

def magenta(color):
	return [color,0,color]

def blanco(color):
	return [color,color,color]

#-------------------------------------------------
# --------------  Clase Pantalla  ----------------
#-------------------------------------------------
# Esta es la clase principal y permite hacer todas las opciones posibles.
# ----
# variables, funciones y colores son 3 Diccionarios que contienen dichos objetos.
# xmin,xmax,ymin,ymax son los bordes del plano.

# recalcular() RECALCULA algunas variables.
# iniciar() redibuja la pygame.screen cada vez que se modifica el grafico.
# modificar() permite modificar las variables.
# cambiar_funcion() perimte cambiar el tipo de fractal.
# zoom() hace zoom in/out.
# moverx() desplaza en X.
# movery() desplaza en Y.
# graficar() dibuja el fractal con todas las variables asignadas.
# devolvercolor() sirve para darle color al fractal, arma el color dependiendo de la variable color.
# foto() guarda un screenshot.


#ratio guarda las proporciones de la pantalla (Ej: 4:3)
# lo calcula dividiendo el alto o el ancho por el mcd entre el alto y el ancho

class Pantalla():
	def __init__(self,variables,funciones,colores):
		pygame.init()
		self.colores = colores
		key,value = self.colores.random()
		self.color = self.colores.contenido[key]
		self.nombrecolor = key
		self.variables = variables
		self.screen = pygame.Surface((1,1))
		self.pxarray = pygame.PixelArray(self.screen)
		self.funciones = funciones
		self.funcion = self.funciones.contenido['mandelbrotx']
		self.nombrefuncion = 'mandelbrotx'
		self.despx = 0
		self.despy = 0
		self.despzoom = 1
		self.espera = int(self.variables.contenido['ancho']/4)

		self.ratio = []
		self.ratio.append(self.variables.contenido['ancho']/matematica.mcd(self.variables.contenido['alto'],self.variables.contenido['ancho']))
		self.ratio.append(self.variables.contenido['alto']/matematica.mcd(self.variables.contenido['alto'],self.variables.contenido['ancho']))
		self.xmin = float(-1 * self.ratio[0])
		self.xmax = float( 1 * self.ratio[0])
		self.ymin = float(-1 * self.ratio[1])
		self.ymax = float( 1 * self.ratio[1])
		self.recalcular()

	def iniciar(self):
		self.screen = pygame.display.set_mode((self.variables.contenido['ancho'],self.variables.contenido['alto']))
		pygame.display.set_caption(self.variables.contenido['titulo'])
		self.screen.fill(self.variables.contenido['fondo'])
		self.pxarray = pygame.PixelArray(self.screen)

	def recalcular(self):
		# xsalto e ysalto son los SALTOS en X e Y que se hacen 
		# cada vez que se itera la funcion para graficar.
		# escala2 devuelve una lista, colorescala la recibe con el SALTO de color que se hace en base a las iteraciones.
		self.xsalto,self.ysalto = escala(self.variables.contenido['ancho'],self.variables.contenido['alto'],self.xmin,self.ymin,self.xmax,self.ymax)

		colorescala = escala2([self.variables.contenido['iteraciones']],[0],[255])
		self.escalacolor = colorescala[0]
		self.espera = int(self.variables.contenido['ancho']/4)

	def modificar(self):
		# extraer EXTRAE el key o el valor de un diccionario (dependiendo del modo ingresado).
		# sirve como verificacion para poder extraer unicamente cosas que existan.
		# si se ingresa cancelar o salir, se ejecuta dicha accion.
		self.variables.mostrar()
		print "Modificar:"
		key = self.variables.extraer(1)
		if (key == 'cancelar'):
			pass
		else: 
			if (key == 'salir'):
				return 'salir'
			else:
				print "Valor acutal: " + str(self.variables.contenido[key])
				print "Valor nuevo:"
				valor = comparartipo(self.variables.contenido[key])
				self.variables.contenido[key] = valor
				self.iniciar()
				self.graficar()		
		
		return 0

	def ver_variables(self):
		print 'Funcion: ' + self.nombrefuncion 
		print 'Constante: ' + str(self.variables.contenido['constante'])
		print 'Color: ' + self.nombrecolor
		print 'iteraciones: ' + str(self.variables.contenido['iteraciones'])
		print 'corrimiento en X: ' + str(self.despx)
		print 'corrimiento en Y: ' + str(self.despy)
		print 'Zoom: x' + str(self.despzoom)
		print 'ancho: ' + str(self.variables.contenido['ancho'])
		print 'alto: ' + str(self.variables.contenido['alto'])
		raw_input('...')
		os.system('clear')

	def cambiar_color(self):
		print "Color acutal: " + self.nombrecolor
		print "Elegir Color:"
		self.colores.mostrar()
		key = self.colores.extraer(1)
		if (key == 'cancelar'):
			pass
		else:
			if(key == 'salir'):
				return 'salir'
			else:
				self.color = self.colores.contenido[key]
				self.nombrecolor = key
				self.graficar()	
		return 0

	def cambiar_funcion(self):	
		# Misma idea que modificar, permite seleccionar una de entre los posibles fractales.
		print "Funcion acutal: " + self.nombrefuncion
		print "Elegir Funcion:"
		self.funciones.mostrar()
		key = self.funciones.extraer(1)
		if (key == 'cancelar'):
			pass
		else:
			if(key == 'salir'):
				return 'salir'
			else:
				self.funcion = self.funciones.contenido[key]
				self.nombrefuncion = key
				self.graficar()	
		return 0	

	def zoom(self):
		print "valor: "
		razon = matematica.convertir2('float',0.0,0.0,"distinto")
		self.xmin *= razon
		self.xmax *= razon
		self.ymin *= razon
		self.ymax *= razon
		self.despzoom *= razon
		self.graficar()
		return 0

	def moverx(self):
		print "Valores positivos corren a la izquierda, negativos a la derecha"
		print "valor: "
		razon = matematica.convertir('float')
		self.xmin += razon
		self.xmax += razon
		self.despx += razon
		self.graficar()

	def movery(self):
		print "Valores positivos corren arriba, negativos abajo"
		print "valor: "
		razon = matematica.convertir('float')
		self.ymin += razon
		self.ymax += razon
		self.despy += razon
		self.graficar()

	def graficar(self):
		# graficar recorre toda la pantalla, y para cada punto del plano ejecuta la funcion seleccionada.
		self.recalcular()
		tiempo = time.time()
		pygame.Surface.fill(self.screen,self.variables.contenido['fondo'])

		# Calcular el cuadrado de radio "Norma" para realizar el proceso unicamente en ese espacio, ya que
		# todo los puntos que exedan la Norma nunca se pintan.
		# Se aprecio una mejora del 50 porciento.
		norma = self.variables.contenido['norma']
		minx = -norma
		maxx = norma
		miny = -norma
		maxy = norma

		imin = (minx - self.xmin)/self.xsalto
		imax = (maxx - self.xmin)/self.xsalto
		jmin = (miny - self.ymin)/self.ysalto
		jmax = (maxy - self.ymin)/self.ysalto
		if (imin < 0):
			imin = 0
		if (imax >self.variables.contenido['ancho']):
			imax = self.variables.contenido['ancho']
		if (jmin < 0):
			jmin = 0
		if (jmax >self.variables.contenido['alto']):
			jmax = self.variables.contenido['alto']
		
		if (self.variables.contenido['bordes'] == 1):
			pygame.draw.line(self.screen,(255,0,0),(imin,jmin),(imin,jmax))
			pygame.draw.line(self.screen,(255,0,0),(imax,jmin),(imax,jmax))
			pygame.draw.line(self.screen,(255,0,0),(imin,jmin),(imax,jmin))
			pygame.draw.line(self.screen,(255,0,0),(imin,jmax),(imax,jmax))
		#for i in range(0,self.variables.contenido['ancho']):
		#	for j in range(0,self.variables.contenido['alto']):
		for i in range(int(imin),int(imax)):
			for j in range(int(jmin),int(jmax)):
				b = (self.xsalto * i) + self.xmin 
				c = ((self.ysalto * j) + self.ymin) * 1j
				d = self.variables.contenido['constante']
				e = self.variables.contenido['norma']
				f = self.variables.contenido['exponente']
				a = self.funcion((b+c),d,self.variables.contenido['iteraciones'],e,f)
				color = int(self.escalacolor*a) 
				if (a!=1):
					self.pxarray[i,j] = self.color(color)
			if(i % self.espera == 0):
				print "."

		tiempototal = (time.time()-tiempo)
		print 'Tiempo total: '+ str(tiempototal)
		pygame.display.flip()
		return tiempototal		

	def foto(self):
		pantall = self.screen.copy()
		directorio = self.variables.contenido['directorio']
		nombrefuncion = self.nombrefuncion
		constante = str(self.variables.contenido['constante'])
		iteraciones = str(self.variables.contenido['iteraciones'])
		x = str(self.despx)
		y = str(self.despy)
		zoom = str(self.despzoom)
		color = self.nombrecolor
		extension = self.variables.contenido['extension']
		norma = str(self.variables.contenido['norma'])
		archivo = directorio+nombrefuncion+' '+constante+' -'+iteraciones+' -'+norma+' -X:'+x+' Y:'+y+' -ZOOM:'+zoom+'-'+color+extension 
		pygame.image.save(pantall,archivo)

		print "Foto Tomada !"

	def interpolar(self,desde,hasta,pasos,variable,sfoto):
	# hasta, desde y pasos son solicitados previamente.
	# variable es la VARIABLE a iterar. 
		delta = hasta - desde 
		salto = delta/ pasos
		salida = desde
		self.variables.contenido[variable] = salida	
		for i in range(0,pasos):	
			print str(i) + " de " + str(pasos)
			salida += salto
			self.variables.contenido[variable] = salida
			self.graficar()
			if (sfoto == 1):
				self.foto()

	def sesion(self):
		directoriooriginal = self.variables.contenido['directorio']
		print "Que variable se va iterar:"
		self.variables.mostrar()
		variable = self.variables.extraer(1)
		if (variable == 'iteraciones' or variable == 'alto' or variable == 'ancho'):
			print "Desde:"
			desde = matematica.convertir2('int',1,None,None)
			print "Hasta:"
			hasta = matematica.convertir2('int',1,None,None)
			print "Pasos:"
			pasos = matematica.convertir2('int',1,None,None)
			print "Guardar imagenes? (S/N)"
			sfoto = matematica.convertir('string')
			while ((hasta - desde)%pasos != 0):
				pasos -= 1

			# sfoto = SACAR FOTO 
			if (sfoto == 'S' or sfoto == 's' or sfoto == 'Y' or sfoto == 'y'):
				sfoto = 1
				a = self.nombrefuncion
				b = str(self.exponente)
				c = variable 
				d = str(desde)
				e = str(hasta)
				f = str(pasos) 
				diraux = 'Sesion-'+ self.nombrefuncion+'-'+str(self.exponente)+ '-'+variable+'-'+str(desde)+'-'+str(hasta)+'-'+str(pasos)+'/'
				directoriocompleto = directoriooriginal + diraux
				err = 1			
				constante = 1	
				while (err == 1):
					err = 0
					# Chequea que no exista una carpeta con el mismo nombre
					if(not os.path.isdir(directoriocompleto)):
						os.mkdir(directoriocompleto)
					else:
						err = 1
						directoriocompleto = directoriooriginal+'('+str(constante)+')'+diraux
						constante += 1

				self.variables.contenido['directorio'] += diraux
			else:	
				sfoto = 0
			# --interpolar--
			self.interpolar(desde,hasta,pasos,variable,sfoto)

		if (variable == 'constante' or variable == 'exponente'):
			print "Desde:"
			desde = matematica.convertir('complex')
			print "Hasta:"
			hasta = matematica.convertir('complex')
			print "Pasos:"
			pasos = matematica.convertir2('int',1,None,None)
			print "Guardar imagenes? (S/N)"
			sfoto = matematica.convertir('string')
			# sfoto = SACAR FOTO 
			if (sfoto == 'S' or sfoto == 's' or sfoto == 'Y' or sfoto == 'y'):
				sfoto = 1
				diraux = 'Sesion-'+ self.nombrefuncion+ '-'+variable+'-'+str(desde)+'-'+str(hasta)+'-'+str(pasos)+'/'
				directoriocompleto = directoriooriginal + diraux
				err = 1			
				constante = 1	
				while (err == 1):
					err = 0
					# Chequea que no exista una carpeta con el mismo nombre
					if(not os.path.isdir(directoriocompleto)):
						os.mkdir(directoriocompleto)
					else:
						err = 1
						directoriocompleto = directoriooriginal+'('+str(constante)+')'+diraux
						constante += 1

				self.variables.contenido['directorio'] += diraux
			else:	
				sfoto = 0
			# --interpolar--
			self.interpolar(desde,hasta,pasos,variable,sfoto)
		# vuelve a colocar el directorio fuera de la caperta recien creada.
		self.variables.contenido['directorio'] = directoriooriginal

#-------------------------------------------------
# --------------------  Salir  -------------------
#-------------------------------------------------
# Funcion para el menu principal, devuelve 'salir' 
# para que se corte el loop del While.
def Salir():
	return 'salir'

#-------------------------------------------------
# ------------------  Acciones  ------------------
#-------------------------------------------------

colores = Diccionario()
colores.agregar('rojo',rojo)
colores.agregar('verde',verde)
colores.agregar('azul',azul)
colores.agregar('amarillo',amarillo)
colores.agregar('celeste',celeste)
colores.agregar('magenta',magenta)
colores.agregar('blanco',blanco)

funciones = Diccionario()
funciones.agregar('asd',asd)
funciones.agregar('asd2',asd2)
funciones.agregar('asd3',asd3)
funciones.agregar('asd4',asd4)
funciones.agregar('asd5',asd5)
funciones.agregar('asd6',asd6)
funciones.agregar('qwe',qwe)
funciones.agregar('qwe2',qwe2)
funciones.agregar('qwe3',qwe3)
funciones.agregar('qwe4',qwe4)
funciones.agregar('qwe5',qwe5)
funciones.agregar('qwe6',qwe6)
funciones.agregar('zxc',zxc)
funciones.agregar('mandelbrotx',mandelbrotx)
funciones.agregar('max',maX)
funciones.agregar('juliax',juliax)
funciones.agregar('cancelar',None)
funciones.agregar('salir',None)

variables = Diccionario()
variables.agregar('ancho',200)
variables.agregar('alto',150)
variables.agregar('iteraciones',15)
variables.agregar('norma',2)
variables.agregar('directorio','/home/luciano/python_scripts/graficos/fotos/')
variables.agregar('extension','.bmp')
variables.agregar('fondo',[0,0,0])
variables.agregar('titulo',"Fractales")
variables.agregar('constante',0.718+0.5j)
variables.agregar('bordes',0)
variables.agregar('cancelar',None)
variables.agregar('salir',None)
variables.agregar('exponente',2.0)

p1 = Pantalla(variables,funciones,colores)

menu = Diccionario()
menu.agregar('modificar',p1.modificar)
menu.agregar('variables',p1.ver_variables)
menu.agregar('color',p1.cambiar_color)
menu.agregar('funcion',p1.cambiar_funcion)
menu.agregar('zoom',p1.zoom)
menu.agregar('moverx',p1.moverx)
menu.agregar('movery',p1.movery)
menu.agregar('sesion',p1.sesion)
menu.agregar('foto',p1.foto)
menu.agregar('salir',Salir)


os.system('clear')
p1.iniciar()
p1.graficar()

while (1 == 1):
	menu.mostrar()
	print "Que deseais hacer"
	opcion = menu.extraer(1)
	resultado = menu.contenido[opcion]()
	if (resultado == 'salir'):
		break

# Constantes divertidas:
# --- (julia) (1+0j)
# --- (julia) (0+1j)	
# --- (julia) (0.5+0.5j) 
# --- (julia) (-1.3+0.00525j)
# --- (julia) (-0.72-0.196j)
# --- (julia) (-0.8-0.2j) !!! 
# --- (julia) (0.4+0.3j)
# --- (julia) (0.7+0.5j)
# --- (juli4) (-0.8-0.2j)
# --- (julia5) (0.718+0.5j) !!! 
# --- (julia5) (0.71898+0.5j) !!! 
# --- ( ) ( )
# --- ( ) ( )


