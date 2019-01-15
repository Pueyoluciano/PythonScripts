class Controlador:
	def __init__(self):
		self.ancho = 200
		self.alto = 100
		self.titulo = "asd"
		pygame.init()
		self.screen = pygame.display.set_mode((self.ancho,self.alto))
		pygame.display.set_caption(self.titulo)
		self.clock = pygame.time.Clock()
	
		self.contenido = [] # lista de dashboards
		
	def loop(self):
		salir = False
			while not salir:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						salir = True
					else:
						
						self.screen.fill(self.colorfondo)
						
						for tarea in self.controlador.dashboards[self.dashSeleccionado].tareas:
							self.dibujarTarea(tarea)
						
				self.tick = self.clock.tick(self.fps)
				
		pygame.quit()
	
		