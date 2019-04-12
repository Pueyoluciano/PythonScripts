# Esta clase sirve para hacer Menus para interaccion con el usuario.
# es un arbol donde cada Nodo tiene un nombre, un texto y una lista de nodos.
# el Leaf es un nodo que tiene la accion concreta.

# Expandir muestra todo el arbol.
# evaluar permite ejecutar la operacion deseada recorriendo el arbol 1 nodo a la vez.

from validador import *

class Nodo:		
	def __init__(self,nombre,texto,*nodos):
		self.nodos = []
		self.nombre = nombre
		self.texto = texto
		self.nodos.extend(nodos)
		
	def expandir(self):
		print self.nombre
		for nodo in self.nodos:
			nodo.expandir()
	
	def evaluar(self):
		print self.nombre
		print self.texto
		for i in range(0, len(self.nodos)):
			print str(i+1)+") " + self.nodos[i].nombre
			
		indice = validador.ingresar(int,validador.entre,1, len(self.nodos))			
		return self.nodos[indice-1].evaluar()
	
	def agregar(self,i,nodo):
		self.nodos.insert(i,nodo)
	
class Leaf:
	def __init__(self,nombre,texto,accion):
		self.nombre = nombre
		self.texto = texto
		self.accion = accion
	
	def expandir(self):
		print self.nombre	
	
	def evaluar(self):
		print self.texto
		return self.accion()