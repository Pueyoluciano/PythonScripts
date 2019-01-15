import pygame
from iniciarpy import *
ancho = 680
alto = 600
fondo = (0,0,0)
titulo = "colores"
screen = iniciarpygame(ancho,alto,fondo,titulo)

anch = 40
alt = 40


#violeta (143,0,255) a rojo
color =[143,0,255]
print color
for i in range(0,ancho,anch):
	for j in range(0,alto,alt):
		color[2] -= 1
		pygame.draw.rect(screen,color,((i,j),(i+50,j+50)),0)
		pygame.draw.aalines(screen,(0,0,0),1, ((i,j),(i+50,j),(i+50,j+50),(i,j+50)),1)
print color
pygame.display.flip()



salir = 0
while salir == 0:		
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1

