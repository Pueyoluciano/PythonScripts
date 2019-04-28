import pygame
from iniciarpy import *

class pantalla():
	def __init__(self,estado,x,y,ancho,alto,margenx,margeny,color1,color2,texto,colortxt,fuente,tamanotxt,alineamiento,maxtxt,press,release,over):
		# estado = 0 (habilitado para escribir)
		# estado = 1 (escribiendo)
		# estado = 2 (bloqueado)
		# alineamiento = 0 (alienado a la izq)
		# alineamiento = 1 (centrado)
		# alineamiento = 2 (alienado a la der)
		self.estado = 0		
		self.x = x
		self.y = y
		self.ancho = ancho
		self.alto = alto
		self.margenx = margenx
		self.margeny = margeny
		self.color1 = color1
		self.color2 = color2
		self.texto = texto
		self.colortxt = colortxt
		self.tamanotxt = tamanotxt
		self.fuente = pygame.font.Font(fuente, self.tamanotxt)
		self.alineamiento = alineamiento
		self.maxtxt = maxtxt
		self.press = press
		self.release = release
		self.over = over
		self.dibujar()

	def dibujar(self):
		cuadrado0 = pygame.draw.rect(screen,fondo,[(self.x,self.y),(self.ancho,self.alto)],0)
		pygame.display.update(cuadrado0)	
		cuadrado = pygame.draw.rect(screen,self.color1,[(self.x,self.y),(self.ancho,self.alto)],0)
		cuadrado2 = pygame.draw.rect(screen,self.color2,[(self.x+self.margenx,self.y+self.margeny),(self.ancho-(2*self.margenx),self.alto-(2*self.margeny))],0)
		self.ctexto("")		
		pygame.display.update(cuadrado)
	
	# --cargar estado --
	def cestado(self, valor):
		self.estado = valor
		xi = self.x+self.margenx
		yi = self.y + self.margeny
		xf = self.x + self.margenx
		yf = self.y + self.alto - self.margeny
		if self.estado == 0:
			aux = pygame.draw.aaline(screen,self.color2,(xi,yi),(xf,yf),5)
		else:
			aux = pygame.draw.aaline(screen,(255,0,0),(xi,yi),(xf,yf),5)
		pygame.display.update(aux)

	def ctexto(self,texto):
		self.texto += str(texto)
		x = 0
		y = 0
		#--- alineamiento:
		# -- 0: alienado a la izq.
		# -- 1: centrado.
		# -- 2: alienado a la der.
		xy = self.fuente.size(self.texto)
		cuadrado = pygame.draw.rect(screen,self.color2,[(self.x+self.margenx,self.y+self.margeny),(self.ancho-(2*self.margenx),self.alto-(2*self.margeny))],0)

		if self.alineamiento == 0:
			x = self.x + 2*(self.margenx)
			y = (self.y + self.alto - 2*self.margeny)/2 + xy[1]/2

		if self.alineamiento == 1:	
			x = self.x + (self.ancho - 2*self.margenx)/2 - xy[0]/2
			y = (self.y + self.alto - 2*self.margeny)/2 + xy[1]/2

		if self.alineamiento == 2:
			x = self.ancho +self.x -2*self.margenx - xy[0]
			y = (self.y + self.alto - 2*self.margeny)/2 + xy[1]/2
		text = self.fuente.render(self.texto,20,self.colortxt)
		screen.blit(text,(x,y))
		pygame.display.update(cuadrado)

class contenedor():
	def __init__(self):				
		self.secuenciab = 0
		self.secuenciap = 0					
		self.botones = {}
		self.pantallas = {}
	#--- botones --------------------
#	def agregarboton(self,nuevoitem):		
#		pos = "btn" + str(self.secuenciab)
#		self.secuenciab += 1
#		self.botones[pos] = nuevoitem
#	
#	def boton_nuevo(self,estado,label,x,y,ancho,alto,press,release,over,rojo,verde,azul):
#		aux = boton(estado,label,x,y,ancho,alto,press,release,over,rojo,verde,azul)
#		self.agregarboton(aux)
#	
#	def boton_nuevo_c_img(self,estado,img,label,x,y,press,release,over):
#		aux = botonimg(estado,img,label,x,y,press,release,over)
#		self.agregarboton(aux)
	#-------------------------------

	#--- pantallas -----------------
	def agregarpantalla(self,nuevoitem):
		pos = "ptn"+ str(self.secuenciap)
		self.secuenciap += 1
		self.pantallas[pos] = nuevoitem

	def pantalla_nueva(self,estado,x,y,ancho,alto,margenx,margeny,color1,color2,texto,colortxt,fuente,tamanotxt,alineamiento,maxtxt,press,release,over):
		aux = pantalla(estado,x,y,ancho,alto,margenx,margeny,color1,color2,texto,colortxt,fuente,tamanotxt,alineamiento,maxtxt,press,release,over)
		self.agregarpantalla(aux)
	#-------------------------------
	
#----------------------------------------------------------------------------------------------------		
#------------------------------
#--- funciones press, release, over de las pantallas ---
#----------------
#bnt0:
#---------------
def ptn0press():
	print("ptn0 PRESS")
	micontenedor.pantallas["ptn0"].ctexto("1")
	print(micontenedor.pantallas["ptn0"].texto)
def ptn0release():
	print("ptn0 RELEASE")
def ptn0over():
	print("ptn0 OVER")
#----------------
#bnt1:
#---------------
def ptn1press():
	print("ptn1 PRESS")
def ptn1release():
	print("ptn1 RELEASE")
def ptn1over():
	print("ptn1 OVER")
#----------------
#bnt2:
#---------------
def ptn2press():
	print("ptn2 PRESS")
def ptn2release():
	print("ptn2 RELEASE")
def ptn2over():
	print("ptn2 OVER")
#----------------
#bntN:
#---------------
#def ptnNpress():
#	pass
#def ptnNrelease():
#	pass
#def ptnNover():
#	pass
#----------------
#-------------------------------------------------------

#--- parametros de pantalla ---
ancho = 400
alto = 150
fondo = (0,0,0)
titulo = "clase pantalla"
screen = iniciarpygame(ancho,alto,fondo,titulo)
salir = 0
ptnapretado = ""
#------------------------------
#pantalla_nueva (estado,x,y,ancho,alto,margenx,margeny,color1,color2,texto,colortxt,fuente,tamanotxt,alineamiento,maxtxt,press,release,over)

micontenedor = contenedor()
micontenedor.pantalla_nueva(0,20,20,70,30,3,3,(100,100,100),(50,50,50),"pantalla0",(255,0,0),None,20,0,100,ptn0press,ptn0release,ptn0over)
micontenedor.pantalla_nueva(0,100,20,70,30,3,3,(100,100,100),(50,50,50),"pantalla1",(255,0,0),None,20,0,100,ptn1press,ptn1release,ptn1over)
micontenedor.pantalla_nueva(0,180,20,70,30,3,3,(100,100,100),(50,50,50),"pantalla2",(255,0,0),None,20,0,100,ptn2press,ptn2release,ptn2over)



while salir == 0:		
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1
			if event.type == pygame.MOUSEBUTTONDOWN:
				hit = 0			
				for i in range(0,micontenedor.secuenciap):
					ptn = "ptn"+str(i)
					xinicial = micontenedor.pantallas[ptn].x				
					xfinal = micontenedor.pantallas[ptn].x + micontenedor.pantallas[ptn].ancho
					yinicial = micontenedor.pantallas[ptn].y
					yfinal = micontenedor.pantallas[ptn].y + micontenedor.pantallas[ptn].alto
					if (mouse[0] >= xinicial and mouse[0]<= xfinal) and (mouse[1] >= yinicial and mouse[1]<= yfinal):
						hit = 1						
						for i in range(0,micontenedor.secuenciap):
							ptn2 = "ptn"+str(i)
							if ptn2 != ptn:
								micontenedor.pantallas[ptn2].cestado(0)
							else:
								ptnapretado = ptn2
								micontenedor.pantallas[ptn2].cestado(1)
								micontenedor.pantallas[ptn].press()	
						break
				if hit == 0:
					ptnapretado = ""
					for i in range(0,micontenedor.secuenciap):
						ptn3 = "ptn"+str(i)
						micontenedor.pantallas[ptn3].cestado(0)			

			if event.type == pygame.MOUSEBUTTONUP:
				if ptnapretado != "":
					micontenedor.pantallas[ptnapretado].release()



