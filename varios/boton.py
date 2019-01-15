import pygame
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# para crear un boton hay que usar la clase contenedor(), esta lleva un registro de todos los botones en un diccionario, con nombre de boton("btn0","btn1",)

class boton():
	def __init__(self,screen,estado,label,x,y,ancho,alto,press,release,over,rojo,verde,azul):
	#---- Parametros iniciales ----	
		self.screen = screen
		self.estado = estado
		self.label = label
		self.x = x
		self.y = y
		self.ancho = ancho
		self.alto = alto
		self.press = press
		self.release = release
		self.over = over
		self.rojo = rojo
		self.verde = verde
		self.azul = azul
		self.colortxt = (100,100,100)
		self.tamanotxt = 20
		self.fuente = pygame.font.Font(None, self.tamanotxt)
		self.xy = self.fuente.size(self.label)
		self.margenx = 20
		self.margeny = 15
		self.dibujar()

	def dibujar(self):
		cuadrado = pygame.draw.rect(self.screen,(self.rojo,self.verde,self.azul),[(self.x,self.y),(self.ancho,self.alto)],0)
		self.estado = 0
		self.texto(self.label,self.colortxt)
		pygame.display.update(cuadrado)

	def texto(self,lbl,color):	
		cuadrado = pygame.draw.rect(self.screen,fondo,((self.x,self.y),(self.ancho,self.alto)),0)
		pygame.display.update(cuadrado)
		self.xy = self.fuente.size(lbl)		
		if (self.xy[0] > (self.ancho - self.margenx)) or (self.ancho > self.xy[0]+self.margenx):
			self.ancho = self.xy[0]+ self.margenx
		if self.xy[1] > (self.alto - self.margeny) or (self.alto > self.xy[1]+self.margeny):
			self.alto = self.xy[1]+ self.margeny	
				
		cuadrado = pygame.draw.rect(self.screen,(self.rojo,self.verde,self.azul),((self.x,self.y),(self.ancho,self.alto)),0)
		text = self.fuente.render(lbl, self.tamanotxt, color)
		#-----centra el texto en el boton--		
		difx = (self.ancho - self.xy[0])/2
		dify = (self.alto - self.xy[1])/2
		if difx < 0:
			difx = difx*(-1)
		if dify < 0:
			dify = dify*(-1)
		#----------------------------------
		screen.blit(text,(difx+self.x,dify+self.y))
		pygame.display.update(cuadrado)

class botonimg():
	def __init__(self,screen,estado,img,label,x,y,press,release,over):
	#---- Parametros iniciales ----	
		self.screen = screen
		self.estado = estado
		self.img = pygame.image.load(img)
		self.label = label
		self.x = x
		self.y = y
		self.rect = self.img.get_rect()
		self.ancho = self.rect.width
		self.alto = self.rect.height 
		self.press = press		
		self.release = release
		self.over = over
		self.colortxt = (100,100,100)
		self.tamanotxt = 20
		self.fuente = pygame.font.Font(None, self.tamanotxt)
		self.xy = self.fuente.size(self.label)
		self.margenx = 20
		self.margeny = 15
		self.dibujar()

	def dibujar(self):
		self.estado = 0		
		cuadrado = pygame.draw.rect(self.screen,fondo,((self.x,self.y),(self.ancho,self.alto)),0)		
		
		self.texto(self.label,self.colortxt)
		pygame.display.update(cuadrado)

	def texto(self,lbl,color):	
		cuadrado = pygame.draw.rect(self.screen,fondo,((self.x,self.y),(self.ancho,self.alto)),0)
		pygame.display.update(cuadrado)
		self.xy = self.fuente.size(lbl)		
		if (self.xy[0] > (self.ancho - self.margenx)) or (self.ancho > self.xy[0]+self.margenx):
			#self.ancho = self.xy[0]+ self.margenx
			pass
		if self.xy[1] > (self.alto - self.margeny) or (self.alto > self.xy[1]+self.margeny):
			#self.alto = self.xy[1]+ self.margeny	
			pass
				
		screen.blit(self.img,(self.x,self.y))
		text = self.fuente.render(lbl, self.tamanotxt, color)
		#-----centra el texto en el boton--		
		difx = (self.ancho - self.xy[0])/2
		dify = (self.alto - self.xy[1])/2
		if difx < 0:
			difx = difx*(-1)
		if dify < 0:
			dify = dify*(-1)
		#----------------------------------
		screen.blit(text,(difx+self.x,dify+self.y))
		pygame.display.update(cuadrado)

class contenedor():
	def __init__(self):				
		self.secuencia = 0					
		self.botones = {}

	def agregarboton(self,nuevoitem):		
		pos = "btn" + str(self.secuencia)
		self.secuencia += 1
		self.botones[pos] = nuevoitem
	
	def boton_nuevo(self,screen,estado,label,x,y,ancho,alto,press,release,over,rojo,verde,azul):
		aux = boton(screen,estado,label,x,y,ancho,alto,press,release,over,rojo,verde,azul)
		self.agregarboton(aux)
	
	def boton_nuevo_c_img(self,screen,estado,img,label,x,y,press,release,over):
		aux = botonimg(screen,estado,img,label,x,y,press,release,over)
		self.agregarboton(aux)

#---hace las veces de main, detecta si se toco/solto un boton.	
class hittest():
	def __init__(self):
		self.salir = 0
		self.btnapretado = ""
		self.xinicial = 0
		self.xfinal = 0
		self.yinicial = 0
		self.yfinal = 0

	def mouse(self):
		for event in pygame.event.get():
			#--- mouse = [x,y]:
			#---- mouse[0] = x.
			#---- mouse[1] = y.
			mouse = pygame.mouse.get_pos()					
			if event.type == pygame.QUIT:
				self.salir = 1
				break			
			if event.type == pygame.MOUSEBUTTONDOWN:			
				for i in range(0,contenedorbtns.secuencia):
					btn = "btn"+str(i)
					self.xinicial = contenedorbtns.botones[btn].x				
					self.xfinal = contenedorbtns.botones[btn].x + contenedorbtns.botones[btn].ancho
					self.yinicial = contenedorbtns.botones[btn].y
					self.yfinal = contenedorbtns.botones[btn].y + contenedorbtns.botones[btn].alto
					if (mouse[0] >= self.xinicial and mouse[0]<= self.xfinal) and (mouse[1] >= self.yinicial and mouse[1]<= self.yfinal):
						if contenedorbtns.botones[btn].estado == 0:					
							contenedorbtns.botones[btn].press()
							contenedorbtns.botones[btn].estado = 1
							self.btnapretado = btn
							break
			if event.type == pygame.MOUSEBUTTONUP:
				if self.btnapretado != "":		
					if (mouse[0] >=self.xinicial and mouse[0]<= self.xfinal) and (mouse[1] >= self.yinicial and mouse[1]<= self.yfinal):
						contenedorbtns.botones[self.btnapretado].release()
					contenedorbtns.botones[self.btnapretado].estado = 0
#----------------------------------------------------------------------------------------------------
