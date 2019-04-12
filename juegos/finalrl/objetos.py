#-------------------------------------------------
# ----------------  Clase Objeto  ----------------
#-------------------------------------------------
# tipos:
# ---------
# 0X una mano
# ---------
# 00 espadas
# 01 mazas
# 02 hachas
# 03 ...
# -------------
# 1X dos manos
# ---------
# 10 espadas 
# 11 mazas
# 12 hachas
# 13 ...

class armas():
	def __init__(self):
		self.lista_armas = {}
	
	def agregar(self,item):
		self.lista_armas[item.nombre] = item
			

class arma():
	def __init__(self,nombre,tipo,dano_base,peso,velocidad):
		self.nombre = nombre
		self.tipo = tipo
		self.dano_base = dano_base
		self.peso = peso
		self.velocidad = velocidad
	

listado_armas = armas()

arma1 = arma("espada corta",1,3,5,1)
listado_armas.agregar(arma1)


print listado_armas.lista_armas


