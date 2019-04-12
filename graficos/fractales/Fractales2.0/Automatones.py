import os
import Aplicacion
import math
import random
from datetime import datetime
from Menu import *
from Variable import *

class Automatones(Aplicacion.Aplicacion):
	def iniciar(self):
	
		self.mapaReglas = {}
		self.grilla =[[]]
		self.grillaOpciones = {"medio":self.iniciarGrillaMedio,"vacia":self.iniciarGrillaVacia,"llena":self.iniciarGrillaLlena,"random":self.iniciarGrillaRandom}
		
		self.vars["charset"] = Variable([".","#"],self.modifCharSet) 
		self.vars["tamano"] = Variable(50,self.modifTamano,2) 
		self.vars["iteraciones"] = Variable(50,self.modifGenerico,1) 
		self.vars["regla"] = Variable("01101110",self.modifRegla,"00000000","11111111") # 01101110 bin = 110 dec
		self.vars["funcioniniciadora"] = Variable("random",self.modifFuncionGeneradora)

		leaf1 = Leaf("Generar","Escribe el archivo de salida con el automata configurado",self.generar)
		self.agregarMenu(0,leaf1)
		
		self.agregarPostFunciones(self.generar)
		
		self.iniciarMapa(self.vars["regla"].valor)
		self.iniciarGrilla()

	def iniciarGrilla(self):
		self.grilla = [[]]	
		clave = self.vars["funcioniniciadora"].valor
		self.grillaOpciones[clave]()
					
	def iniciarGrillaMedio(self):
		self.grilla = [[]]
		mitad = math.ceil(self.vars["tamano"].valor/2.0)		
		espar = not(self.vars["tamano"].valor%2)
		for i in range(0,self.vars["tamano"].valor):
			if(i == mitad or (espar and i == mitad+1)):
				self.grilla[0].append("1")
			else:
				self.grilla[0].append("0")
	
	def iniciarGrillaVacia(self):
		self.grilla = [[]]
		for i in range(0,self.vars["tamano"].valor):
			self.grilla[0].append("0")
	
	def iniciarGrillaLlena(self):
		self.grilla = [[]]
		for i in range(0,self.vars["tamano"].valor):
			self.grilla[0].append("1")

	def iniciarGrillaRandom(self):
		self.grilla = [[]]
		for i in range(0,self.vars["tamano"].valor):
			self.grilla[0].append(random.choice(["0","1"]))
			
	def iniciarMapa(self,regla):
		self.mapaReglas = {"000":regla[7],
							"001":regla[6],
							"010":regla[5],
							"011":regla[4],
							"100":regla[3],
							"101":regla[2],
							"110":regla[1],
							"111":regla[0]}
		
	def modifCharSet(self,key):
		self.vars["charset"].valor[0] = validador.ingresar(str)
		self.vars["charset"].valor[1] = validador.ingresar(str)

	def modifRegla(self,key):
		# keys = self.mapaReglas.keys()
		# for regla in keys:
			# print str(regla) + ":"
			# self.mapaReglas[regla] = validador.ingresar(str,validador.igual,"0","1")
	
		regla = validador.ingresar(str,validador.entre,self.vars["regla"].minimo,self.vars["regla"].maximo)
		regla = regla.zfill(8)

		self.mapaReglas["111"] = regla[0]
		self.mapaReglas["110"] = regla[1]
		self.mapaReglas["101"] = regla[2]
		self.mapaReglas["100"] = regla[3]
		self.mapaReglas["011"] = regla[4]
		self.mapaReglas["010"] = regla[5]
		self.mapaReglas["001"] = regla[6]
		self.mapaReglas["000"] = regla[7]	
		
		self.vars["regla"].valor = regla[:7]
		
	def modifGrilla(self,key):
		pass
	
	def modifFuncionGeneradora(self,key):
		for (i,clave) in enumerate(self.grillaOpciones.keys()):
			print str(i+1) + ") " + clave
			
		clave = validador.ingresar(str,validador.igual,self.grillaOpciones.keys())
		self.vars["funcioniniciadora"].valor = clave
		self.iniciarGrilla()

	def modifTamano(self,key):
		self.vars["tamano"].valor = validador.ingresar(int,validador.entre,self.vars["tamano"].minimo, self.vars["tamano"].maximo)
		self.iniciarGrilla()
		
	def generar(self):		
		grillaAux = self.grilla[:]
		print grillaAux
		for i in range(0,self.vars["iteraciones"].valor):
			grillaAux.append([])
			for j in range(0,self.vars["tamano"].valor):
				# en estos IF se arma el numero binario de 3 digitos, que forman la vecindad. la vecindad es el punto que estoy mirando y los puntos inmediatos a su derecha e izquierda. cada punto tiene un 1 o un 0, en total formando un numero de 3 digitos binario, este numero es el indice de mi mapa de reglas, y asi se decide como se pintara el punto del medio en la siguiente iteracion.
				if(j == 0):
					vecindad = "0" + grillaAux[i][j] + grillaAux[i][j+1]
					
				else: 
					if(j == self.vars["tamano"].valor - 1):
						vecindad = grillaAux[i][j-1] + grillaAux[i][j] + "0"
					
					else:
						vecindad = grillaAux[i][j-1] + grillaAux[i][j] + grillaAux[i][j+1]
						
				grillaAux[i+1].append(self.aplicarRegla(vecindad))
				
		self.escribirOUT(grillaAux)
		return grillaAux[0] #retorno la ultima linea de la grilla
		
	def aplicarRegla(self,vecindad):
		return self.mapaReglas[vecindad]

	def escribirOUT(self,grilla):
		archivo = open(self.vars["outFile"].valor,"w")
		archivo.write(str(self.vars) + "\n")
		archivo.write("Creado: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n")

		for i in range(0,self.vars["iteraciones"].valor):
			for j in range(0,self.vars["tamano"].valor):
				indice = int(grilla[i][j])
				char = self.vars["charset"].valor[indice]
				archivo.write(char)
			archivo.write("\n")
		archivo.close()		
		
		
if __name__ == '__main__':	
	a = Automatones("Automatones","1.0.0")
	a.menuPrincipal()		