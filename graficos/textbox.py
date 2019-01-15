import pygame

alto = 400
ancho = 300
fondo = (0,0,0)

#------argumentos------
#-- "estado":0,1,2,3,
#-- "label":"contenido del txt box"
#-- "x": esquina superior izq.(coordenada X)
#-- "y": esquina superior izq.(coordenada Y)
#-- "longitud": Dimension X del txtbox.
#-- "altitud":  Dimension X del txtbox.
#-- "rgb": Diccionario RGB con colores.
rgb = {"rojo":150,"verde":150,"azul":150}
argumentos = {"estado":0,"label":"","x":ancho/2,"y":alto/2,"longitud":100,"altitud":20,"rgb":rgb}

txts = {}        #---- contiene el objeto txtbox
contadortxts = 0 #---- contador de txtbox en pantalla
nombrestxt = []  #---- guarda los nombres de los txtbox Ej: "txt0","txt1"...

pygame.init()
screen = pygame.display.set_mode((ancho,alto))
screen.fill(fondo)


class txtbox():
	def __init__(self,screen):
	#---- Parametros iniciales ----		
		# estados:
		# 0-- habilitado esta disponible para escribir. pero lo que se ingrese lo tomara el estado 3.
		# 1-- bloqueado	txtbloqueado.
		# 2-- mostrar txt ReadOnly.
		# 3-- escribiendo Esta disponible para escribir y es el que recibe lo ingresado.
		self.estado = 0      #---- definido arriba.
		self.txtnombre = 0   #---- identificador interno del txtbox: "0","1"...
		self.label = ""      #---- contenido del txtbox.
		self.x = 0           #---- coordenada x de la esq. sup. izq.
		self.y = 0			 #---- coordenada y de la esq. sup. izq.
		self.longitud = 0    #---- ancho del txtbox.
		self.altitud = 0	 #---- alto del txtbox. 
		self.dif = 1		 #---- separacion de pixeles entre los dos cuadrados del txtbox.
		self.difc = 50       #---- contraste entre los dos cuadrados que conforman el txtbox.
		self.rojo = 0        #---- R.
		self.verde = 0       #---- G.
		self.azul = 0        #---- B.

	def dibujar(self,screen,contadortxts,argumentos):

		self.estado = argumentos["estado"]
		self.txtnombre = contadortxts
		self.label = argumentos["label"]
		self.x = argumentos["x"]
		self.y = argumentos["y"]
		self.longitud = argumentos["longitud"]		
		self.altitud = argumentos["altitud"] 	
		self.rojo = argumentos["rgb"]["rojo"] 
		self.verde = argumentos["rgb"]["verde"] 
		self.azul = argumentos["rgb"]["azul"] 

		rgr = self.rojo 		# -- rojo del cuadrado grande (el de atras)
		vgr = self.verde		# -- verde del cuadrado grande 
		agr = self.azul 		# -- azul del cuadrado grande 
		xgr = self.x     		# -- x del cuadrado grande
		ygr = self.y     		# -- y del cuadrado grande
		longigr = self.longitud # -- longitud del cuadrado grande
		altigr = self.altitud	# -- altitud del cuadrado grande 	

		rch = self.rojo-self.difc		 	 # -- rojo del cuadrado chico (el de adelante)
		vch = self.verde-self.difc		 	 # -- verde del cuadrado chico
		ach = self.azul-self.difc 			 # -- azul del cuadrado chico
		xch = self.x+self.dif     			 # -- x del cuadrado chico
		ych = self.y+self.dif   			 # -- y del cuadrado chico
		longich = self.longitud - self.dif*2 # -- longitud del cuadrado chico
		altich = self.altitud - self.dif*2	 # -- altitud del cuadrado chico

		rrc = 255		 	 # -- rojo del rectangulo 
		vrc = 255		 	 # -- verde del rectangulo
		arc = 255 			 # -- azul del rectangulo	
		
		rr = pygame.draw.rect(screen,(rgr,vgr,agr),[(xgr,ygr),(longigr,altigr)],0)
		pygame.draw.rect(screen,(rch,vch,ach),[(xch,ych),(longich,altich)],0)		
		pygame.draw.rect(screen,(rrc,vrc,arc),[(xch,ych),(longich,altich)],1)
		pygame.display.update(rr)

	def escribiendo(self,txts,contadortxts,nombrestxt,screen):		
		for i in range (0,contadortxts):
			if i == self.txtnombre:
				self.estado = 3
			else:
				txts[nombrestxt[i]].estado = 0					
		rojo = 0
		verde = 0
		azul = 0
		x = self.x + self.dif*2
		y = self.y + self.dif*2
		longi = 3
		alti = self.altitud-(self.dif*4)
		rc = pygame.draw.rect(screen,(0,0,0),[(x,y),(longi,alti)],0)
		pygame.display.update(rc)		

	def desescribir(self,txts,contadortxts,nombrestxt,screen):
		for i in range(0,contadortxts):
			txts[nombrestxt[i]].estado = 0
		rojo = self.rojo - self.difc
		verde = self.verde - self.difc
		azul = self.azul - self.difc
		x = self.x + self.dif*2
		y = self.y + self.dif*2
		longi = 3
		alti = self.altitud-(self.dif*4)
		rectang = pygame.draw.rect(screen,(rojo,verde,azul),[(x,y),((self.longitud)-4,(self.altitud)-4)],0)
		pygame.display.update(rectang)	

def creartxt(screen,txts,contadortxts,argumentos):
	nombrestxt = "txt"+str(contadortxts)
	txt = txtbox(screen)
	txt.dibujar(screen,contadortxts,argumentos)
	txts[nombrestxt] = txt
	contadortxts = contadortxts + 1
	return txts, contadortxts, nombrestxt

def main(txts,nombrestxt,contadortxts):
	salir = 0
	delay = 800
	interval = 20
	font = pygame.font.SysFont(None, 20)  
	font_height = font.get_linesize()
	#pygame.key.set_repeat(delay,interval)
	yyy = 0 	
	while salir == 0:		
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				salir = 1
			if event.type == pygame.MOUSEBUTTONDOWN:			
				a = 1

			if event.type == pygame.MOUSEBUTTONUP:					
				for i in range(0,contadortxts):							
					if(mouse[0] <= (txts[nombrestxt[i]].longitud + txts[nombrestxt[i]].x) and mouse[0] >= txts[nombrestxt[i]].x) and (mouse[1] <= (txts[nombrestxt[i]].altitud + txts[nombrestxt[i]].y) and mouse[1] >= txts[nombrestxt[i]].y):			
						txts[nombrestxt[i]].escribiendo(txts,contadortxts,nombrestxt,screen)
					else:
						if txts[nombrestxt[i]].estado == 3:		
							print nombrestxt[i]				
							txts[nombrestxt[i]].desescribir(txts,contadortxts,nombrestxt,screen)
							yyy = 0
			
			if event.type == pygame.KEYDOWN:				
				for i in range(0,contadortxts):
					if txts[nombrestxt[i]].estado == 3:								
						for key_constant, presionado in enumerate(pygame.key.get_pressed()):
							if presionado == 1:
							#pygame.draw.rect(screen,fondo,[((ancho/2)-30,(alto/2)-30),(90,90)],0)						
								teclaname = pygame.key.name(key_constant)								
								if teclaname == "space":
									teclaname = " "
								if teclaname == "backspace":
									teclaname = ""
								if teclaname == "return":
									teclaname = ""
									txts[nombrestxt[i]].desescribir(txts,contadortxts,nombrestxt,screen)
									yyy = 0
								else:
									txts[nombrestxt[i]].label += teclaname
									yyy += 7	
									
								text_surface = font.render(teclaname, True, (255,0,0))
			 					screen.blit(text_surface,(txts[nombrestxt[i]].x+yyy, txts[nombrestxt[i]].y+3)) 
								pygame.display.flip()


#creo los txtboxs.

rgb = {"rojo":150,"verde":150,"azul":150}
argumentos = {"estado":0,"label":"","x":ancho/2,"y":alto/2,"longitud":100,"altitud":20,"rgb":rgb}
txts, contadortxts, nombretxtaux = creartxt(screen,txts,contadortxts,argumentos)
nombrestxt.append(nombretxtaux)

rgb = {"rojo":150,"verde":150,"azul":150}
argumentos = {"estado":0,"label":"","x":ancho/2,"y":(alto/2) + 50,"longitud":100,"altitud":20,"rgb":rgb}
txts, contadortxts, nombretxtaux = creartxt(screen,txts,contadortxts,argumentos)
nombrestxt.append(nombretxtaux)

rgb = {"rojo":150,"verde":150,"azul":150}
argumentos = {"estado":0,"label":"","x":ancho/2,"y":(alto/2) + 100,"longitud":100,"altitud":20,"rgb":rgb}
txts, contadortxts, nombretxtaux = creartxt(screen,txts,contadortxts,argumentos)
nombrestxt.append(nombretxtaux)

main(txts,nombrestxt,contadortxts)
