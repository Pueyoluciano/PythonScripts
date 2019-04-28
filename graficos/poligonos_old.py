import pygame
import os
from iniciarpy import *
ancho = 200
alto = 200
fondo = (0,0,0)
titulo = "Poligonos"
screen = iniciarpygame(ancho,alto,fondo,titulo)

def interfaz(modo):
	os.system("clear")
	print("----------------------------------------------")
	print("----------------------------------------------")
	print("----------------- polis V1.0 -----------------")
	print("\n\n\n\n\n")
	if (modo == 0):
		print("(-) Para dibujar clickear la pantalla")
	
	if (modo == 1):
		print("Lados:")
		lados = input("> ")
		interfaz(2)

	if (modo == 2):
		print("Radio: ")
		lados = input("> ")
		return lados		

class interfaz():

	def __init__(self):
		pass

	def pantalla_inicial(self):
		os.system("clear")
		print("----------------------------------------------")
		print("----------------------------------------------")
		print("----------------- polis V1.0 -----------------")
		print("\n\n\n\n\n")
	
	def radio(self):
		pass
	
	def lados(self):
		pass


salir = 0
#interfaz(0)
while salir == 0:		
	for event in pygame.event.get():
		mouse = pygame.mouse.get_pos()					
		if event.type == pygame.QUIT:
			salir = 1
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse = pygame.mouse.get_pos()
			#interfaz(1)

	pygame.draw.cirle()


	pygame.time.wait(5)


