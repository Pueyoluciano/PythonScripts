#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import matematica

#-------------------------------------------------
#------------------  Acciones  -------------------
#-------------------------------------------------

class polinomio():
	def __init__(self,grado):
		self.grado = grado
		self.coeficientes = []
		for i in range(0,grado+1):
			print "coeficiente para X^"+str (i) 
			self.coeficientes.append(matematica.convertir("int"))	
	
	def mostrar(self,modo):
		# Modo 0: oculta los terminos con coeficiente = 0
		# modo 1: complementario :D a modo 0.
		for i in range(self.grado,-1,-1):
			if (self.coeficientes[i] != 0 or modo == 1):
				if (i == 0):
					print str(self.coeficientes[i]) ,
				else:
					print str(self.coeficientes[i])+ "X^" + str(i),
					if((self.grado-i) <= self.grado+1):
						print "+",		

	def evaluar(self):
		print "evaluar polinomio en:"
		aux = matematica.convertir("complex")
		valor  = self.coeficientes[0] + aux
		for i in range(1,self.grado):
			valor += (self.coeficientes[i]*(aux**i))	
		return valor		

print "polinomio de grado: " 
poli = polinomio(matematica.convertir("int"))
poli.mostrar(0)

a = poli.evaluar()

print a




