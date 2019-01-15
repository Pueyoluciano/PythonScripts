#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os
import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica

#-------------------------------------------------
#----------------  Elegir Accion  ----------------
#-------------------------------------------------
# funcion para elegir una accion; toma como entrada un diccionario, 
# solicita la key a buscar, y si la encuentra, devuelve la key ingresada y valor en el diccionario.
def elegir_accion(diccionario):
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

#-------------------------------------------------
#-------------  Calcular_cantidad  ---------------
#-------------------------------------------------
def calcular_cantidad(atacante,atacado,accion):
	cantidad = 0
	if (accion == "atacar"):
		cantidad = 5
	if (accion == "curar"):
		cantidad = 3

	return cantidad

#-------------------------------------------------
#---------------------  I. A. --------------------
#-------------------------------------------------
def inteligencia_artificial():
	pass
	return 0

#-------------------------------------------------
#----------------  Clase Jugador  ----------------
#-------------------------------------------------
#Clase jugador.
# npc ------------------------- bool para saber si es un npc o no.
# accion_pendiente ------------ guarda la key de la accion a realizar.
# parametros_accion_pendiente - guarda todos los parametros que necesita la accion a ejecutarse.
# tiempo ---------------------- integer que guarda el tiempo restante para ejecutar la accion.
# acciones -------------------- diccionario con las acciones realizables.
# x,y ------------------------- coordenadas espaciales ;).
# vida ------------------------ vida del jugador. 
# mana ------------------------ mana del jugador.
# numero ---------------------- Numero de orden para el mapa.

class jugador():
	def __init__(self,nombre,equipo,inventario,acciones,x,y):
		self.nombre = nombre
		self.npc = 0
		self.numero = 0
		self.accion_pendiente = ""
		self.parametros_accion_pendiente = []
		self.tiempo = 0
		self.acciones = acciones
		self.inventario = inventario
		self.equipo = equipo
		self.x = x
		self.y = y
		self.vida = 20
		self.mana = 5
	
	def elegir(self):
		print "que haces?"
		self.accion_pendiente,resultado = elegir_accion(self.acciones)
		self.tiempo, self.parametros_accion_pendiente = resultado.solicitar(globales.jugadores[self.nombre])
		

	def ejecutar(self):
		self.acciones[self.accion_pendiente].ejecutar(self.parametros_accion_pendiente)
		self.accion_pendiente = ""
		self.parametros_accion_pendiente = []
	
# Todas las acciones tienen 2 metodos:
# solicitar y ejecutar
# Solicitar es llamado cuando se elige accion; cada accion tendra distintas solicitudes,
# por ejemplo atacar solicita el jugador que va a ser atacado, y devuelve el tiempo de la accion,
# que es un atributo de la clase, y una lista con todos los parametros que necesita para la ejecucion.
# ---
# Ejecutar es llamado cuando se va a realizar la accion, recibe como entrada la lista con los parametros
# que se nombra anteriormente y ejecuta el codigo con estos datos.
#-------------------------------------------------
#-----------------  Clase pasar  -----------------
#-------------------------------------------------
class pasar():
	def __init__(self):
		self.tiempo = 1

	def solicitar(self,jugador):
		if (jugador.npc == 0):
			pass

		else:
			pass
				
		return self.tiempo,[]

	def ejecutar(self,parametros):
		pass

#-------------------------------------------------
#-----------------  Clase curar  -----------------
#-------------------------------------------------
class curar():
	def __init__(self):
		self.tiempo = 6
		self.mana = 1

	def solicitar(self,jugador):
		if (jugador.npc == 0):
			print "a quien?"
			nombre,objetivo = elegir_accion(globales.jugadores)
		else:
			objetivo = inteligencia_artificial("curar")
		
		cantidad = calcular_cantidad(jugador,objetivo,"curar")				
				
		return self.tiempo,[objetivo,cantidad]

	def ejecutar(self,parametros):
		parametros[0].vida += parametros[1]
		parametros[0].mana -= self.mana

#-------------------------------------------------
#----------------  Clase atacar  -----------------
#-------------------------------------------------
class atacar():
	def __init__(self):
		self.tiempo = 5

	def solicitar(self,jugador):
		if (jugador.npc == 0):
			print "a quien?"
			nombre,objetivo = elegir_accion(globales.jugadores)
		else:
			objetivo = inteligencia_artificial("atacar")
		
		cantidad = calcular_cantidad(jugador,objetivo,"atacar")				
				
		return self.tiempo,[objetivo,cantidad]

	def ejecutar(self,parametros):
		parametros[0].vida -= parametros[1]

#-------------------------------------------------
#-----------------  Clase Mover  -----------------
#-------------------------------------------------
class mover():
	def __init__(self):
		self.tiempo = 4

	def solicitar(self,jugador):
		if (jugador.npc == 0):
			print "a donde?"
			lugar = matematica.convertir("int")
		else:
			lugar = inteligencia_artificial("mover")		

		if (lugar == 1 ):
			x = -1
			y = -1

		if (lugar == 2 ):
			x = 0
			y = -1

		if (lugar == 3 ):
			x = 1
			y = -1

		if (lugar == 6 ):
			x = 1
			y = 0

		if (lugar == 9 ):
			x = 1
			y = 1

		if (lugar == 8 ):
			x = 0
			y = 1

		if (lugar == 7 ):
			x = -1
			y = 1
 
		if (lugar == 4 ):
			x = -1
			y = 0

		globales.mapa.actualizar()

		return self.tiempo,[jugador,[x,y]]

	def ejecutar(self,parametros):
		parametros[0].x += parametros[1][0] 
		parametros[0].y += parametros[1][1]
 
#-------------------------------------------------
#-----------------  Turnador  --------------------
#-------------------------------------------------
# Maneja los turnos y todas las acciones que se realizan.
class turnador():
	def __init__(self,jugadores):
		self.jugadores = jugadores
		self.salto = 1
		self.tiempototal = 0

	def visualizar_jugadores(self,jugadores):
		personajes = jugadores.items()			
		os.system("clear")
		for key,i in personajes:
			print "---------------"
			print "Nombre: " + str(key)
			print "- Vida: " + str(jugadores[key].vida)
			print "- Mana: " + str(jugadores[key].mana)
			print "- x: " + str(jugadores[key].x) + " y: " +  str(jugadores[key].y)
			print "- tiempo: " + str(jugadores[key].tiempo)			
			print "---------------\n"

	def loop(self):
		while (1 == 1):
			# elegir accion si es posible
			personajes = self.jugadores.items()
			self.visualizar_jugadores(self.jugadores)
			for key, i in personajes:
				if (self.jugadores[key].accion_pendiente == ""):
					print "juega: " + key
					jugadores[key].elegir()
					self.visualizar_jugadores(self.jugadores)	

			#ejecuta accion si es posible							
			for key, j in personajes:
				self.jugadores[key].tiempo -= self.salto
				print key + " Tiempo restante: "+ str(self.jugadores[key].tiempo)

				if (self.jugadores[key].tiempo == 0):
					jugadores[key].ejecutar()
					globales.mapa.ver()
				
			self.tiempototal += self.salto
			print "Tiempo total: " + str(self.tiempototal)

#-------------------------------------------------
# -------------------  Equipo  -------------------
#-------------------------------------------------
class equipo():
	def __init__(self):
		self.equipo = {}
		self.equipo["cabeza"] = ""
		self.equipo["torzo"] = ""
		self.equipo["piernas"] = ""
		self.equipo["pies"] = ""
		self.equipo["manos"] = ""
		self.equipo["capa"] = ""
		self.equipo["anillo1"] = "" 
		self.equipo["anillo2"] = ""
		self.equipo["colgante"] = ""
		self.equipo["mano_der"] = ""
		self.equipo["mano_izq"] = ""

#-------------------------------------------------
# ---------  Sacar el enter de un STR  -----------
#-------------------------------------------------
# copia un string igual que el que entra pero sin el "\n"
def sacarenter(palabra):
	palabra2 = ''
	for i in range(0,len(palabra)-1):	
		palabra2 += palabra[i]
	return palabra2

#-------------------------------------------------
#---------------------  Mapa  --------------------
#-------------------------------------------------
class mapa():
	def __init__(self):
		# matriz es el mapa vacio.
		# map es el mismo mapa pero con los bichitos.
		self.matriz = []
		self.map = []
		self.entidades = {}
		self.contador_entis = 0

	def cargar(self,archivo):
			mapa = open(archivo)
			vector = []
			# carga el mapa en una matriz
			linea = mapa.readline()
			while (linea != ""):
				linea = sacarenter(linea)
				for dato in linea:
					vector.append(dato)
				self.matriz.append(vector)
				vector = []
				linea = mapa.readline()
			self.map = self.matriz

	def ver(self):
		os.system("clear")
		for i in range(0,len(self.map)):
			for j in range(0,len(self.map[0])):
				print self.map[i][j],
			print '\n',
	
	def cargar_jugadores(self,jugadores):
		personajes = jugadores.items()
		for key, i in personajes:
			jugadores[key].numero = self.contador_entis
			self.contador_entis += 1
		self.actualizar()

	def actualizar(self):
		personajes = globales.jugadores.items()
		for key, i in personajes:
			self.map[globales.jugadores[key].x][globales.jugadores[key].y] = globales.jugadores[key].numero

#-------------------------------------------------
#-----------------  Globales  --------------------
#-------------------------------------------------
class Globales():
	def __init__(self,acciones,jugadores,turnador,mapa):
		self.acciones = acciones
		self.jugadores = jugadores
		self.turnador = turnador
		self.mapa = mapa


#-------------------------------------------------
# --------------------  Main  --------------------
#-------------------------------------------------



equipo1 = equipo()
inventario = {}





acciones = {}
acciones["mover"] = mover()
acciones["atacar"] = atacar()
acciones["curar"] = curar()
acciones["pasar"] = pasar()

jugadores = {}
jugadores["pepe"] = jugador("pepe",equipo1,inventario,acciones,1,1)
jugadores["carl"] = jugador("carl",equipo1,inventario,acciones,4,4)

mapa0 = mapa()
mapa0.cargar("mapa0")

turnero = turnador(jugadores)

globales = Globales(acciones,jugadores,turnero,mapa0)

globales.mapa.cargar_jugadores(globales.jugadores)

globales.turnador.loop()


		








	
