import pygame
import math
from iniciarpy import *

#--- parametros de pantalla ---
ancho = 200
alto = 200
fondo = (0,0,0)
titulo = "poligonos"
screen = iniciarpygame(ancho,alto,fondo,titulo)
#------------------------------
# -- variables iniciales --
salir = 0
radian = math.pi/180
# -------------------------

class pantalla():
	def __init__(self):
		self.poligonos = []
		self.cuadrillas = []
		self.cuad(10,10,[50,50,50],1)

	def poli(self,x,y,angulo,ratiox,ratioy,radio,lados,color,width):
		self.poligonos.append(poligono(x,y,angulo,ratiox,ratioy,radio,lados,color,width))
		self.actualizar()

	def cuad(self,x,y,color,width):
		self.cuadrillas = cuadrilla(x,y,color,width)
		pygame.display.flip()		

	def actualizar(self):
		for i in range (0,len(self.poligonos)):
			pygame.display.update(self.poligonos[i].rect)

class cuadrilla():
	def __init__(self,x,y,color,width):
		# x e y son el numero de divisiones que tendran dichos ejes.
		self.x = x
		self.y = y
		stepx = ancho/(x+1)
		stepy = alto/(y+1)
		for i in range(0,x):
			pygame.draw.line(screen,color,(stepx+(stepx*i),0),(stepx+(stepx*i),alto),width)			
		for i in range(0,y):
			pygame.draw.line(screen,color,(0,stepy+(stepy*i)),(ancho,stepy+(stepy*i)),width)		

class poligono():
	def __init__(self,x,y,angulo,ratiox,ratioy,radio,lados,color,width):	
		self.puntos = []
		self.x = x
		self.y = y
		self.angulo = angulo
		self.ratiox = ratiox
		self.ratioy = ratioy
		self.radio = radio
		self.lados = lados		
		self.color = color
		self.width = width
		self.grados = 360.0/self.lados
		for i in range(0,lados):
			xp = self.x + (self.ratiox * self.radio * math.cos(radian*((self.grados*i)+self.angulo)))
			yp = self.y + (self.ratioy * self.radio * math.sin(radian*((self.grados*i)+self.angulo)))
			self.puntos.append([xp,yp])
		self.cargar(self.color,self.puntos,self.width)		
		
	def cargar(self,color,puntos,width):
		self.rect = pygame.draw.aalines(screen, color, 1, puntos, width)



pantalla1 = pantalla()


#Poligono(x,y,angulo,ratiox,ratioy,radio,lados,color,width)	

def esfera(pantalla):

	pantalla.poli(ancho/2,alto/2,0,1,1,50,100,[255,0,0],1)
	pantalla.poli(ancho/2,alto/2,0,0.75,1,50,100,[255,100,100],1)
	pantalla.poli(ancho/2,alto/2,0,0.50,1,50,100,[255,100,100],1)
	pantalla.poli(ancho/2,alto/2,0,0.25,1,50,100,[255,100,100],1)
	pantalla.poli(ancho/2,alto/2,0,0,1,50,100,[255,100,100],1)

	pantalla.poli(ancho/2,alto/2,0,1,0.75,50,100,[255,100,100],1)
	pantalla.poli(ancho/2,alto/2,0,1,0.50,50,100,[255,100,100],1)
	pantalla.poli(ancho/2,alto/2,0,1,0.25,50,100,[255,100,100],1)
	pantalla.poli(ancho/2,alto/2,0,1,0,50,100,[255,100,100],1)

pantalla1.poli(ancho/2,alto/2,0,1,1,50,8,[255,0,0],1)
pantalla1.poli(ancho/2,alto/2,0,0.9,0.9,50,8,[200,0,0],1)

#------------------------------
while salir == 0:		
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1
			if event.type == pygame.MOUSEBUTTONDOWN:
				pass
			if event.type == pygame.MOUSEBUTTONUP:
				pass

