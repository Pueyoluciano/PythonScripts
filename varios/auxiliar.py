import pygame
import boton #importo la clase boton
#import os
#import math

#-------------------------------------------------------------------------------------
#----------------------------- Interfaz grafica --------------------------------------
#-------------- Dimensiones -----------------------------
#-------------- Globales --------------------------------

ancho = 400      # ancho de la pantalla.
alto = 200       # alto de la pantalla.
fondo = (0,0,0)  # color de fondo.
bloqueado = 0    # estado del boton.
label = ""       # texto del boton.
x = 0            # x del boton (coordenada x del punto superior izquierdo).
y = 0            # y del boton (coordenada y del punto superior izquierdo).
longitud = 0     # ancho del boton.
altitud = 0      # alto del boton.
rojo = 0         # R.
verde = 0        # G.  
azul = 0         # B.
rgb = {"rojo":rojo,"verde":verde,"azul":azul}
argumentos = {"bloqueado":bloqueado,"label":label,"x":x,"y":y,"longitud":longitud,"altitud":altitud,"rgb":rgb}
contador = 0     # contador unico para asignar botones.
botones = {}     # diccionario de instancias de boton y sus metodos y demas.
presionados = {} # diccionario de los "press" de cada boton.
sueltos = {}     # diccionario de los "release" de cada boton.
sobres = {}      # diccionario de los "over" de cada boton.
nombre = []      # lista de nombres de todos los botones.

#-------------- inicia modulo pygame---------------------

pygame.init()

#-------------- se crea interfaz grafica-----------------

screen = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("interfaz grafica")
screen.fill(fondo)

#--------------------------------------------------------------------------------------
#------------------ creador de botones ------------------------------------------------
#crearboton toma los datos del boton a crear y las variables de control de botones(botones,contador)

def crearboton(botones,presionados,sueltos,sobres,btnpress,btnrelease,btnover,contador,screen,argumentos):
	nombre = "btn"+str(contador)
	btn = boton.boton(screen)	
	btn.dibujar(screen,argumentos)
	botones[nombre] = btn
	presionados[nombre] = btnpress
	sueltos[nombre] = btnrelease
	sobres[nombre] = btnover 
	contador = contador + 1
	return botones, nombre, contador

#--------------- Fuciones PRESS RELEASE Y OVER para todos los botones -----------------
#--------------------------------------------------------------------------------------
#----- Btn0 ------------------------------

def btn1press(screen):
	pygame.draw.rect(screen,(255,0,0),[(50,50),(30,30)],0)

def btn1release(screen):
	pygame.draw.rect(screen,(255,0,255),[(100,50),(30,30)],0)

def btn1over(screen):
	pygame.draw.rect(screen,(0,0,255),[(150,50),(30,30)],0)	

#-----------------------------------------
#----- Btn2 ------------------------------

def btn2press(screen):
	pygame.draw.rect(screen,(255,255,0),[(50,50),(30,30)],0)

def btn2release(screen):
	pygame.draw.rect(screen,(0,0,255),[(100,50),(30,30)],0)
	# Crea un evento tipo QUIT, y lo carga con el post.
	pygame.event.post(pygame.event.Event(pygame.QUIT))
	
def btn2over(screen):
	pygame.draw.rect(screen,(0,0,255),[(150,50),(30,30)],0)	

#-----------------------------------------
#----- Btn3 ------------------------------

def btn3press(screen):
	pygame.draw.rect(screen,(0,255,0),[(50,50),(30,30)],0)

def btn3release(screen):
	pygame.draw.rect(screen,(255,255,255),[(100,50),(30,30)],0)

def btn3over(screen):
	pygame.draw.rect(screen,(255,255,0),[(150,50),(30,30)],0)

#-----------------------------------------
#----- Btn4 ------------------------------

def btn4press(screen):
	pygame.draw.rect(screen,(100,0,0),[(50,50),(30,30)],0)

def btn4release(screen):
	pygame.draw.rect(screen,(0,100,0),[(100,50),(30,30)],0)

def btn4over(screen):
	pygame.draw.rect(screen,(0,100,0),[(50,50),(30,30)],0)

#-----------------------------------------
#----- BtnN ------------------------------

#def btnNpress(screen):
#def btnNrelease(screen):
#def btnNover(screen):

#-----------------------------------------
#-------------------------------------------------------------------------------------
#Btn 0
# le paso los parametros del boton
argumentos["bloqueado"] = 0
argumentos["label"] = "hola"
argumentos["x"] = ancho/2
argumentos["y"] = alto/2
argumentos["longitud"] = 50
argumentos["altitud"] = 20
argumentos["rgb"]["rojo"] = 100
argumentos["rgb"]["verde"] = 0
argumentos["rgb"]["azul"] = 0

# llamo a la funcion para crear el boton.
botones, nombreaux, contador = crearboton(botones,presionados,sueltos,sobres,btn1press,btn1release,btn1over,contador,screen,argumentos)
nombre.append(nombreaux)
#Btn 1

argumentos["bloqueado"] = 0
argumentos["label"] = "Salir"
argumentos["x"] = (ancho/2)+70
argumentos["y"] = alto/2
argumentos["longitud"] = 50
argumentos["altitud"] = 20
argumentos["rgb"]["rojo"] = 0
argumentos["rgb"]["verde"] = 100
argumentos["rgb"]["azul"] = 0

botones, nombreaux, contador = crearboton(botones,presionados,sueltos,sobres,btn2press,btn2release,btn2over,contador,screen,argumentos)
nombre.append(nombreaux)
#Btn 2

argumentos["bloqueado"] = 0
argumentos["label"] = ":D"
argumentos["x"] = (ancho/2)-70
argumentos["y"] = alto/2
argumentos["longitud"] = 50
argumentos["altitud"] = 20
argumentos["rgb"]["rojo"] = 0
argumentos["rgb"]["verde"] = 0
argumentos["rgb"]["azul"] = 100

botones, nombreaux, contador = crearboton(botones,presionados,sueltos,sobres,btn3press,btn3release,btn3over,contador,screen,argumentos)
nombre.append(nombreaux)
#Btn 3

argumentos["bloqueado"] = 0
argumentos["label"] = ":C"
argumentos["x"] = (ancho/2)-140
argumentos["y"] = alto/2
argumentos["longitud"] = 50
argumentos["altitud"] = 20
argumentos["rgb"]["rojo"] = 0
argumentos["rgb"]["verde"] = 100
argumentos["rgb"]["azul"] = 100

botones, nombreaux, contador = crearboton(botones,presionados,sueltos,sobres,btn4press,btn4release,btn4over,contador,screen,argumentos)
nombre.append(nombreaux)

#-------------------------------------------------------------------------------------
#rgb = {"rojo","verde","azul"}
#argumentos = {"bloqueado","label","x","y","longuitd","altitud","rgb"}
#bot1.dibujar(screen,argumentos)
#bot1.bloquear(0)
#bot1.sobre(screen,btn1over)

#---------------------------------------

pygame.display.flip()

#-------------------------------------------------------------------------------------
# ------------------------loop principal------------------------

def main(botones,nombre,contador):
	salir = 0	
	presanterior = 0 
#	sueltanterior = 0

	while salir == 0:
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1

			if event.type == pygame.MOUSEBUTTONDOWN:			
				presanterior = hittestbtndwn(screen,presionados,presanterior,botones,nombre,contador,mouse)	

			if event.type == pygame.MOUSEBUTTONUP:
				hitestbtnup(screen,sueltos,nombre,botones,contador,mouse)
			
#			if 	event.type != pygame.MOUSEBUTTONDOWN and event.type != pygame.MOUSEBUTTONUP:		
#				for i in range (0,contador):				
#					if (mouse[0] >= botones[nombre[i]].x and mouse[0] <= (botones[nombre[i]].x + botones[nombre[i]].ancho)) and (mouse[1] >= botones[nombre[i]].y and mouse[1] <= (botones[nombre[i]].y + botones[nombre[i]].alto)):
#						a = 5
#-------------------------------------------------------------------------------------
# ---------------------------HitTests----------------------------
#--------------- HitPresionado ---------------

def hittestbtndwn(screen,presionados,presanterior,botones,nombre,contador,mouse):
	for i in range (0,contador):	
		if presanterior == 0:
			if (mouse[0] >= botones[nombre[i]].x and mouse[0] <= (botones[nombre[i]].x + botones[nombre[i]].ancho)) and (mouse[1] >= botones[nombre[i]].y and mouse[1] <= (botones[nombre[i]].y + botones[nombre[i]].alto)):	
				botones[nombre[i]].presionar(screen,presionados[nombre[i]])
				pygame.display.flip()	
				presanterior = 1	
		else:
			presanterior = 0
	return presanterior

#--------------- HitSuelto ---------------

def hitestbtnup(screen,sueltos,nombre,botones,contador,mouse):
	for i in range (0,contador):			
		if (mouse[0] >= botones[nombre[i]].x and mouse[0] <= (botones[nombre[i]].x + botones[nombre[i]].ancho)) and (mouse[1] >= botones[nombre[i]].y and mouse[1] <= (botones[nombre[i]].y + botones[nombre[i]].alto)):	
			botones[nombre[i]].presionar(screen,sueltos[nombre[i]])
			pygame.display.flip()		

#-------------------------------------------------------------------------------------

#print presionados, sueltos, sobres
main(botones,nombre,contador)


