	
#-------------------------------------------------
# ------------  Clase Diccionario  ---------------
#-------------------------------------------------
class Diccionario():
	def __init__(self):
		self.contenido = {}
		
	def agregar(self,key,instancia):
		self.contenido[key] = instancia

	def quitar(self,key):
		del self.contenido[key]

	def subconjunto(self,lista):
		diccio = {}
		for i in range(0,len(lista)):
			try:
				diccio[lista[i]] = self.contenido[lista[i]]

			except(KeyError):
				pass
		
		return diccio

	def mostrar(self):
		keys = self.contenido.keys()
		keys.sort()
		for i in range(0,len(keys)):
			print '- '+ str(keys[i])
		print ''

	def extraer(self,modo):
		#-- modo = 0: revuelve el valor
		# -- modo = 1: devuelve la Key
		error = 1
		while (error == 1):
			key = raw_input("> ")
			error = 0
			try:
				resultado = self.contenido[key]

			except(KeyError):
				print "El item no existe"
				error = 1
		if (modo == 0):
			return resultado

		if (modo == 1):
			return key			

	def random(self):
		listakeys = self.contenido.keys()
		key = random.sample(listakeys,1)				

		return key[0], self.contenido[key[0]]




variable valor
-------- tipo
-------- minimo
-------- maxmimo
-------- distinto de 







