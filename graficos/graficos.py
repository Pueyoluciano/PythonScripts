import pygame
import math
from iniciarpy import *
ancho = 300
alto = 200 
fondo = (0,0,0)
titulo = "graficos"
screen = iniciarpygame(ancho,alto,fondo,titulo)

color = [0,0,100]
x = ancho/2
y = alto/2
angulo = 0
while 1 == 1:
	pygame.draw.line(screen,color,(x,y),(x+(30)*(math.cos((math.pi/180)*angulo)),y+(30)*(math.sin((math.pi/180)*angulo))),1)
	angulo = angulo+1
	
	if (color[0]< 255):
		color[0] = color[0] + 1
	else:
		if (color[1]< 255):
			color[1] = color[1] + 1			
	
	if(x<200):
		x = x + 1	
	

	
	pygame.display.flip()
#	pygame.time.wait(50)

