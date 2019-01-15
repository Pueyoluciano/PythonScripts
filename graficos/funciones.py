#-------------------------------------------------
# ------------------  Imports  -------------------
#-------------------------------------------------
import pygame
import math
import os
import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica
import time
import random
from iniciarpy import *

#-------------------------------------------------
# -----------------  pantalla  -------------------
#-------------------------------------------------
class pantalla():
	def __init__(self):
		pygame.init()

	def iniciar(self):
		self.ancho = 400
		self.alto = 400
		self.titulo = 'Funciones'
		self.screen = pygame.display.set_mode((self.ancho,self.alto))
		self.pxarray = pygame.PixelArray(self.screen)
		pygame.display.set_caption('Funciones')
		self.screen.fill((0,0,0))
		self.pxarray = pygame.PixelArray(self.screen)
		# inicializo los extremos de la pantalla
		self.minimox = -1.0
		self.maximox = 1.0
		self.minimoy = -1.0
		self.maximoy = 1.0
		# calculo la relacion entre X e Y
		self.ratio = matematica.mcd(self.ancho,self.alto)
		self.ratiox = self.ancho/self.ratio
		self.ratioy = self.alto/self.ratio
		# convierto los bordes a la relacion anterior
		self.minimox *= self.ratiox
		self.maximox *= self.ratiox
		self.minimoy *= self.ratioy
		self.maximoy *= self.ratioy

		self.minimox *= 2
		self.maximoy *= 2 
		#calculo el salto en X y en Y
		self.saltox = abs(self.maximox-self.minimox)/self.ancho
		self.saltoy = abs(self.maximoy-self.minimoy)/self.alto

		#print self.saltox, self.saltoy

	def traducir(self,valor,coor):
	# traducir recibe un punto del plano y devuelve el valor correspondiente segun la escala, dimensiones etc.
		if (coor == 'x'):
			salida = self.minimox+(self.saltox * valor)

		if (coor == 'y'):
			salida = self.minimoy+(self.saltoy * valor)
		
		return salida		

	def traducirinv(self,valor,coor):
	# traducirinv(el inverso de traducir) recibe un valor en escala y devuelve la coordenada del pixel.
		if(coor =='x'):
			salida = (valor - self.minimox)/self.saltox

		if(coor =='y'):
			salida = (valor - self.minimoy)/self.saltoy

		return salida

	def x(self):
		for i in range(0,self.ancho):
			x = self.traducir(float(i),'x')
			y = self.traducirinv(x,'y')
			print x,y
			self.pxarray[i,int(y)] = [255,0,0]
		pygame.display.flip()

	def graficarsin(self):
		for i in range(0,self.ancho):
			x = self.traducir(float(i),'x')
			y = self.traducirinv(math.sin(x),'y')
			print x,y
			self.pxarray[i,int(y)] = [255,0,0]

		pygame.display.flip()


#-------------------------------------------------
# ------------------  Acciones  ------------------
#-------------------------------------------------
pantalla1 = pantalla()
pantalla1.iniciar()
pantalla1.x()

raw_input('...')


