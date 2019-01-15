#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os

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
		self.matriz = []
		self.map = []
		self.npcs = {}
		
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
		print self.npcs
		mapa.close() 

	def cargarnpc(self,npc,x,y):
		print npc
		print x
		print y
		self.npcs[npc] = personaje(x,y)
		self.map[int(y)][int(x)] = npc			

#-------------------------------------------------
#---------------  Clase personaje  ---------------
#-------------------------------------------------
class personaje():
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def mover(self):
		pass

	def pasar(self):
		pass
	
#-------------------------------------------------
#-----------------  Turnador  --------------------
#-------------------------------------------------
class turnador():
	def __init__(self):
		pass

#-------------------------------------------------
#-----------------  acciones  --------------------
#-------------------------------------------------


os.system("clear")
mapa1 = mapa()
mapa1.cargar("./mapa1")
mapa1.ver()





