class Variable:
	"""
		Clase para generar variables con varios parametros, los datos de entrada valor y modificador son obligatorios.
		el dato **parametros es un diccionario que contiene todos los parametros que son relevantes para la Variable.
		
		-valor: contiene el valor concreto. puede ser cualquier cosa.
		
		-modificador: es la funcion que modifica a Variable. Esta pensada para ser usada con la clase Aplicacion, que tiene
			un metodo modificar generico, el cual llama a este parametro.
		
		**Para cargar estos valores, hay que invocar a Variables con un parametro que se llame igual que alguno/s de esto/s: **
		
		-minimo: (opcional) puede ser que no tenga sentido, por ejemplo para un complex().
		
		-maximo: (opcional) idem minimo.
		
		-valoresPosibles: (opcional) Lista de valores posibles, util para conjuntos finitos.
		
		-flags: (opcional) diccionario con los flags que se quieran implementar.
		
		ejemplos de invocaciones:
			Variable(15,funcionN1)
			Variable(15.0,funcionN2,minimo=0)
			Variable(8,funcionN3,minimo=0,maximo=17)
			Variable("jpg",funcionN4,valoresPosibles=["jpg","bmp"],flags={"iterable":False})
		
	"""
	def __init__(self,valor, modificador, **parametros):
		self.valor = valor
		self.modificador = modificador
		self.orden = parametros["orden"] if "orden" in parametros.keys() else -1
		self.minimo = parametros["minimo"] if "minimo" in parametros.keys() else None
		self.maximo = parametros["maximo"] if "maximo" in parametros.keys() else None
		self.valoresPosibles = parametros["valoresPosibles"] if "valoresPosibles" in parametros.keys() else []
		self.flags = parametros["flags"] if "flags" in parametros.keys() else {}

	def __str__(self):
		return str(self.valor)
		
	def __repr__(self):
		return str(self.valor)
