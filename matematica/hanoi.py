import pygame
import os
from iniciarpy import *
ancho = 400
alto = 200
fondo = (0,0,0)
titulo = "Torres de Hanoi"
screen = iniciarpygame(ancho,alto,fondo,titulo)



def terminado(t1,t2,t3,opt,discos):
	if (opt == 2):
		for i in range(0,discos):
			terminado = 1
			if (t2[i] != i + 1):
				terminado = 0
		return terminado

	if (opt == 3):
		for i in range(0,discos):
			terminado = 1
			if (t3[i] != i + 1):
				terminado = 0
		return terminado

salir = 0


#---------------------------------------------------

def correr(dsd,hst,quien):
	hst[quien] = dsd[quien]
	dsd[quien] = 0


def torres():
	color = (0,60,0)
	torre = (((ancho*(1.0/6.0))-5,20),(10,150))
	pygame.draw.rect(screen,color,torre,0)

	torre = (((ancho*(3.0/6.0))-5,20),(10,150))
	pygame.draw.rect(screen,color,torre,0)

	torre = (((ancho*(5.0/6.0))-5,20),(10,150))
	pygame.draw.rect(screen,color,torre,0)

	torre = ((ancho*(1.0/16.0),170),(ancho-(ancho*(2.0/16.0)),-10))
	pygame.draw.rect(screen,color,torre,0)

	pygame.display.flip()				


def click(mouse):
	pass


class disco():
	def __init__(self):
		self.color = [100,100,100]
		self.x = 30
		self.y = 30

class con_discos():
	def __init__(self):
		self.cont = 0
		self.t1 = []
		self.t2 = []
		self.t3 = []

	
	def agregardisco(self):
		self.t1.append(self.cont+1)
		self.t2.append(0)
		self.t3.append(0)
		self.cont += 1

	def dibujar(self):
		contadory = 0
		for i in range(0,self.cont):
			if(self.t1[i] != 0):
				contadory += 1				
				rect,clr = parametros(self.t1[i],1,contadory)
				pygame.draw.rect(screen,clr,rect,0)
				pygame.display.flip()

		for i in range(0,self.cont):
			if(self.t2[i] != 0):
				contadory += 1				
				rect,clr = parametros(self.t1[i],2,contadory)
				pygame.draw.rect(screen,clr,rect,0)
				pygame.display.flip()

		for i in range(0,self.cont):
			if(self.t3[i] != 0):
				contadory += 1				
				rect,clr = parametros(self.t1[i],2,contadory)
				pygame.draw.rect(screen,clr,rect,0)
				pygame.display.flip()
		
			#pygame.draw.arc(screen,color, Rect, 90,270, width=0)		
					
def parametros(entrada,tx,cnty):
	x = 20 + (20*entrada)
	y = (25*cnty) + 50
	rojo = 0
	verde = 0
	azul = 0
	centro = ancho*((1.0/6.0)+((2.0/6.0)*(tx-1)))
	cuadrado = [(centro -(x/2),y),(x,- 30)]

	if (entrada%1 == 0):
		rojo += 100
	
	if (entrada%2 == 0):
		verde += 100
	
	if (entrada%3 == 0):
		azul += 100		
	if (entrada%4 == 0):
		rojo = 0	

	color = [rojo,verde,azul]
	print cuadrado
	return cuadrado,color

discos = con_discos()

discos.agregardisco()
discos.agregardisco()
discos.agregardisco()
discos.agregardisco()


torres()

discos.dibujar()	



while (salir == 0):
	for event in pygame.event.get():
		mouse = pygame.mouse.get_pos()					
		if event.type == pygame.QUIT:
			salir = 1
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse = pygame.mouse.get_pos()
			click(mouse)
			correr(discos.t1,discos.t2,2)
			discos.dibujar()	









