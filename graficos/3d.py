import pygame
import math
from iniciarpy import *
ancho = 300
alto = 300 
fondo = (0,0,0)
titulo = "3d"
screen = iniciarpygame(ancho,alto,fondo,titulo)

def dif(a,b):
	if a >= b:
		c = a-b
	else:
		c = b-a
	return c

#-------------------------------------------------
def pers(ang,a,b,x,y):
	xx = dif(a[0],b[0])
	yy = dif(a[1],b[1])
	zz = dif(a[2],b[2])
	l = math.sqrt((xx*xx)+(yy*yy)+(zz*zz))
	auxx = x
	auxy = y
	x = l*math.cos((math.pi/180)*ang)
	y = l*math.sin((math.pi/180)*ang)

	print x,y
	difx = auxx-x
	dify = auxy-y

	a[0] = a[0] + (difx/2)
	a[1] = a[1] + (dify/2)
	b[0] = b[0] - (difx/2)
	b[1] = b[1] - (dify/2)
	return a,b

#-------------------------------------------------------------------

class plano ():
	
	def __init__(self,centro,longitud,anguloyx,anguloyz,anguloxz):
		self.centro = centro
		self.longitud = longitud
		self.anguloyx = anguloyx
		self.anguloyz = anguloyz
		self.anguloxz = anguloxz
		self.a = [0,0,0]
		self.b = [0,0,0]
		self.c = [0,0,0]
		self.d = [0,0,0]
#		x = self.centro[0] + (-1*self.longitud)
#		y = self.centro[1] + (1*self.longitud)
#		z = self.centro[2] + (0*self.longitud)
#		self.a = [x,y,z]
#		print self.a
#		x = self.centro[0] + (1*self.longitud)
#		y = self.centro[1] + (1*self.longitud)
#		z = self.centro[2] + (0*self.longitud)
#		self.b = [x,y,z]
#		print self.b
#		x = self.centro[0] + (1*self.longitud)
#		y = self.centro[1] + (-1*self.longitud)
#		z = self.centro[2] + (0*self.longitud)
#		self.c = [x,y,z]
#		print self.c
#		x = self.centro[0] + (-1*self.longitud)
#		y = self.centro[1] + (-1*self.longitud)
#		z = self.centro[2] + (0*self.longitud)
#		self.d = [x,y,z]
#		print self.d
		self.rotar(0,self.anguloyx)
		#self.rotar(1,self.anguloyz)
		#self.rotar(2,self.anguloxz)

		self.dibujar([100,50,10])

	def dibujar(self,color):

		pygame.draw.line(screen,color,(self.a[0],self.a[1]),(self.b[0],self.b[1]),1)
		pygame.draw.line(screen,color,(self.b[0],self.b[1]),(self.c[0],self.c[1]),1)
		pygame.draw.line(screen,color,(self.c[0],self.c[1]),(self.d[0],self.d[1]),1)
		pygame.draw.line(screen,color,(self.d[0],self.d[1]),(self.a[0],self.a[1]),1)
		pygame.display.flip()

	def rotar(self,plano,angulo):
		#--plano : 
		#--0 = yx
		#--1 = yz
		#--2 = xz
		if plano == 0:
			x = self.centro[0] + ((math.cos((math.pi/180)*(135+angulo))) * self.longitud)
			y = self.centro[1] + ((math.sin((math.pi/180)*(135+angulo))) * self.longitud)
			self.a[0] = round(x,3)
			self.a[1] = round(y,3)

			x = self.centro[0] + ((math.cos((math.pi/180)*(45+angulo)))*self.longitud)
			y = self.centro[1] + ((math.sin((math.pi/180)*(45+angulo)))*self.longitud)
			self.b[0] = round(x,3)
			self.b[1] = round(y,3)

			x = self.centro[0] + ((math.cos((math.pi/180)*(315+angulo)))*self.longitud)
			y = self.centro[1] + ((math.sin((math.pi/180)*(315+angulo)))*self.longitud)
			self.c[0] = round(x,3)
			self.c[1] = round(y,3)

			x = self.centro[0] + ((math.cos((math.pi/180)*(225+angulo)))*self.longitud)
			y = self.centro[1] + ((math.sin((math.pi/180)*(225+angulo)))*self.longitud)
			self.d[0] = round(x,3)
			self.d[1] = round(y,3)
		
		if plano == 1:
			y = self.centro[1] + ((math.sin((math.pi/180)*(90+angulo))) * self.longitud)
			z = self.centro[2] + ((math.cos((math.pi/180)*(90+angulo))) * self.longitud)
			self.a[1] = round(y,3)
			self.a[2] = round(z,3)

			y = self.centro[1] + ((math.sin((math.pi/180)*(90+angulo))) * self.longitud)
			z = self.centro[2] + ((math.cos((math.pi/180)*(90+angulo))) * self.longitud)
			self.b[1] = round(y,3)
			self.b[2] = round(z,3)

			y = self.centro[1] + ((math.sin((math.pi/180)*(270+angulo))) * self.longitud)
			z = self.centro[2] + ((math.cos((math.pi/180)*(270+angulo))) * self.longitud)
			self.c[1] = round(y,3)
			self.c[2] = round(z,3)

			y = self.centro[1] + ((math.sin((math.pi/180)*(270+angulo))) * self.longitud)
			z = self.centro[2] + ((math.cos((math.pi/180)*(270+angulo))) * self.longitud)
			self.d[1] = round(y,3)
			self.d[2] = round(z,3)

		if plano == 2:
			pass

		self.dibujar([100,50,10])

		
	def mover(self,pos):


		self.dibujar([100,50,10])

miplano = plano([ancho/2,alto/2,0],50,0,0,0)

miplano.rotar(0,45)



salir = 0
while salir == 0:		
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1



