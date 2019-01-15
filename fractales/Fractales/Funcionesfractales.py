# Clase Funcion:
# esta clase es la que generaliza las funciones que ejecuta Fractales.py
# el parametro "parametros" es una lista (en orden) con los paramteros requeridos por la funcion concreta.
# la accion es la funcion concreta.
# para usar la funcion, hay que hacer la invocacion con un primer parametro obligatorio c, que es el punto en el plano complejo(que puede ser utilizado o no)
# y a continuacion todos los parametros que la funcion espera recibir, en el orden en el que fueron declarados a la hora de instanciar la clase.

class Funcion():
	listado = {}
	
	def __init__(self,nombre,parametros,accion):
		self.parametros = parametros
		self.nombre = nombre
		self.accion = accion
	
	def __str__(self):
		return str(self.nombre)
	
	def parametros(self):
		return self.parametros
		
	def calcular(self,c,params):
		return self.accion(c,params)
		
#-------------------------------------------------
# ---------------  Mandelbrot  -------------------
#-------------------------------------------------
# Funcion para el Conjunto de mandelbrot.
# c es un numero complejo (a+bi).
# si despues del numero de iteraciones indicado, el |z| no es >= 2,
# entonces se entiende que z pertenece a M(conjunto de Mandelbrot).
# OBS:
# esta funcion recibe un parametro "d"pero no lo usa, esta simplemente
# para unificar las llamadas de las funciones mandelbrot y julia.

def mandelbrot(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**2)) + c )
	return i
	
#-------------------------------------------------
# ---------------  MandelbrotX  ------------------
#-------------------------------------------------
def mandelbrotx(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	exp = params[2]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**exp)) + c )
	return i

#-------------------------------------------------
# -------------------  MaX  ----------------------
#-------------------------------------------------
def maX(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	exp = params[2]
	d = params[3]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**exp)) + (c**2-(d)) )
	return i

#-------------------------------------------------
# ------------------  Julia  ---------------------
#-------------------------------------------------
# Funcion para Conjuntos de Julia, muy similar a Mandelbrot 
# pero toma un complejo "d" como parametro extra.
def julia(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**2)) + d )
	return i

#-------------------------------------------------
# ------------------  JuliaX  --------------------
#-------------------------------------------------
# Funcion para Conjuntos de Julia, muy similar a Mandelbrot 
# pero toma un complejo "d" como parametro extra.
def juliax(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	exp = params[2]
	d = params[3]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**exp)) + d )
	return i

#-------------------------------------------------
# -------------------  asd  ---------------------
#-------------------------------------------------
def asd(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			zsig = (((z**2)) + c  - ((c+d)/2))
			z = zsig
	return i

#-------------------------------------------------
# -------------------  asd2  ---------------------
#-------------------------------------------------
def asd2(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			try:
				zsig = ((z**2) + d)/((z**3)+ d)
				z = zsig
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  asd3  ---------------------
#-------------------------------------------------
def asd3(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			zsig = ((z**5) + d)/((z**4) + d)
			z = zsig
	return i

#-------------------------------------------------
# -------------------  asd4  ---------------------
#-------------------------------------------------
def asd4(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			try:
				zsig = ((z**2) + d)/((z**6) + d)
				z = zsig
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  asd5  ---------------------
#-------------------------------------------------
def asd5(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]	
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			try:
				zsig = ((z**2)+d)/((z**3))
				z = zsig
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  asd6  ---------------------
#-------------------------------------------------
def asd6(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]	

	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			try:
				z = (z+c**3)/(z**4-c+d)+(d**3)
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  qwe  ----------------------
#-------------------------------------------------
def qwe(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]	
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:			
			try:
				z = ((z**6) + d)/((z**2) + d)
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  qwe2  ---------------------
#-------------------------------------------------
def qwe2(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:		
			try:
				z = (z+d)/(z-d)
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  qwe3  ---------------------
#-------------------------------------------------
def qwe3(c,prams):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:		
			try:
				z = ((z**6) + d)/((z**3) + d)
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  qwe4  ---------------------
#-------------------------------------------------
def qwe4(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]	
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:		
			try:
				z = ((z**6) + d)/((z**1) + d)
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  qwe5  ---------------------
#-------------------------------------------------
def qwe5(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]	
	zsig = 0
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:		
			try:
				z = z/(d+z)
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

#-------------------------------------------------
# -------------------  qwe6  ---------------------
#-------------------------------------------------
def qwe6(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:			
			try:
				z = (((z**2)) + c ) / (((z**2)) + d ) 
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue		
	return i

#-------------------------------------------------
# --------------------  zxc  ---------------------
#-------------------------------------------------
# Funcion para Conjuntos de Julia, muy similar a Mandelbrot 
# pero toma un complejo "d" como parametro extra.
def zxc(c,params):
	z = c
	diteraciones = params[0]
	norma = params[1]
	d = params[2]
	
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			try:
				z = (z**z)-(z**d)
				
			except(ZeroDivisionError):
				print "DIVISION POR 0"
				continue
	return i

Funcion.listado["mandelbrot"] = Funcion("mandelbrot",["resolucion","norma"],mandelbrot)
Funcion.listado["mandelbrotx"] = Funcion("mandelbrotx",["resolucion","norma","exponente"],mandelbrotx)
Funcion.listado["max"] = Funcion("max",["resolucion","norma","exponente","parametro"],maX)
Funcion.listado["julia"] = Funcion("julia",["resolucion","norma","parametro"],julia)
Funcion.listado["juliax"] = Funcion("juliax",["resolucion","norma","exponente","parametro"],juliax)
Funcion.listado["asd"] = Funcion("asd",["resolucion","norma","parametro"],asd)
Funcion.listado["asd2"] = Funcion("asd2",["resolucion","norma","parametro"],asd2)
Funcion.listado["asd3"] = Funcion("asd3",["resolucion","norma","parametro"],asd3)
Funcion.listado["asd4"] = Funcion("asd4",["resolucion","norma","parametro"],asd4)
Funcion.listado["asd5"] = Funcion("asd5",["resolucion","norma","parametro"],asd5)
Funcion.listado["asd6"] = Funcion("asd6",["resolucion","norma","parametro"],asd6)
Funcion.listado["qwe"] = Funcion("qwe",["resolucion","norma","parametro"],qwe)
Funcion.listado["qwe2"] = Funcion("qwe2",["resolucion","norma","parametro"],qwe2)
Funcion.listado["qwe3"] = Funcion("qwe3",["resolucion","norma","parametro"],qwe3)
Funcion.listado["qwe4"] = Funcion("qwe4",["resolucion","norma","parametro"],qwe4)
Funcion.listado["qwe5"] = Funcion("qwe5",["resolucion","norma","parametro"],qwe5)
Funcion.listado["qwe6"] = Funcion("qwe6",["resolucion","norma","parametro"],qwe6)
Funcion.listado["zxc"] = Funcion("zxc",["resolucion","norma","parametro"],zxc)