#------------------------------------------------------------------------------------------------------
#-------------------------------------------- Matematica ----------------------------------------------
#------------------------------------------------------------------------------------------------------
# Recopilacion de Funciones matematicas.
# Glorario:
#
# -- Generales:
# ---- factorial(numero)
# ---- combinatoria(n,k)
# ---- divent(a,b)
# ---- convertir(entrada)
# ---- sqrt(raiz)
# ---- phie(n) -- (Funcion Fi de Euler)
# ---- modulo(numero)


# -- Mcd && Mcm:
# ---- mcm(a,b)
# ---- mcd(a,b)

# -- Factorizacion:
# ---- factorizar(numero)
# ---- iterar(numero)
# ---- primos(diccionario,item)
# ---- traducir(diccionario)


#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os
import time
import math

#--------------------------------------------------------------------------------------------------
#-------- Generales -------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#-------------------------------------------------
# -----------------  Factorial  ------------------
#-------------------------------------------------
def factorial(numero):
	numero = long (numero)
	out = 1
	for i in range(numero,1,-1):
		out = out * i
	return out

#-------------------------------------------------
# -----------  Numero Combinatorio  --------------
#-------------------------------------------------
def combinatoria(n,k):
	n = long(n)
	k = long(k)
	if (n < k):
		aux = k
		k = n
		n = aux
	comb = factorial(n)/(factorial(k)*factorial(n-k))
	return comb

#-------------------------------------------------
# -------------  Resto modulo M  -----------------
#-------------------------------------------------
def resto(numero,modulo):
	for i in range(numero,-1,-modulo):
		pass
	return i


#-------------------------------------------------
#---------------  Division entera  ---------------
#-------------------------------------------------
# hace la division entera de a dividido b y devuelve el resultado y el resto.
def divent(a,b):
	if (a>0 and b>0):
		devol = 1
	if (a>0 and b<0):
		devol = 2
	if (a<0 and b>0):	
		devol = 3
	if (a<0 and b<0):
		devol = 4

	conta = 0
	resto = a
 	while (resto >= abs(b)):
		conta += 1		
		resto -= abs(b)
	if (devol == 1):
		return conta,resto
	if (devol == 2):
		return (-1)*conta,resto
	if (devol == 3):
		if (resto == 0):
			return (-1)*conta,0
		else:
			return (-1)*conta-1, abs(b)-resto
	if (devol == 4):
		if (resto == 0):
			return conta,0
		else:
			return conta+1, abs(b)-resto

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

			if(entrada == 'long'):
				valor = long(raw_input("> "))
				
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
# ----------------  Convertir2  ------------------
#-------------------------------------------------
# Convierte el dato que recibe con el raw_iput al tipo que se indica en entrada.
# solo sirve para numeros reales, y permite comparar el valor ingresado con un minimo y maximo.
# Si el valor minimo y el maximo son iguales (y no son NONE) entonces compara el valor con el minimo(que es igual al maximo) y verifica si son iguales.
# Comparacion es el operador logico aplicado al valor minimo y al maximo, cuando estos son iguales,
# es decir cuando quiere comprararse el dato de entrada a un valor puntual:
# --- igual, distinto, mayor, menor, mayorigual, menorigual.
# Si el Minimo o el maximo es una lista, se fija si el valor ingresado se encuentra dentro de la misma.

def convertir2(entrada,minimo,maximo,comparacion):
	err = 1
	while (err == 1):
		err = 0
		try:
			if(entrada == 'int'):
				valor = int(raw_input("> "))

			if(entrada == 'long'):
				valor = long(raw_input("> "))
				
			if(entrada == 'float'):
				valor = float(raw_input("> "))

			if ((minimo == maximo) and (minimo != None)):
				if (comparacion == 'igual'):
					if (valor != minimo):
						err = 1
						continue				

				if (comparacion == 'distinto'):
					if (valor == minimo):
						err = 1
						continue

				if (comparacion == 'mayor'):
					if (valor <= minimo):
						err = 1
						continue

				if (comparacion == 'menor'):
					if (valor >= minimo):
						err = 1
						continue

				if (comparacion == 'mayorigual'):
					if (valor < minimo):
						err = 1
						continue		
		
				if (comparacion == 'menorigual'):
					if (valor > minimo):
						err = 1
						continue

			else:
				if ((type(minimo) == type(list())) or (type(maximo) == type(list()))):
					if (minimo.count(valor) == 0):	
						err = 1
						continue
				else:
					if (minimo != None):
						if (valor < minimo):
							err = 1
							continue

					if (maximo != None):
						if (valor > maximo):
							err = 1
							continue

		except(ValueError):
			err = 1
	return valor

#-------------------------------------------------
# --------  Raiz Cuadrada(Por geometria) ---------
#-------------------------------------------------
#Nada, eso.
def sqrt(raiz):
	if (raiz < 0):	
		print "el numero es menor a 0"
	else:
		if (raiz == 0):
			return raiz
		else:
			area = raiz
			b = area
			h = 1
			for i in range(0,10):
				b = 0.5*(b+ area/b)
	return b

#-------------------------------------------------
# ------------  Funcion Fi de Euler  -------------
#-------------------------------------------------
# La funcion calcula la cantidad de numeros enteros positivos < a 'n'
# que son coprimos con n.
#Recibe un parametro n, lo factoriza, y aplica la propiedad de Phi(n) 
# descrita abajo.
def phie(n):
	resultado = 1
	tupla,tiempo = factorizar(n,0)
	factorizado = tupla.items()
	for base,exponente in factorizado:
		# Propiedad de Phi(n): Phi(p**k) = (p-1)*(p**(k-1))
		resultado *= (base-1)*(base**(exponente-1)) 	
	return resultado

#-------------------------------------------------
# -------------------  Modulo  -------------------
#-------------------------------------------------
#Distancia euclidea del punto al origen, norma 2, o modulo de un numero complejo.
#Como mas te guste ;).
def modulo(numero):
	# Compara el Type de numero con el de un complejo y una lista.
	# Si es un Complejo extrae parte real e imaginaria.
	# Si es una lista extrae todos los items de la misma, los eleva al cuadrado,
	# los suma y saca raiz.
	if (type(numero) == type(1+1j)):
		complejo = 1
		resultado = sqrt(numero.real**2 + numero.imag**2)
	else:
		if (type((numero) == type([]))):
			complejo = 0
			resultado = 0
			for i in range(0,len(numero)):
				resultado += (numero[i]**2)
			resultado = sqrt(resultado) 
		else:
			return -1	

	return resultado

#--------------------------------------------------------------------------------------------------
#-- Maximo Comun Divisor &&  Minimo Comun Multiplo  -----------------------------------------------
#--------------------------------------------------------------------------------------------------

#-------------------------------------------------
#----------  Minimo Comun Multiplo  --------------
#-------------------------------------------------
# Devuelve el MCM entre dos numeros.
def mcm(a,b):
	resultado = (a*b)/(mcd(a,b))
	return resultado

#-------------------------------------------------
#------------  Maximo Comun Divisor  -------------
#-------------------------------------------------
def mcd(a,b):
	if (a == 0 or b == 0):
		return max(a,b)
	else:
		if (b > a):
			c = b
			b = a
			a = c
	
		maximo = int(math.ceil(a/2))
		for i in range(maximo,0,-1):
			if(a%i == 0 and b%i == 0):
				break

		return i

#-------------------------------------------------
#-----------  Maximo Comun Divisor2  -------------
#-------------------------------------------------
# Calcula la factorizacion del numero mas chico,
# y se fija que factores(y sus potencias) dividen al mas grande.
def mcd2(a,b):
	if(a != 0 and b != 0):
		# si son negativos los invierto.
		if (a<0):
			a *= -1
		if (b<0):
			a*= -1
		# me quedo con el numero mas chico.
		if(a>b):
			numeroa = b
			numerob = a
		else:
			numeroa = a
			numerob = b
		diccio2 = {}
		#factorizo el numero mas chico
		diccio,tiempo = factorizar(numeroa,0)
		# recorro la factorizacion de arriba y me fijo cuales dividen al mas grande.
		# y lo guardo en diccio2
		for primo,potencia in diccio.iteritems():
			for i in range(0,potencia):
				if(numerob % primo == 0):
					diccio2 = primos(diccio2,primo)
					numerob = numerob/primo

		return traducir(diccio2)
	else:
		return(max(a,b))



#--------------------------------------------------------------------------------------------------
#-- Factorizacion ---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#-------------------------------------------------
# ------------------  FACTOREO  ------------------
#-------------------------------------------------
#Metodo poco eficiente para calcular los factores primos de un numero.
# (0): prueba con un divisor >=2 sumando de a 1 hasta que el numero sea divisble por este.
# (1): divisor solo toma valores menores o iguales a sqrt(numero). (Teorema)
# (2): NO divido por ningun numero par > 2

# numero: numero a factorizar.
# modo == 1: muestra como se factoriza el numero.
# modo == cualquier otra cosa: no muestra nada.
def factorizar(numero,modo):
	numero = int(numero)
	divisor = 2
	diccio = {}
	raiz =  math.floor(math.sqrt(numero))
	if (modo == 1):
		print numero
	tiempo = time.time()
	while (numero != 1):
		# (1)
		if(divisor > raiz):
			diccio = primos(diccio,numero)
			numero = 1
		else:
			#print "raiz:" +str(sqrt(numero))
			#print "divisor: "+ str(divisor)
			#(0)
			if (numero % divisor == 0):
				numero = numero/divisor
				diccio = primos(diccio,divisor)
				raiz =  math.floor(math.sqrt(numero))
				divisor = 2
				if (modo == 1):
					print numero
			else:
				#(2)
				divisor = iterar(divisor)

	tiempototal = (time.time()-tiempo) 
	return diccio,tiempototal

#-------------------------------------------------
# -------------------  ITERAR  -------------------
#-------------------------------------------------
# Funcion para iterar el divisor en factorizar()
def iterar(numero):
	#numero += 1
	if(numero == 2):
		numero += 1
	else:				
		numero += 2
		if(numero %3 == 0 and numero > 3):
			numero += 2
		if(numero% 5 == 0 and numero >5):
			numero += 2
			if(numero %3 == 0):
				numero += 2
	return numero

#-------------------------------------------------
# --------------  FACTORES PRIMOS  ---------------
#-------------------------------------------------
# recibe un diccionario y un valor, si ya existe el indice le suma 1
# caso contrario crea un nuevo indice y le asigna un valor = 1.
def primos(diccionario,item):
	if (item in diccionario):
		diccionario[item] += 1
	else:
		diccionario[item] = 1
	return diccionario

#------------------------------------------------
#------------  Calcular diccionario  ------------
#------------------------------------------------
# calcula el numero que es resultado de las potencias de primos ingresada como diccionario.
def traducir(diccionario):
	numero = 1
	for primo,potencia in diccionario.iteritems():
		numero *= primo**potencia
	return numero

