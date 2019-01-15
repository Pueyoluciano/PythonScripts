#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os
import personaje

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
#----------------  Clase mapa  -------------------
#-------------------------------------------------
class mapa():
	def __init__(self):
		# matriz es el mapa vacio.
		# map es el mismo mapa pero con los bichitos.
		# entidades es un diccionario con el nombre de los bichos (incluido el player)
		# y la referencia al objeto con ese nombre.
		self.matriz = []
		self.map = []
		self.entidades = {}
		
	def ver(self):
		for i in range(0,len(self.map)):
			for j in range(0,len(self.map[0])):
				print self.map[i][j],
			print '\n',

	def cargar(self,archivo):
		mapa = open(archivo)
		vector = []
		# carga el mapa en una matriz
		linea = mapa.readline()
		while (linea != "-npcs-\n"):
			linea = sacarenter(linea)
			for dato in linea:
				vector.append(dato)
			self.matriz.append(vector)
			vector = []
			linea = mapa.readline()
		self.map = self.matriz
		# saca la info de los npcs
		while (linea != ''):
			npc = sacarenter(mapa.readline())
			if (npc != ''):
				x = sacarenter(mapa.readline())
				y = sacarenter(mapa.readline())
				self.cargarnpc(npc,x,y)
			else:
				break
		#print self.npcs
		mapa.close() 

	def cargarnpc(self,npc,x,y):
		#print npc
		#print x
		#print y
		self.entidades[npc] = personaje.jugador(x,y)
		self.map[int(y)][int(x)] = npc			
	
#-------------------------------------------------
#-----------------  Turnador  --------------------
#-------------------------------------------------
# la clase turnador maneja todas las acciones que se llevan a cabo.
# todos las acciones, automaticas o del jugador envian una "solicitud"
# a turnador y esta ejecuta la accion cuando el contador de segundos llega a 0.
class turnador():
	def __init__(self):
		# self.cola = [[accion1,tiempo1], [accion2,tiempo2], ..., [accionN,tiempoN]]
		self.cola = []
		self.salto = 0.1


	def agregar(self,accion):
		tupla = [accion,]
		self.cola.append(accion)


	def siguienteturno(self):
		for i in range(0,len(self.cola)):
			self.cola[i][1] -= salto
			if(self.cola[i][1] == 0):
				self.cola[i].accion


	def jugada(self,entidades):
		entis = entidades.items()
		for i,entidad in entis:
			pass		
		




#-------------------------------------------------
#------------------  accion  ---------------------
#-------------------------------------------------
class acciones():
	def __init__(self):
		pass
		#self.tiempo = 0.0
		#self.accion = "llamada a funcion"
	@staticmethod
	def mover(self,objeto,desplazamiento):	
		# desplazamiento: [x,y] tupla con coordenadas.
		objeto.x += desplazamiento[0]
		objeto.y += desplazamiento[1]
				
	@staticmethod	
	def pasarturno(self,objeto):	
		pass

#-------------------------------------------------
#-----------------  acciones  --------------------
#-------------------------------------------------

os.system("clear")
mapa1 = mapa()
mapa1.cargar("./mapa1")
mapa1.ver()






