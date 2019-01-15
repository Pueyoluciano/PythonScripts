import os
import math
import random
from datetime import datetime
from Variable import *
from validador import *

class Automata2d:
	def __init__(self):			
		self.vars = {}
		self.mapaReglas = {}
		self.grilla =[[]]
		self.grillaOpciones = {"medio":self.iniciarGrillaMedio,"vacia":self.iniciarGrillaVacia,"llena":self.iniciarGrillaLlena,"random":self.iniciarGrillaRandom}
		
		self.vars["charset"] = Variable([".","#"],False,self.modifCharSet) 
		self.vars["tamano"] = Variable(50,False,self.modifTamano,2) 
		self.vars["iteraciones"] = Variable(50,False,self.modifGenerico,1) 
		self.vars["fileOut"] = Variable(os.getcwd() + "\\automata2DOut.txt",False,self.modifGenerico)
		self.vars["regla"] = Variable("01101110",False,self.modifRegla,"00000000","11111111") # 01101110 bin = 110 dec
		self.vars["funcioniniciadora"] = Variable(self.grillaOpciones["random"],False,self.modifFuncionGeneradora)
		
		self.iniciarMapa(self.vars["regla"].valor)
		self.iniciarGrilla()
		# self.iniciarGrillaRandom()
#[["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"]]
		
	def iniciarGrilla(self):
		self.grilla = [[]]	
		self.vars["funcioniniciadora"].valor()
					
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

	def variables(self):
		keys = self.vars.keys()
		keys.sort()
		for key in keys:
			print "-" + key + ":",self.vars[key].valor	
	
	def modificar(self):
		print "variable a modificar:"
		for (i,clave) in enumerate(self.vars.keys()):
			print str(i+1) + ") " + clave, ":",self.vars[clave].valor 

		key = validador.ingresar(str,validador.igual,self.vars.keys())
		
		print "valor actual: ", self.vars[key].valor
		self.vars[key].modificador(key)
		self.generar()
		
	def modifGenerico(self,key):
		tipo = type(self.vars[key].valor)
		self.vars[key].valor = validador.ingresar(tipo,validador.entre,self.vars[key].minimo,self.vars[key].maximo)
		
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
		
	def modifGrilla(self,key):
		pass
	
	def modifFuncionGeneradora(self,key):
		for (i,clave) in enumerate(self.grillaOpciones.keys()):
			print str(i+1) + ") " + clave
			
		clave = validador.ingresar(str,validador.igual,self.grillaOpciones.keys())
		self.vars["funcioniniciadora"].valor = self.grillaOpciones[clave]
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
		archivo = open(self.vars["fileOut"].valor,"w")
		archivo.write(str(self.vars) + "\n")
		archivo.write("Creado: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n")

		for i in range(0,self.vars["iteraciones"].valor):
			for j in range(0,self.vars["tamano"].valor):
				indice = int(grilla[i][j])
				char = self.vars["charset"].valor[indice]
				archivo.write(char)
			archivo.write("\n")
		archivo.close()
		
	def verFile(self):
		os.startfile(self.vars["fileOut"].valor)