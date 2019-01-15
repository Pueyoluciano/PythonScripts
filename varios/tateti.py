import pygame

#---clase boton :D.
class boton():
	def __init__(self,screen,x,y,lon,alt,nombre):
		self.x = x
		self.y = y
		self.lon = lon
		self.alt = alt	
		#--- estados:
		#----- 0: limpio.
		#----- 1: 0.
		#----- 2: X.	
		self.estado = 0
		self.nombre = nombre
		#pygame.draw.rect(screen,(60,60,60),[(self.x, self.y),(self.lon, self.alt)],0)
		

	def presionado(self,screen,jugador):
		#--jugador 0		
		cirx = (self.x + (self.lon/2))
		ciry = (self.y + (self.alt/2))
		radio = int(round(self.lon / (2.5)))
		color = (0,30,0)
		#-- jugador 1		
		#-- cruxiar: cruz X izquierda arriba	
		#-- cruyiar: cruz Y izquierda arriba	
		#-- cruxiab: cruz X izquierda abajo	
		#-- cruyiab: cruz Y izquierda abajo
		#-- cruxdar: cruz X derecha arriba	
		#-- cruydar: cruz Y derecha arriba	
		#-- cruxdab: cruz X derecha abajo	
		#-- cruydab: cruz Y derecha abajo	
		a = 4.5
		cruxiar = self.x + self.lon/(a)
		cruyiar = self.y + self.alt/(a)
		cruxiab = self.x + self.lon/(a)
		cruyiab = (self.y + self.alt) - (self.alt/(a))
		cruxdar = (self.x + self.lon) - (self.lon/(a))
		cruydar = self.y + self.alt/(a)			
		cruxdab = (self.x + self.lon) - (self.lon/(a))
		cruydab = (self.y + self.alt) - (self.alt/(a))

		color2 = (30,0,0) 			
		if self.estado == 0:		
			if jugador == 1:
				pygame.draw.circle(screen, color, [cirx, ciry], radio, 3)
				self.estado = 1
			else:
				pygame.draw.line(screen, color2, (cruxiab,cruyiab),(cruxdar,cruydar), 3)
				pygame.draw.line(screen, color2, (cruxiar,cruyiar),(cruxdab,cruydab), 3)			
				self.estado = 2

	def juegonuevo(self,screen,fondo):
		cuadrado = pygame.draw.rect(screen,fondo,[(self.x,self.y),(self.lon,self.alt)],0)
		self.estado = 0
		pygame.display.update(cuadrado)

def tateti():
	#--- dibuja los margenes
	#----- linea: RGB
	linea = (30,30,30)
	#--	linea vertical izquierda.
	pygame.draw.line(screen, linea, ((margen+lon),(margen/2)),((margen+lon), (alto-(margen/2))), 3)
	#-- linea vertical derecha.	
	pygame.draw.line(screen, linea, (margen+(lon*2),margen/2), (margen+(lon*2),alto-(margen/2)), 3)
	#-- linea horizontal arriba.	
	pygame.draw.line(screen, linea, (margen/2,margen+alt),((ancho-menu)-(margen/2),margen+alt), 3)
	#-- linea horizontal abajo.	
	pygame.draw.line(screen, linea, (margen/2,alto-(margen+alt)),((ancho-menu)-(margen/2),alto-(margen+alt)), 3)
	

def puntajes():
	linea = (30,30,30)
	#--- linea vertical:
	xiv = tat + (menu/2)
	yiv = (margen/2)
	xfv = xiv 
	yfv = alto - margen

	#375 15 375 270 480 120 570 120

	#--- linea horizontal:
	xih = tat + (margen/2)
	yih = margen * 2
	xfh = ancho - (margen/2)
	yfh = yih

	pygame.draw.line(screen,linea, ((xiv),(yiv)),((xfv), (yfv)), 3)
	pygame.draw.line(screen,linea, ((xih),(yih)),((xfh), (yfh)), 3)


def gameover(puntos):
	aux = [0,0]
	pts = 0
	#---resultado = 0: sigue jugando.
	#---resultado = 1: Gana jugador 1.
	#---resultado = 2: Gana jugador 2.	
	resultado = 0
#	print puntos	
	for a in range (1,3):
#		print a
		if puntos[0] == a and puntos[1] == a and puntos[2] == a:
			resultado = a
			print "PUUM!"
			return resultado
			#break
		else:
			if puntos[3] == a and puntos[4] == a and puntos[5] == a:	
				resultado = a
				print "PUUM!"
				return resultado
				#break
			else:
				if puntos[6] == a and puntos[7] == a and puntos[8] == a:
					resultado = a
					print "PUUM!"
					return resultado
					#break
				else:
					if puntos[0] == a and puntos[3] == a and puntos[6] == a:	
						resultado = a
						print "PUUM!"
						return resultado
						#break
					else:
						if puntos[1] == a and puntos[4] == a and puntos[7] == a:
							resultado = a
							print "PUUM!"
							return resultado
							#break
						else:
							if puntos[2] == a and puntos[5] == a and puntos[8] == a:	
								resultado = a
								print "PUUM!"
								return resultado
								#break
							else:
								if puntos[0] == a and puntos[5] == a and puntos[8] == a:	
									resultado = a
									print "PUUM!"
									return resultado
									#break
								else:
									if puntos[2] == a and puntos[5] == a and puntos[6] == a:	
										resultado = a
										print "PUUM!"
										return resultado
										#break
									else:
										h = 1
		

#------------------------------------------------------------------			
#---- incializacion.

menu = 150
tat = 300 # tamano del tateti
ancho = tat + menu
alto = 300
margen = 30
lon = 80
alt = 80
fondo = (0,0,0)
juegon = 1
clicks = 0
resultado = 0
salir = 0
# --- puntuacion[0]: Jugador 1 puntaje.
# --- puntuacion[1]: Jugador 2 puntaje.

puntuacion = {}
puntuacion["1"]= 0
puntuacion["2"]= 0
#--- jugador:
#----- 1: 0.
#----- 2: X.

jugador = 1
#--- puntos = 0: Vacio.
#--- puntos = 1: marca jugador 1.
#--- puntos = 2: marca jugador 2.

puntos = [0,0,0,0,0,0,0,0,0]
nombres = {}

pygame.init()
screen = pygame.display.set_mode((ancho,alto))
screen.fill(fondo)

#---creacion de los cuadrados.

btn0 = boton(screen,margen+(lon*0),margen+(lon*0),lon,alt,"btn0")
nombres ["btn0"] = btn0
btn1 = boton(screen,margen+(lon*1),margen+(lon*0),lon,alt,"btn1")
nombres ["btn1"] = btn1
btn2 = boton(screen,margen+(lon*2),margen+(lon*0),lon,alt,"btn2")
nombres ["btn2"] = btn2
btn3 = boton(screen,margen+(lon*0),margen+(lon*1),lon,alt,"btn3")
nombres ["btn3"] = btn3
btn4 = boton(screen,margen+(lon*1),margen+(lon*1),lon,alt,"btn4")
nombres ["btn4"] = btn4
btn5 = boton(screen,margen+(lon*2),margen+(lon*1),lon,alt,"btn5")
nombres ["btn5"] = btn5
btn6 = boton(screen,margen+(lon*0),margen+(lon*2),lon,alt,"btn6")
nombres ["btn6"] = btn6
btn7 = boton(screen,margen+(lon*1),margen+(lon*2),lon,alt,"btn7")
nombres ["btn7"] = btn7
btn8 = boton(screen,margen+(lon*2),margen+(lon*2),lon,alt,"btn8")
nombres ["btn8"] = btn8


while salir == 0:		
	if juegon == 1:	
		juegon = 0
		clicks = 0
		for i in range(0,9):
			nombre = "btn"+ str(i)
			nombres[nombre].juegonuevo(screen,fondo)
			puntos[i] = 0
		tateti()
		puntajes()			
		pygame.display.flip()

	for event in pygame.event.get():
		#--- mouse = [x,y]:
		#---- mouse[0] = x.
		#---- mouse[1] = y.
		mouse = pygame.mouse.get_pos()					
		if event.type == pygame.QUIT:
			salir = 1
		if event.type == pygame.MOUSEBUTTONDOWN:			
			a = 1
		if event.type == pygame.MOUSEBUTTONUP:
			for i in range(0,9):								
				nombre = "btn"+ str(i)
				xxx = nombres[nombre].x + nombres[nombre].lon
				yyy = nombres[nombre].y + nombres[nombre].alt							
				if (mouse[0]>=nombres[nombre].x and mouse[0]<=xxx) and (mouse[1]>=nombres[nombre].y and mouse[1]<=yyy):
					nombres[nombre].presionado(screen,jugador)					
					puntos[i] = jugador	
					clicks += 1				
					if jugador == 1:
						jugador = 2
					else:
						jugador = 1					
					pygame.display.flip()
			resultado = gameover(puntos)
			if clicks < 9:
				if (resultado == 1 or resultado == 2):				
					juegon = 1
					puntuacion[str(resultado)] += 1
					print "jugador 1:", puntuacion["1"]
					print "jugador 2:", puntuacion["2"]
			else:
				juegon = 1					
				if (resultado == 1 or resultado == 2):				
					puntuacion[str(resultado)] += 1
				print "jugador 1:", puntuacion["1"]
				print "jugador 2:", puntuacion["2"]



