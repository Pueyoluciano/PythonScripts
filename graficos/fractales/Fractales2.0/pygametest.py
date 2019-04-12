import pygame
import threading
import Queue
from validador import *

# pygame.init()

# screen = pygame.display.set_mode((150, 150))
# pygame.display.set_caption("tutorial pygame parte 4")

# salir = False
# clock = pygame.time.Clock()
# while not salir:
	# for event in pygame.event.get():
		# if event.type == pygame.QUIT:
			# salir = True
	# tick = clock.tick(25)

class Pantalla(threading.Thread):
	def __init__(self,ancho,alto,titulo,colorfondo,queue):
		threading.Thread.__init__(self)
		self.queue = queue
		pygame.init()
		self.screen = pygame.display.set_mode((ancho,alto))
		pygame.display.set_caption(titulo)
		self.pixelArray = pygame.PixelArray(self.screen)
		self.clock = pygame.time.Clock()
		self.colorfondo = colorfondo
		self.acciones = {"actualizar":self.actualizar,"resize":self.resize}
		
	def run(self):
		Salir = False
		
		while not Salir:

			self.tick = self.clock.tick(20)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					salir = True
					
			#polling = self.queue.get()
			#if (polling.accion in self.acciones):
			#	self.acciones[polling.accion](polling.parametros)
			
	def actualizar(self,parametros):
		if(parametros["refresco"]):
			self.screen.fill(self.colorfondo)
		
		# self.screen.blit(parametros["pixelarray"].surface,(0,0))
		self.pixelArray = parametros["pixelarray"]
		pygame.display.flip()
	
	def resize(self,ancho,alto):
		self.screen = pygame.display.set_mode((ancho,alto))
		
		
queue = Queue.Queue()		
p = Pantalla(50,50,"titulo",[0,0,0],queue)		
p.daemon = True

p.start()
p.join()

while True:
	print validador.ingresar(str)
	



