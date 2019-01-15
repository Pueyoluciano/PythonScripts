import pygame

pygame.init()
ancho = 400
alto = 400
fondo = (0,0,0)
screen = pygame.display.set_mode((ancho,alto))
screen.fill(fondo)



def main ():
	salir = 0	
	font = pygame.font.Font(None, 20)
	font_height = pygame.font.Font.get_linesize(font)
	poss = 0
	while salir == 0:				
		for event in pygame.event.get():					
			if event.type == pygame.QUIT:
				salir = 1
			if event.type == pygame.KEYDOWN:				
				for key_constant, presionado in enumerate(pygame.key.get_pressed()):
					if presionado == 1:
						pygame.draw.rect(screen,fondo,[((ancho/2)-30,(alto/2)-30),(90,90)],0)						
						teclaname = pygame.key.name(key_constant)
						print teclaname						
						text_surface = font.render(teclaname, True, (127,255,212))			 					
						xy = font.size(teclaname)
						poss = poss + xy[0]						
						screen.blit(text_surface,((ancho/2)+poss, alto/2))
						pygame.display.flip()
			else:
				a = 1 
		
main()			

