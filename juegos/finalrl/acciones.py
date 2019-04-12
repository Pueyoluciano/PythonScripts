#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os
import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica

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

	def agregar_entidad(entidad):
		self.entidades[entidad.nombre] = entidad


#-------------------------------------------------
#-----------------  acciones  --------------------
#-------------------------------------------------
mapa0 = mapa()
mapa0.cargar("mapa0")

mapa0.ver()


