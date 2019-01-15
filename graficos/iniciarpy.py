def iniciarpygame (ancho,alto,fondo,titulo):
	import pygame	
	pygame.init()
	screen = pygame.display.set_mode((ancho,alto))
	pygame.display.set_caption(titulo)
	screen.fill(fondo)
	return screen

