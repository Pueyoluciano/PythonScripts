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
def mandelbrot(c,d,diteraciones,norma,exp):
	z = c
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**2)) + c )
	return i
#-------------------------------------------------
# ---------------  MandelbrotX  ------------------
#-------------------------------------------------
def mandelbrotx(c,d,diteraciones,norma,exp):
	z = c
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**exp)) + c )
	return i

#-------------------------------------------------
# -------------------  MaX  ----------------------
#-------------------------------------------------
def maX(c,d,diteraciones,norma,exp):
	z = c
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
def julia(c,d,diteraciones,norma,exp):
	z = c
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
def juliax(c,d,diteraciones,norma,exp):
	z = c
	for i in range(1,diteraciones+1):
		if (abs(z) >= norma):
			return i
		else:
			z = (((z**exp)) + d )
	return i

#-------------------------------------------------
# -------------------  asd  ---------------------
#-------------------------------------------------
def asd(c,d,diteraciones,norma,exp):
	z = c
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
def asd2(c,d,diteraciones,norma,exp):
	z = c
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
def asd3(c,d,diteraciones,norma,exp):
	z = c
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
def asd4(c,d,diteraciones,norma,exp):
	z = c
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
def asd5(c,d,diteraciones,norma,exp):
	z = c
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
def asd6(c,d,diteraciones,norma,exp):
	z = c
	zsig = 0
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
def qwe(c,d,diteraciones,norma,exp):
	z = c
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
def qwe2(c,d,diteraciones,norma,exp):
	z = c
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
def qwe3(c,d,diteraciones,norma,exp):
	z = c
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
def qwe4(c,d,diteraciones,norma,exp):
	z = c
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
def qwe5(c,d,diteraciones,norma,exp):
	z = c
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
def qwe6(c,d,diteraciones,norma,exp):
	z = c
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
def zxc(c,d,diteraciones,norma,exp):
	z = c
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

