class Item:
	def __init__(self,nombre,desc,impl):
		self.nombre = nombre
		self.descripcion = desc
		self.implementacion = impl

	def __str__(self):
		return str(self.nombre)
		
	def accionDiccionario(self,**params):
		return self.implementacion(params)
	
	def accionLista(self,*params):
		return self.implementacion(params)
	
	def accionParametro(self,params):
		return self.implementacion(params)

class Implementaciones:
	def __init__(self):
		self.contenido = []
		self.nombres = []
	
	def _actualizarNombres(self):
		self.nombres = [item.nombre for item in self.contenido]
	
	def agregarItem(self,nombre,desc,impl):
		self.contenido.append(Item(nombre,desc,impl))
		self._actualizarNombres()

	def obtenerID(self,nombre):
		if(nombre in self.nombres):
			return self.nombres.index(nombre)
		else:
			return -1
		
	def obtenerItem(self,nombre):
		return self.contenido[self.obtenerID(nombre)]
	
	def obtenerNombre(self,id):
		return self.nombres[id]
