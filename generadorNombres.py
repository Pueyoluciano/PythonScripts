import random

vocales = set(["a","e","i","o","u"])
consonantes = set(["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"])
letras =vocales.union(consonantes)


class ListadoReglas:
	def __init__(self):
		self.letras = letras
		self.vocales = vocales
		self.consonantes = consonantes
		
	def unaVocalUnaConsonante(self,nombreParcial):
		if(nombreParcial[-1] in self.consonantes):
			return self.vocales
		else:
			return self.consonantes
			
	def soloLetrasA(self,nombreParcial):
		return set(["a"])
		
	def qSiempreConU(self,nombreParcial):
		if(nombreParcial[-1] == "q"):
			return set(["u"])
		else:
			return letras
	
	
class MotorReglas:
	def __init__(self):
		self.reglas = []

	def agregarReglas(self,*params):
		for regla in params:
			self.reglas.append(regla)

	def nuevaLetra(self,nombreParcial):
		letrasPosibles = letras
		for regla in self.reglas:
			letrasPosibles = letrasPosibles.intersection(regla(nombreParcial))
		
		if(len(letrasPosibles) == 0):
			print nombreParcial
			raise Exception("Las reglas filtran todas las letras :(")
				
		return  random.sample(letrasPosibles,1)[0]

		
def crearNombre(largo,reglas,letras):
	nombre = random.sample(letras,1)[0].upper()
	for i in range(0,largo-1):
		nombre += reglas.nuevaLetra(nombre.lower())
		
		
	return nombre

a = ListadoReglas()
m = MotorReglas()
m.agregarReglas(a.unaVocalUnaConsonante,a.qSiempreConU)