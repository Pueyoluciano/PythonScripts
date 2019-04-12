#-------------------------------------------------
#---------------  Clase entidad  ---------------
#-------------------------------------------------
class entidad():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.vida = 0
		self.nivel = 1
		self.exp = 0
		self.nombre = ""
		self.magias = []
		self.habilidades = []
		self.inventario = []
	
	def agarrar(self):
		pass

	def objeto(self):
		pass
	
	def habilidad(self):
		pass

	def magia(self):
		pass
	
	def morir(self):	
		pass

	def atacar(self):	
		pass

	def mover(self):
		self.x,self.y = movervalidacion(self.x,self.y)

	def pasar(self):
		pass


def movervalidacion(x,y):
	#validaciones para que se pueda mover.
	return x,y
	


#-------------------------------------------------
#---------------  Clase personaje  ---------------
#-------------------------------------------------
class jugador(entidad):
	pass

#-------------------------------------------------
#------------------  Clase npc  ------------------
#-------------------------------------------------
class npc(entidad):
	pass



