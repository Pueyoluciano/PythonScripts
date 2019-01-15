#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os
from math import *

#-------------------------------------------------
#----------------  Evaluar Rango -----------------
#-------------------------------------------------
# Evalua que el Item este entre el valor minimo y maximo ingresado, si los supera, iguala el item a este valor.
def rango(item,minimo,maximo):
	if (item > maximo):
		item = maximo
	if (item < minimo):	
		item = minimo
	return item

#-------------------------------------------------
#-------------------  Norma 2  -------------------
#-------------------------------------------------
#Funcion que calcula la norma 2 de un numero complejo.
def norma(numero):
	numero = sqrt((numero.real*numero.real)+(numero.imag*numero.imag))
	return float(numero)

#-------------------------------------------------
#----------------  Mostrar como  -----------------
#-------------------------------------------------
# Muestra el valor de entrada con el formato indicado en tipo.
def mostrarcomo(valor,tipo):
	#--tipo:
	#--- int: muestra la parte entera, si la parte imaginaria es 0 no la muestra.
	#--- float: muestra la parte real, si la parte imaginaria es 0 no la muestra.
	#--- complex: muestra el numero complejo con la parte imaginaria incluso si es 0.
	if (valor.imag == 0):
		aux = valor- int(valor.real)
		if (aux == 0):
			if (tipo == 'int'):
				print int(valor.real) ,
			if (tipo == 'float'):
				print float(valor.real) ,
			if (tipo == 'complex'):
				print complex(valor) ,
		else:
			print float(valor.real),
	else:
		print complex(valor),

#-------------------------------------------------
#------------------  Convertir  ------------------
#-------------------------------------------------
# Convierte el dato que recibe con el raw_iput al tipo que se indica en entrada.
def convertir(entrada):
	err = 1
	while (err == 1):
		err = 0
		try:
			if(entrada == 'int'):
				valor = int(raw_input("> "))
				
			if(entrada == 'float'):
				valor = float(raw_input("> "))

			if(entrada == 'string'):
				valor = str(raw_input("> "))

			if(entrada == 'complex'):
				valor = complex(raw_input("> "))
		except(ValueError):
			err = 1
	return valor

#-------------------------------------------------
#-----------  Suma/resta de matrices  ------------
#-------------------------------------------------
#Suma/Resta dos matrices de dimensiones iguales.
def sumaresta(matriza,matrizb,signo):
	if (matriza.filas == matrizb.filas and matriza.columnas == matrizb.columnas):
		if(signo == "+"):
			for i in range(0,matriza.filas):
				for j in range(0,matriza.columnas):
					matriza.matriz[i][j] += matrizb.matriz[i][j]
		if(signo == "-"):
			for i in range(0,matriza.filas):
				for j in range(0,matriza.columnas):
					matriza.matriz[i][j] -= matrizb.matriz[i][j]
	else:
		print "las matrices tienen dimensiones distintas"
	return matriza

#-------------------------------------------------
#------------  producto de matrices  -------------
#-------------------------------------------------
#Producto matricial.
def producto(matriza,matrizb):
	if (matriza.columnas == matrizb.filas):	
		aux = 0
		matrizc = matriz([matriza.filas,matrizb.columnas])
		for i in range(0,matrizc.filas):
			for j in range(0,matrizc.columnas):
				aux = 0
				for k in range(0,matriza.columnas):
					aux += matriza.matriz[i][k] * matrizb.matriz[k][j]
				matrizc.matriz[i][j] = aux	
				print "---------"						
				matrizc.visualizar(0,'int')
		return matrizc
	else: 
		print "Las matrices no son multiplicables"

#-------------------------------------------------
#----------------  crear matriz  -----------------
#-------------------------------------------------
#Crea una matriz de numeros complejos.
def crearmatriz(filas,columnas):
	matriz = []
	for i in range(0,int(filas)):
		matriz.append([])	
		for j in range(0,int(columnas)):
			matriz[i].append(complex(0))
	return matriz


#-------------------------------------------------
#-----------------  Restar Fila  -----------------
#-------------------------------------------------
# Resta la fila de la matriz en el indice indicado con la fila entregada como parametro.
def restarfila(matriz,fila,indice):
	for i in range(0,len(fila)):
		matriz[indice][i] -= fila[i]
	return matriz

#-------------------------------------------------
#---------------  Multiplicar Fila  --------------
#-------------------------------------------------
# Multiplica la fila por el factor indicado.
def multiplicarfila(fila,factor):
	for j in range(0,len(fila)):
		fila[j] = fila[j]* factor
	return fila

#-------------------------------------------------
#-------------  Multiplicar Matriz  --------------
#-------------------------------------------------
# Multiplica la fila de la matriz por el factor indicado.
# hay que pasarle cuantas columnas tiene la matriz.
def multiplicarmatriz(matriz,fila,factor,columnas):
	for j in range(0,columnas):
		matriz[fila][j] = matriz[fila][j] * factor
	return matriz

#-------------------------------------------------
#-----------------  Extraer Fila  ----------------
#-------------------------------------------------
# Extrae la fila indicada en "fila" de la matriz "matriz" y devuelve una lista con la misma.
# hay que pasarle cuantas columnas tiene la matriz.
def extraerfila(matriz,columnas,fila):
	aux = []
	for i in range(0,columnas):
		aux.append(matriz[fila][i])
	return aux

#-------------------------------------------------
#----------------  Clase Matriz  -----------------
#-------------------------------------------------

class matriz():
	def __init__(self,modo):
		# - modo = 0: Carga manual.     -- Se indican manualmente las filas y las columnas.
		# - modo = 1: Carga automatica. -- en la variable modo se envia una tupla [x,y] con las filas y las columnas.	
		self .matriz = []
		os.system("clear")
		if (modo == 0):
			print "Crear Matriz: \n"
			print "Filas: "
			self.filas = convertir('int')
			print "Columnas: "
			self.columnas = convertir('int')
		else:
			self.filas = modo[0]
			self.columnas = modo[1]
		self.matriz = crearmatriz(self.filas,self.columnas)
						

	def visualizar(self,modo,tipo):
		# - modo = 0: muestra la matriz entera.
		# - modo = [a,b]: muestra la matriz para que sea cargada, con el "_" en el campo a cargar.

		# - tipo:
		# --- mostrar los datos como el tipo que se indica.

		for i in range(0,self.filas):
			for j in range(0,self.columnas):
				if (modo != 0):
					if (i == modo[0] and j == modo[1]):
						print "_" ,
					else:
						mostrarcomo(self.matriz[i][j],tipo)
				else:
					mostrarcomo(self.matriz[i][j],tipo)	
			print ""
	
	def cargar(self,modo):
		# -- modo = 0:
		# --- con esta funcion se carga la matriz, se recorre toda la matriz y para la poss actual se envia
		#     una tupla [i,j] que le indica la poss a la funcion visualizar.

		# -- modo = 1:
		# --- Crea una matriz identidad.

		if (modo == 0):
			os.system("clear")
			print "Cargar Matriz: \n"
			for i in range(0,self.filas):
				for j in range(0,self.columnas):
					self.visualizar([i,j],'int')
					valor = convertir('complex')
					self.matriz[i][j] = valor
					os.system("clear")

		if (modo == 1):
			for i in range(0,self.filas):
				for j in range(0,self.columnas):
					if (i == j):	
						self.matriz[i][j] = 1

		self.visualizar(0,'int')

	def modificar(self):
		# modifica un valor en la matriz.
		err = 1
		os.system("clear")
		print "Modificar Matriz: \n"
		self.visualizar(0,'int')
		print "\nFila:"
		while (err == 1):
			err = 0
			fila = convertir('int')
			if (fila > (self.filas)):
				err = 1
		err = 1
		print "Columna:"
		while (err == 1):
			err = 0
			columna = convertir('int')
			if (columna > (self.columnas)):
				err = 1
		print "Valor:"
		self.matriz[fila-1][columna-1] = convertir('complex')
		self.visualizar(0,'int')
		
	def resolver(self): 
		self.ordenar()
		x = 0	
		# con este for se carga el array factores, que guarda los indices que estan bajo de la diagonal.
		#para la columna 0 guarda las X:
		# X 0 0 --
        # X 0 0 --
		# X 0 0 --
 		#para la columna 1 guarda las X:
		# 0 0 0 --
        # 0 X 0 --
		# 0 X 0 --
		# y asi siguiendo hasta la anteultima columna.

		for i in range(0,self.filas-1):
			factores = []
			for k in range(x,self.filas):
				factores.append(self.matriz[k][0+i])
		
		# este otro For recorre la matriz desde la fila 1 hasta el final,
		# multiplica la fila de indice j por el factor de la fila de arriba.
		# luego se guarda la fila de arriba y la multiplica por el factor de la fila de abajo
		# por ultimo guarda en la fila de abajo la resta de los 2.
 
			for j in range(x+1,self.filas):				
				self.matriz = multiplicarmatriz(self.matriz,j,factores[i-x],self.columnas)					
				fila = extraerfila(self.matriz,self.columnas,i)
				fila = multiplicarfila(fila,factores[j-i])
				self.matriz = restarfila(self.matriz,fila,j)
				print "--------"
				self.visualizar(0,'int')
			self.ordenar()				
			x += 1

		print "Resultado: "	
		self.visualizar(0,'int')	
			
	def ceros(self,lista):
		for i in range(0,self.filas):
			lista.append(0)
			for j in range(0,self.columnas):
				if(self.matriz[i][j] == 0):	
					lista[i] += 1		
		return lista

	def ordenar(self):
		# auxiliar: lista que contiene la cantidad de 0 por fila, tiene tantos items como filas en la matriz.
		# aux: variable para el burbujeo de la variable axuiliar nombrada arriba.
		# aux2: variable para el burbujeo de la matriz.
		# aux3: la otra variable necesaria para el burbujeo de la matriz.
		# aux4: flag para detectar si la matriz esta ordenada.
		auxiliar = []
		aux = 0
		aux2 = []
		aux3 = []
		aux4 = 0
		
		# cargo la varialbe Axuiliar con los 0 que hay por fila de la matriz.
		auxiliar = self.ceros(auxiliar)
		
		# ordeno la variable Auxiliar y la matriz.
		for k in range(0,len(auxiliar)):
			aux4 = 0
			for l in range(0,len(auxiliar)-1):		
				if(auxiliar[l] > auxiliar[l+1]):
					aux4 = 1
					# burbujeo de la variable Auxiliar
					aux = auxiliar[l]
					auxiliar[l] = auxiliar[l+1]
					auxiliar[l+1] = aux
					# burbujeo de la matriz
					aux2 = extraerfila(self.matriz,self.columnas,l)				
					aux3 = extraerfila(self.matriz,self.columnas,l+1)
					for w in range(0,len(aux2)):
						self.matriz[l][w] = aux3[w]
						self.matriz[l+1][w] = aux2[w]
			if (aux4 == 0):
				break

	def escalar(self,valor):
		for i in range(0,self.filas):
			for j in range(0,self.columnas):	
				self.matriz[i][j] = self.matriz[i][j] * valor

#-------------------------------------------------
#--------------------  menu  ---------------------
#-------------------------------------------------
class menu():
	def __init__(self):
		self.contenedor = []
		self.mostrartipo = 'int'

	def main(self):
		salir = 0 
		while (salir == 0):
			elegido = self.pantalla('m')
			if(elegido == 1):
				self.pantalla(1)

			if(elegido == 2):
				self.pantalla(2)

			if(elegido == 3):
				self.pantalla(3)

			if(elegido == 4):
				self.pantalla(4)

			if(elegido == 5):
				self.pantalla(5)

			if(elegido == 6):
				salir = 1			
		
	def vertodo(self):
		for i in range(0,len(self.contenedor)):
			print "Matriz "+ str(i)
			self.contenedor[i].visualizar(0,self.mostrartipo)
			print ""			

	def pantalla(self,opt):					
		os.system("clear")
		print "-------------------------------------------------"
		print "---------------  Matrices V2.0  -----------------"
		print "-------------------------------------------------"
		# (m) --- menu principal ---
		if (opt == "m"):
			print "- Acciones:\n"
			print "(1) ver todo"
			print "(2) Crear"
			print "(3) Modificar"
			print "(4) Borrar"
			print "(5) Operaciones"
			print "(6) Salir"
			elegido = convertir('int')
			return elegido

		# (1) --- Acciones ---
		if (opt == 1):
			print "(1)------ ver todo -------"
			self.vertodo()
			raw_input("Volver")		

		# (2) --- Crear Matriz ---
		if (opt == 2):
			print "(2)------ Crear Matriz -------"	
			print "- opciones:\n"
			print "(1) matriz vacia"
			print "(2) Matriz identidad"	
			print "(3) Volver"		
			elegido = convertir('int')
			if (elegido == 1):
				matrizaux = matriz(0)
				matrizaux.cargar(0)		
				self.contenedor.append(matrizaux)
				raw_input("Volver")
			if (elegido == 2):
				print "numero de filas & columnas:"
				elegido = convertir('int')
				matrizaux = matriz([elegido,elegido])
				matrizaux.cargar(1)		
				self.contenedor.append(matrizaux)
				raw_input("Volver")
			if (elegido == 3):
				pass
			

		# (3) --- Modificar Matriz ---
		if (opt == 3):
			print "(3)------ Modificar Matriz -------"		
			self.vertodo()
			if (len(self.contenedor) > 0):
				print "matriz a modificar:"
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				self.contenedor[elegido].modificar()
				raw_input("Volver")
			else:
				print "No hay ninguna matriz cargada"
				raw_input("Volver")

		# (4) --- Borrar Matriz ---
		if (opt == 4):
			print "(4)------ Borrar Matriz -------"
			if (len(self.contenedor) > 0):			
				self.vertodo()
				print "Borrar matriz: "
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				del self.contenedor[elegido]
			else:
				print "No hay ninguna matriz cargada"
			raw_input("Volver")
		# (5) --- Operaciones ---
		if (opt == 5):
			print "(5)------ Operaciones -------"
			print "- opciones:\n"
			print "(1) Reducir Matriz"
			print "(2) producto escalar"
			print "(3) producto matricial"
			print "(4) sumar matrices"
			print "(5) restar matrices"
			print "(6) Volver"
			elegido = convertir('int')
			self.vertodo()

			if(elegido == 1):
				print "seleccionar matriz:"
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				self.contenedor[elegido].resolver()
				raw_input("Volver")	

			if(elegido == 2):
				print "Multiplicar matriz:"
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				print "multiplicar por:"
				valor = convertir('complex')
				self.contenedor[elegido].escalar(valor)
				self.contenedor[elegido].visualizar(0,self.mostrartipo)
				raw_input("Volver")	

			if(elegido == 3):
				print "matriz a multiplicar: "			
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				print "\ncon: "
				matb = rango(convertir('int'),0,len(self.contenedor)-1)
				matrizaux = producto(self.contenedor[elegido],self.contenedor[matb])
				if (matrizaux != None):
					self.contenedor.append(matrizaux)
				raw_input("Volver")

			if(elegido == 4):
				print "matriz a sumar: "			
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				print "con: "
				matb = rango(convertir('int'),0,len(self.contenedor)-1)
				self.contenedor[elegido] = sumaresta(self.contenedor[elegido],self.contenedor[matb],"+")
				self.contenedor[elegido].visualizar(0,self.mostrartipo)
				raw_input("Volver")

			if(elegido == 5):
				print "matriz a restar: "			
				elegido = rango(convertir('int'),0,len(self.contenedor)-1)
				print "con: "
				matb = rango(convertir('int'),0,len(self.contenedor)-1)
				self.contenedor[elegido]= sumaresta(self.contenedor[elegido],self.contenedor[matb],"-")
				self.contenedor[elegido].visualizar(0,self.mostrartipo)
				raw_input("Volver")

			if(elegido == 6):
				pass

#-------------------------------------------------
#------------------  Acciones  -------------------
#-------------------------------------------------
menu_p = menu()
menu_p.main()

#matriz1 = matriz(0)
#matriz2 = matriz(0)
#matriz1.cargar()
#matriz2.cargar()
#matriz1.modificar()
#matriz1.resolver()
#matriz3 = producto(matriz1,matriz2)





