import pygame

pygame.init()
ancho = 400
alto = 150
fondo = (0,0,0)
titulo = "archivo Pygame para pruebas"
screen = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption(titulo)
screen.fill(fondo)

#imagen = pygame.image.load("bttn.png")
#areaimg = imagen.get_rect()
#print areaimg.height, areaimg.width
#screen.blit(imagen,(ancho/2,alto/2))
#pygame.display.update()


pygame.display.flip()
texto = ""
y = 10
x = 0
font = pygame.font.SysFont("Comic Sans", 20) 
teclaname1 = ""
teclaname2 = ""
aux = []
out = []

while 1 == 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

		if event.type == pygame.KEYDOWN:
			aux = pygame.key.get_pressed()
			lon = len(aux)
			for i in range(0,lon-1):
				if aux[i] == 1:
					out.append(i)

			for i,key_constant in enumerate(out):
				print key_constant
				teclaname1 = pygame.key.name(key_constant)							
				x += 7
				text_surface = font.render(teclaname1, True, (255,0,0))
				if x > (ancho -20):
					x = 0
					y+= 20						
				screen.blit(text_surface,(x,y)) 
				pygame.display.flip()					
					
#			for key_constant, presionado in enumerate(pygame.key.get_pressed()):								
#				if presionado:
#					teclaname1 = pygame.key.name(key_constant)							
#					x += 7
#					text_surface = font.render(teclaname1, True, (255,0,0))
#					if x > (ancho -20):
#						x = 0
#						y+= 20						
#					screen.blit(text_surface,(x,y)) 
#					print teclaname1
#					pygame.display.flip()
		
		else:
			pygame.draw.rect(screen,fondo,[(0,0),(ancho,alto)],0)
			x = 0
			y = 0
			aux = []
			out = []





