

# Globales es una clase general que contiene todas los arreglos que interactuaran entre si.
#globales:
#--- jugadores
#--- turnador
#--- acciones
#--- mapa

# arreglo con la lista de todas las entidades activas, incluye jugador y monstruos..
#jugadores
#--- {"jugador1",objeto_entidad}
#--- {"jugador2",objeto_entidad}
#(...)
#--- {"jugadorN",objeto_entidad}

# Clase entidad
#entidad
#--- atributos
#	--- nombre
#	--- npc
#	--- estadisticas (vida,exp,nivel, ...)
#	--- aptitudes (fue,vit,Int, ...)
#	--- accion_pendiente
#	--- parametros_accion_pendiente
#	--- tiempo

#--- metodos
#	--- elegir_accion
#	--- ejecutar_accion
# clase turnador, maneja las acciones globales. tiene el main loop.

#turnador
#-------------------------------------------------
# ------------------  Imports  -------------------
#-------------------------------------------------
import os
import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica
import pygame
sys.path.append('/home/luciano/python_scripts/graficos')
from iniciarpy import *

#-------------------------------------------------
# -----------------  Interfaz  -------------------
#-------------------------------------------------
class Interfaz():
	def __init__(self,alto,ancho,fondo,titulo,tile):
		self.alto = alto
		self.ancho = ancho
		self.fondo = fondo
		self.titulo = titulo
		# tile es el tamano del TILE. es cuadrado.
		self.tile = tile
		self.paso = alto/tile
		self.color_cuadri =(80,80,80)
		self.mapa = []

	def iniciar(self):
		self.screen = iniciarpygame(self.ancho,self.alto,self.fondo,self.titulo)
		# cargar el mapa
		#for i in range(0,self.paso):
			

	def cuadricula(self):		
		for i in range(0,self.paso):
			# lineas verticales
			linea = pygame.draw.line(self.screen,self.color_cuadri,(self.tile*i,0),(self.tile*i,alto),1)
			#pygame.display.update(linea)			
			# lineas Horizontales
			linea = pygame.draw.line(self.screen,self.color_cuadri,(0,self.tile*i),(self.ancho,self.tile*i),1)
			pygame.display.flip()

	def dibujar(self,x,y,color):
		# X0 e y0
		xoyo = (x * self.tile, y * self.tile)
		longitudes = (self.tile,self.tile)
		cuadrado = pygame.draw.rect(self.screen,color,(xoyo,longitudes),0)
		pygame.display.update(cuadrado)

	def actualizar(self,jugadores):
		personajes = jugadores.contenido.items()
		for key, i in personajes:	
			self.dibujar(jugadores.contenido[key].estadisticas.x, jugadores.contenido[key].estadisticas.y,(100,100,100))
		self.cuadricula()
#-------------------------------------------------
# --------------  Jugador Activo  ----------------
#-------------------------------------------------
# Funcion para detectar si un jugador esta activo.
# Se pasa el nombre del jugador a verificar, y si hay una KeyError devuelve 0 (el jugador NO esta activo),
# si devuelve 1 el jugador esta activo.
def activo(key):
	try:
		aa = lista_globales.entidades.contenido[key]
	except(KeyError):
		return 0
	return 1

#-------------------------------------------------
#-------------  Calcular_cantidad  ---------------
#-------------------------------------------------
def calcular_cantidad(atacante,atacado,accion):
	cantidad = 0
	if (accion == "atacar"):
		cantidad = 20
	if (accion == "curar"):
		cantidad = 3

	return cantidad

#-------------------------------------------------
# ----------------  Elegir Lista  ----------------
#-------------------------------------------------
# modo: si el modo es igual a 1, pregunta al usuario por el item a buscar.
# Si el modo es un String, buscara ese String en la lista enviada.
def elegir_lista(lista,modo):
	if (modo == 1):
		while(1 == 1):
			item = matematica.convertir("string")
			for i in range(0,len(lista)):
				if (item == lista[i]):
					return item		
			print "el item no existe"

	else:
		for i in range(0,len(lista)):
			if (modo == lista[i]):
				return modo		
		return 0

	return 0

#-------------------------------------------------
# ---------------  Elegir Diccio  ----------------
#-------------------------------------------------
# funcion para elegir un item(y su key) de un diccionario,
# solicita la key a buscar, y si la encuentra, devuelve la key ingresada y valor en el diccionario.
# modo: si el modo es igual a 1, pregunta al usuario por el item a buscar.
# Si el modo es un String, buscara ese String en el diccionario enviado.
def elegir_diccio(diccionario,modo):
	if (modo == 1):
		error = 1
		while(error == 1):
			key = matematica.convertir("string")
			try:
				error = 0
				instancia = diccionario[key]

			except(KeyError):
				print "Escribi bien Capo"
				error = 1
		return key, instancia

	else:
		try:
			instancia = diccionario[key]

		except(KeyError):
			return 0
		
		return key, instancia

	return 0

#-------------------------------------------------
# ----------------  Clase Global  ----------------
#-------------------------------------------------
class Globales():
	def __init__(self,entidades,turnador,acciones,pantalla):
		self.entidades = entidades	
		self.turnador = turnador
		self.acciones = acciones
		self.pantalla = pantalla

#-------------------------------------------------
# ---------------  Clase entidad  ----------------
#-------------------------------------------------
# nombre:                      string con el nombre de la entidad
# npc:                         flag para saber si es jugable o no
# atravesable: 				   flag para la validacion de mover()
# estadisticas:                (vida,exp,nivel, ...)
# aptitudes:                   (fue,vit,Int, ...)
# acciones:                    lista de Strings, con las acciones que puede realizar la entidad.
# accion_pendiente:            lista con las acciones pendientes a realizar, y el tiempo restante.
# --- Ej: [[1,"mover"],[4,"mover"],[4,"mover"]]

# parametros_accion_pendiente: lista con los parametros relacionados a las acciones pendientes,
# estan ordenados de modo que la primera accion se corresponda con el primer parametro.
# --- Ej: [[objeto_entidad,[x1,y1]],[objeto_entidad,[x2,y2]],[objeto_entidad,[x3,y3]]] 

class Entidad():
	def __init__(self,nombre,npc,atravesable,estadisticas,aptitudes,acciones):
		self.nombre = nombre
		self.npc = npc
		self.atravesable = atravesable
		self.estadisticas = estadisticas
		self.aptitudes = aptitudes
		self.acciones = acciones		
		self.accion_pendiente = []
		self.parametros_pendiente = []

	def elegir(self,g_acciones):
		if (self.npc == 0):
			print "que haces?"
			accion = elegir_lista(self.acciones,1)
		else:
			accion = inteligencia_artificial("elegir")
		tiempo,parametros = g_acciones.contenido[accion].solicitar(self)
		self.accion_pendiente.append([tiempo,accion])
		self.parametros_pendiente.append(parametros)
		
	def ejecutar(self,g_acciones):
		flag = g_acciones.contenido[self.accion_pendiente[0][1]].ejecutar(self.parametros_pendiente[0])
		self.accion_pendiente.remove(self.accion_pendiente[0])
		self.parametros_pendiente.remove(self.parametros_pendiente[0])
		return flag

	def morir(self):
		lista_globales.pantalla.dibujar(self.estadisticas.x,self.estadisticas.y,(0,0,0))
		lista_globales.entidades.quitar(self.nombre)
		

	
#-------------------------------------------------
# --------------  Clase turnador  ----------------
#-------------------------------------------------
class Turnador():
	def __init__(self,salto):
		self.salto = salto
		self.tiempototal = 0

	def seleccion(self,jugadores):
		# elegir accion si es posible
		personajes = jugadores.contenido.items()
		for key, i in personajes:
			if (jugadores.contenido[key].accion_pendiente == []):
				print "\njuega: " + key
				print	"vida: "+ str(jugadores.contenido[key].estadisticas.vida)
				print	"Nivel: "+ str(jugadores.contenido[key].estadisticas.nivel)
				print	"x: "+ str(jugadores.contenido[key].estadisticas.x) + " y: " + str(jugadores.contenido[key].estadisticas.y)
				jugadores.contenido[key].elegir(lista_acciones)

	def ejecucion(self,jugadores):
		#ejecuta accion si es posible	
		personajes = jugadores.contenido.items()
		for key, j in personajes:
			if (activo(key) == 1):
				jugadores.contenido[key].accion_pendiente[0][0] -= self.salto
				if (jugadores.contenido[key].accion_pendiente[0][0] == 0):
					flag = jugadores.contenido[key].ejecutar(lista_globales.acciones)
					if(type(flag) == type(tuple())):
						if (flag[0] == "muerto"):
							print str(jugadores.contenido[flag[1]].nombre) + " ha muerto"
							jugadores.contenido[flag[1]].morir()					

	def turno(self,jugadores):
		self.seleccion(jugadores)
		self.ejecucion(jugadores)
		lista_globales.pantalla.actualizar(jugadores)

		self.tiempototal += 1

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

#-------------------------------------------------
# ----------------  Clase pasar  -----------------
#-------------------------------------------------
class Pasar():
	def __init__(self):
		self.tiempo = 1

	def solicitar(self,jugador):
		if (jugador.npc == 0):
			pass

		else:
			pass
				
		return self.tiempo,[jugador]

	def ejecutar(self,parametros):
		print parametros[0].nombre + " pasa"	

#-------------------------------------------------
# ---------------  Clase atacar  -----------------
#-------------------------------------------------
class Atacar():
	def __init__(self):
		self.tiempo = 5

	def solicitar(self,jugador):
		if (jugador.npc == 0):
			print "a quien?"
			nombre,objetivo = elegir_diccio(lista_globales.entidades.contenido,1)
		else:
			objetivo = inteligencia_artificial("atacar")
		
		cantidad = calcular_cantidad(jugador,objetivo,"atacar")				
				
		return self.tiempo,[objetivo,cantidad]

	def ejecutar(self,parametros):
		print  parametros[0].nombre + " es atacado"
		parametros[0].estadisticas.vida -= parametros[1]
		if (parametros[0].estadisticas.vida <= 0):
			resultado = "muerto", parametros[0].nombre	
			return resultado
	
#-------------------------------------------------
# ----------------  Clase Mover  -----------------
#-------------------------------------------------
class Mover():
	def __init__(self):
		self.tiempo = 4


	def validacion(self,jugador,objetivo):
		if (objetivo.atravesable == 1):
			return 1

		else:
			pass
			
		

	def solicitar(self,jugador):
		#  7  8   9
		#  \  |  /   
		#4 -- 5 -- 6	
		#  /  |  \
        # 1   2  3
		mapeo = Diccionario()
		mapeo.agregar(1,[-1,1])
		mapeo.agregar(2,[0,1])
		mapeo.agregar(3,[1,1])
		mapeo.agregar(6,[1,0])
		mapeo.agregar(9,[1,-1])
		mapeo.agregar(8,[0,-1])
		mapeo.agregar(7,[-1,-1])
		mapeo.agregar(4,[-1,0])

		if (jugador.npc == 0):
			print "a donde?"		
			error = 1
			while (error == 1):
				error = 0
				lugar = matematica.convertir("int")
				try:
					instancia = mapeo.contenido[lugar]
				except(KeyError):
					error = 1
		else:
			lugar = inteligencia_artificial("mover")		

		x = mapeo.contenido[lugar][0]
		y = mapeo.contenido[lugar][1]

		return self.tiempo,[jugador,[x,y]]

	def ejecutar(self,parametros):
		lista_globales.pantalla.dibujar(parametros[0].estadisticas.x,parametros[0].estadisticas.y,(0,0,0))
		print parametros[0].nombre + " se mueve"
		parametros[0].estadisticas.x += parametros[1][0] 
		parametros[0].estadisticas.y += parametros[1][1]

#-------------------------------------------------
# ------------  Clase Estadisticas  --------------
#-------------------------------------------------
class Estadisticas():
	def __init__(self,tipo):
		if (tipo == "jugador"):
			#diccio = {}
			self.vida = 20
			self.experiencia = 0
			self.nivel = 1
			self.x = 0
			self.y = 0

#-------------------------------------------------
# -------------------  Main  ---------------------
#-------------------------------------------------
lista_acciones = Diccionario()
lista_acciones.agregar("atacar",Atacar())
lista_acciones.agregar("mover",Mover())
lista_acciones.agregar("pasar",Pasar())

lista_entidades = Diccionario()
lista_entidades.agregar("pepe",Entidad("pepe",0,0,Estadisticas("jugador"),[],[]))
lista_entidades.agregar("carl",Entidad("carl",0,0,Estadisticas("jugador"),[],[]))

lista_entidades.contenido["carl"].estadisticas.x = 5
lista_entidades.contenido["carl"].estadisticas.y = 5

lista_entidades.contenido["pepe"].acciones = ["mover","atacar","pasar"]
lista_entidades.contenido["carl"].acciones = ["mover","atacar","pasar"]

#lista_entidades.contenido["pepe"].elegir(lista_acciones)
#lista_entidades.contenido["pepe"].ejecutar(lista_acciones)

turnero = Turnador(1)

alto = 300
ancho =  300
fondo = (0,0,0)
titulo = "finalrl"
tile = 30
pantalla = Interfaz(alto,ancho,fondo,titulo,tile)

lista_globales = Globales(lista_entidades,turnero,lista_acciones,pantalla) 


lista_globales.pantalla.iniciar()
lista_globales.pantalla.actualizar(lista_globales.entidades)


while (1 == 1):
	turnero.turno(lista_globales.entidades)


