import pygame
from iniciarpy import *
ancho = 350
alto = 50
fondo = (0,0,0)
titulo = "colores"
screen = iniciarpygame(ancho,alto,fondo,titulo)

anch = 50
alt = 50


#violeta (143,0,255) a rojo
color =[143,0,255]
#print color
#for i in range(0,ancho,anch):
#	for j in range(0,alto,alt):
#		color[2] -= 1
#		pygame.draw.rect(screen,color,((i,j),(i+50,j+50)),0)
#		pygame.draw.aalines(screen,(0,0,0),1, ((i,j),(i+50,j),(i+50,j+50),(i,j+50)),1)
#print color
#pygame.display.flip()

color = [0,255,0]
#color = [0,0,255]
pygame.draw.rect(screen,color,((0,0),(50,50)),0)
pygame.draw.line(screen,color,(0,0),(50,50),1)
color = [43,255,0]
#color = [40,0,212]
pygame.draw.rect(screen,color,((50,0),(100,50)),0)
pygame.draw.line(screen,color,(50,0),(100,50),1)
color = [86,255,0]
#color = [83,0,169]
pygame.draw.rect(screen,color,((100,0),(150,50)),0)
pygame.draw.line(screen,color,(100,0),(150,50),1)
color = [132,255,0]
#color = [126,0,126]
pygame.draw.rect(screen,color,((150,0),(200,50)),0)
pygame.draw.line(screen,color,(150,0),(200,50),1)
color = [178,255,0]
#color = [169,0,83]
pygame.draw.rect(screen,color,((200,0),(250,50)),0)
pygame.draw.line(screen,color,(200,0),(250,50),1)
color = [224,255,0]
#color = [212,0,40]
pygame.draw.rect(screen,color,((250,0),(300,50)),0)
pygame.draw.line(screen,color,(250,0),(300,50),1)
color = [255,255,0]
#color = [255,0,0]
pygame.draw.rect(screen,color,((300,0),(350,50)),0)
pygame.draw.line(screen,color,(300,0),(350,50),1)



#for i in range(0,ancho,anch):
#	pygame.draw.rect(screen,color,((i,0),(i+50,50)),0)
#	pygame.draw.line(screen,color,(i,0),(i,50),1)
#	color[2] -= 51
#	color[0] += 22
#print color
pygame.display.flip()


salir = 0
while salir == 0:		
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1

