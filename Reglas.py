import random
from Letras import Letras
import Implementador

class Filtros:		
	@staticmethod
	def unaConsonanteUnaVocal(nombreParcial):
		if(nombreParcial[-1] in Letras.consonantes):
			return Letras.vocales
		else:
			return Letras.consonantes
	
	@staticmethod
	def unaConsontanteHastaDosVocales(nombreParcial):
		if(nombreParcial[-1] in Letras.consonantes):
			return Letras.vocales
			
		else:		
			if(len(nombreParcial) >=2):
				if(nombreParcial[-2] in Letras.vocales and nombreParcial[-1] in Letras.vocales):
					return Letras.consonantes
			
		return Letras.letras
	
	@staticmethod
	def soloLetrasAUnaVocal(nombreParcial):
		letrasParcial = Filtros.unaConsonanteUnaVocal(nombreParcial)
		filtro = Letras.letras.copy()
		filtro.remove("a")
		return letrasParcial.intersection(filtro)
	
	@staticmethod
	def soloLetrasADosVocales(nombreParcial):
		letrasParcial = Filtros.unaConsontanteHastaDosVocales(nombreParcial)
		filtro = Letras.letras.copy()
		filtro.remove("a")
		return letrasParcial.intersection(filtro)
	
	@staticmethod	
	def qSiempreConU(nombreParcial):
		if(nombreParcial[-1] == "q"):
			return set(["u"])
		else:
			return Letras.letras		
	
	@staticmethod
	def quSiempreConEI(nombreParcial):
		if(len(nombreParcial) >= 2):
			if(nombreParcial[-2]+nombreParcial[-1] == "qu"):
				return set(["e","i"])

		return Letras.letras


class ListadoReglas:
	contenido = Implementador.Implementaciones()
	contenido.agregarItem("unaConsonanteUnaVocal","Permite solo una vocal seguida de una consonante, y viceversa",Filtros.unaConsonanteUnaVocal)
	contenido.agregarItem("unaConsontanteHastaDosVocales","Permite una consonante seguida de Hasta dos vocales",Filtros.unaConsontanteHastaDosVocales)
	contenido.agregarItem("qSiempreConU","Siempre que aparece una Q la sigue una U",Filtros.qSiempreConU)
	contenido.agregarItem("quSiempreConEI","Si aparece QU le sigue una E o una I",Filtros.quSiempreConEI)	
	contenido.agregarItem("soloLetrasAUnaVocal","unaConsonanteUnaVocal + vocales unicamente A",Filtros.soloLetrasAUnaVocal)
	contenido.agregarItem("soloLetrasADosVocales","unaConsonanteHastaDosVocales + vocales unicamente A",Filtros.soloLetrasADosVocales)

	
class MotorReglas:
	def __init__(self):
		self.reglas = []

	def agregarReglas(self,params):
		for regla in params:
			self.reglas.append(regla)

	def limpiarReglas(self):
		self.reglas = []
			
	def nuevaLetra(self,nombreParcial):
		letrasPosibles = Letras.letras
		for regla in self.reglas:
			letrasPosibles = letrasPosibles.intersection(regla.accionParametro(nombreParcial))
		
		if(len(letrasPosibles) == 0):
			print nombreParcial
			raise Exception("Las reglas filtran todas las letras :(")
				
		return  random.sample(letrasPosibles,1)[0]
