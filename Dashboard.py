import pygame

class Prioridades:
	lista = ["Baja","Media","Alta"]
	
	
class Estados:
	lista = ["Pausado","En proceso","Terminado","Cancelado"]

	
class Controlador:	
	def __init__(self):
		self.dashboards = []

	def agregarDashboard(self,*dashboards):
		for dashboard in dashboards:
			self.dashboards.append(dashboard)

	
class Dashboard:
	def __init__(self,nombre,desc,categorias):
		self.nombre = nombre
		self.descripcion = desc
		self.categorias = categorias
		self.tareas = []
	
	def agregarTareas(self,*tareas):
		for tarea in tareas:
			self.tareas.append(tarea)

def generico(self):
	pass

class Graficable:		
	ancho = 0
	alto = 0
	eje = [0,0]
	color = [0,0,0]
	presionado = False
	seleccionado = False
	presionadoEn = [-1,-1]
	mouseSobre = False
	
	accSobreSi = generico
	accSobreNo = generico
	accClick = generico
	accLiberar = generico
	
	def sobreSi(self):
		# print "estas sobre mi" + str(self.eje)
		self.accSobreSi()
	
	def sobreNo(self):
		# print "ya no estas sobre mi" + str(self.eje)
		self.accSobreNo()
	def click(self):
		# print "me clickeaste" + str(self.eje)
		if(not self.seleccionado):
			self.seleccionado = True
			
		self.accClick()
	
	def liberar(self):
		# print "me soltaste" + str(self.eje)
		self.presionadoEn = [-1,-1]
		self.accLiberar()
		
	def arrastrar(self):
		if(self.presionadoEn[0] == -1):
			self.presionadoEn = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
			
		x = pygame.mouse.get_pos()[0] - self.presionadoEn[0]
		y = pygame.mouse.get_pos()[1] - self.presionadoEn[1]
		self.eje = [x, y]
	
class Tarea(Graficable):
	def __init__(self,nombre,desc,prioridad,estado,ancho,alto,eje,color):
		self.nombre = nombre
		self.descripcion = desc
		self.prioridad = prioridad
		self.estado = estado
		self.items = []
		
		self.ancho = ancho 
		self.alto = alto
		self.eje = eje
		self.color = color
		
	def agregarItem(self,*items):
		for item in items:
			self.items.append(item)

	def getCuadrado(self):
		#return [x0,y0,xf,yf]
		return [self.eje[0],self.eje[1],self.eje[0] + self.ancho, self.eje[1] + self.alto]  
		
class Item:
	def __init__(self,estado,descripcion):
		self.estado = estado
		self.descripcion = descripcion
	
	
class Interfaz:
	def __init__(self):
		self.tile = 10
		self.ancho = 250
		self.alto = 100
		self.titulo = "Dasboard v1.0"
		self.fps = 5
		self.colorfondo = [0,0,0]
		self.tareaSeleccionada = None
		
		
		pygame.init()
		self.screen = pygame.display.set_mode((self.ancho,self.alto))
		pygame.display.set_caption(self.titulo)
		self.clock = pygame.time.Clock()
		
		self.dashSeleccionado = 0
		self.controlador = Controlador()
		
	def loop(self):
		salir = False
		seleccione = False
		solte = False
		
		while not salir:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					salir = True
					
			if(not salir):
				# Recorro todas las tareas para ver que pasa
				for tarea in self.controlador.dashboards[self.dashSeleccionado].tareas:	
					#Me fijo si el mouse toca la tarea
					if(self.hitTest(pygame.mouse.get_pos(),tarea.getCuadrado())):
						tarea.mouseSobre = True
						
						#Si hice click
						if(pygame.mouse.get_pressed()[0]):
							tarea.presionado = True
							
							#esto es para dejar seleccionada una tarea
							if(not seleccione and not solte):
								self.tareaSeleccionada = tarea
								seleccione = True
								solte = False
								
							else:
								if(seleccione and solte):
									self.tareaSeleccionada = tarea
									seleccione = True
									solte = False
									
						else:
							tarea.presionado = False
							if(seleccione and not solte):
								solte = True
							
					else:
						tarea.mouseSobre = False
			
					if(tarea.mouseSobre):
						tarea.accSobreSi()
						
					if(not tarea.mouseSobre):
						tarea.accSobreNo()

					if(tarea.presionado):
						tarea.accClick()
						
					if(not tarea.presionado):
						tarea.accLiberar()

				#Limpiar la Pantalla
				self.screen.fill(self.colorfondo)					
				
				#Redibujar las tareas
				for tarea in self.controlador.dashboards[self.dashSeleccionado].tareas:
					self.dibujarTarea(tarea)
								
				pygame.display.flip()
					
				self.tick = self.clock.tick(self.fps)		
		
	def dibujarTarea(self,tarea):
		#dibujar Rectangulo con el tamano de tarea
		# escribir los textos
		pygame.draw.rect(self.screen,tarea.color,[tarea.eje[0], tarea.eje[1], tarea.ancho, tarea.alto],0)
	
	def hitTest(self,a,b):
		#punto y punto
		if(len(a) == 2 and len(b) == 2):
			if(a == b):
				return 1
		
		#punto y cuadrado		
		if(len(a) == 2 and len(b) == 4):
			if(a[0] >= b[0] and a[0] <= b[2] and a[1] >= b[1] and a[1] <= b[3]):
				return 1
		
		#cuadrado y punto
		if(len(a) == 4 and len(b) == 2):
			if(b[0] >= a[0] and b[0] <= a[2] and b[1] >= a[1] and b[1] <= a[3]):
				return 1
				
		#cuadrado y cuadrado
		if(len(a) == 4 and len(b) == 4):
			# este if es equivalente a preguntar si las lineas No estan Disjuntas.
			if not((a[0]<b[0] and a[2]< b[0]) or (b[0]<a[0] and b[2]< a[0])):
				return 1
				
		return 0
		
if __name__ == '__main__':	
	int = Interfaz()
		
	tarea1 = Tarea("tarea1","desc1_tarea",Prioridades.lista[2],Estados.lista[1],20,20,[0,0],[20,20,20])
	tarea2 = Tarea("Tarea2","asd2",Prioridades.lista[1],Estados.lista[1],20,20,[30,30],[20,20,20])

	tarea1.accClick = tarea1.arrastrar
	tarea2.accClick = tarea2.arrastrar
	
	int.controlador.agregarDashboard(Dashboard("DashboardDePruebas","descripcion",Estados.lista))
	int.controlador.dashboards[0].agregarTareas(tarea1,tarea2)
	
	int.loop()
	pygame.quit()	
		
			
				# for tarea in self.controlador.dashboards[self.dashSeleccionado].tareas:
					# #Mouse Sobre
					# if(self.hitTest(pygame.mouse.get_pos(),tarea.getCuadrado()) and not tarea.mouseSobre):
						# tarea.sobreSi()
					
					# #Mouse Fuera
					# if(not self.hitTest(pygame.mouse.get_pos(),tarea.getCuadrado()) and tarea.mouseSobre):
						# tarea.sobreNo()
					
					# #Mouse Click
					# if(self.hitTest(pygame.mouse.get_pos(),tarea.getCuadrado()) and pygame.mouse.get_pressed()[0] and not tarea.presionado):
						# print "CLICK"
						# tarea.presionadoEn = pygame.mouse.get_pos()
						# tarea.click()
					
					# #Mouse Release
					# if(not pygame.mouse.get_pressed()[0] and tarea.presionado):
						# tarea.liberar()		
# eventos:
# clickon clickoff sobreon sobreoff		

# tareas:
# 1, 2


		
# for tarea in tareas:
	# if(hittest(mouse,tarea)):
		# tarea.sobre = True
		
		# if(mouse.getpressed()):
			# tarea.click = True
		# else:
			# tarea.click = False
			
	# else:
		# tarea.sobre = False
	
	# if clickon:
		# tarea.clickok
		
	# if clickoff:
		# tarea.clickoff
	
	# if sobreon:
		# tarea.sobreOn
		
	# if sobreOf:
		# tarea.sobreoff
		
		
		