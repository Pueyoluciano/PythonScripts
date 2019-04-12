class Estadisticas():
	def __init__(self,tipo):
		if (tipo == "jugador"):
			self.vida = 20
			self.experiencia = 0
			self.nivel = 1
			self.x = 0
			self.y = 0

class Entidad():
	def __init__(self,nombre,npc,atravesable,estadisticas,aptitudes,acciones):
		self.nombre = nombre
		self.npc = npc
		self.atravesable = atravesable
		self.estadisticas = estadisticas
		self.aptitudes = aptitudes
		self.acciones = acciones		
		self.accion_pendiente = []
		self.parametros_pendiente = []

	def elegir(self,g_acciones):
		if (self.npc == 0):
			print "que haces?"
			accion = elegir_lista(self.acciones,1)
		else:
			accion = inteligencia_artificial("elegir")
		tiempo,parametros = g_acciones.contenido[accion].solicitar(self)
		self.accion_pendiente.append([tiempo,accion])
		self.parametros_pendiente.append(parametros)
		
	def ejecutar(self,g_acciones):
		flag = g_acciones.contenido[self.accion_pendiente[0][1]].ejecutar(self.parametros_pendiente[0])
		self.accion_pendiente.remove(self.accion_pendiente[0])
		self.parametros_pendiente.remove(self.parametros_pendiente[0])
		return flag

	def morir(self):
		lista_globales.pantalla.dibujar(self.estadisticas.x,self.estadisticas.y,(0,0,0))
		lista_globales.entidades.quitar(self.nombre)
		


class Objetivo():
	def __init__(self,nombre,jugador,parametros,condiciones):
		self.nombre = nombre
		self.jugador = jugador
		self.parametros = parametros
		self.condiciones = condiciones

	def acutalizar(self):
		pass		
		

	def verificar(self):
		cumplido = 1
		for i in range(0,len(self.condiciones)):
			if (self.parametros[i] != self.condiciones[i]):
				cumplido = 0
				break
		if (cumplido == 1):
			# ejecutar acciones de objetivo cumplido.
			self.cumplir()
			print "ganaste"
		else:
			print "no pasa nada"

	def cumplir(self):
		pass




pepe = Entidad("pepe",0,0,Estadisticas("jugador"),[],[])


parametros = [pepe.estadisticas.vida]

condiciones = [0]

objet = Objetivo("ganar",pepe,parametros,condiciones)
objet.verificar()

pepe.estadisticas.vida = 0

objet.verificar()

