import Tkinter as tk
import time
import random

class Propiedades:
	#Clase que contiene todas las variables "globales"
	anchoPantalla = 250  # alto de la pantalla.
	altoPantalla = 250   # ancho de la pantalla.
	tile = 10            # alto y ancho del tile.
	colorFondo = [0,0,0] # color del fondo.
	modoPaleta = "MC"	 # CS = Color Solido, MC = Monocromatico, NCS = n-colores solidos, NMC = n-cromaticos
	
class Paleta:
	def __init__(self):
		self.iniciarPaleta()

	def iniciarPaleta(self):
		self.modo = Propiedades.modoPaleta # CS = Color Solido, MC = Monocromatico, NCS = n-colores solidos, NMC = n-cromaticos
		self.paleta = []
		for i in range(0,256):
			self.paleta.append(Propiedades.colorFondo[:])
		
	def setearPaleta(self,modo,listaColores):
		#modos: Color solido, Monocromatico, n-colores solidos, n-cromaticos
		#Color solido: se pintan todos los circulos de un solo color.
		#monocromatico: se pintan los circulos de un solo matiz de colores segun la intensidad. es decir con degrade del color elegido al color de fondo.
		#n-colores solidos: se pintan los circulos de n-colores solidos segun la intensidad.
		#n-cromaticos: se pintan los circulos con n-colores en degrade.
		
		#listaColores: si modo es CS --> se agarra el primer item de la lista, ese es el color.
		#listaColores: si modo es MC --> se agarran los primeros dos items de la lista, el primero es el color de inicio y el segundo es el final.
		#listaColores: si modo es NCS -> se agarran todos los items de listaColores, en este caso van a ser tuplas de la pinta [R,G,B,hasta] donde hasta indica donde finaliza el color en cuestion. es obligatorio cubrir los 255 espacios de paleta, y se pueden pasar hasta un maximo de 255 tuplas, de modo que cada valor de paleta tendra un color especifico.
		
		#Ejemplos de llamadas a setearPaleta		
		#p.setearPaleta("CS",[[255,0,0]])		
		#p.setearPaleta("MC",[[0,255,0],[255,0,255]])	
		#p.setearPaleta("NCS",[[0,0,0,50],[100,100,100,75],[200,0,200,150],[152,152,152,255]])
		#p.setearPaleta("NMC",[[[0,0,0],[100,100,100],99],[[200,0,200],[0,200,0],150],[[0,100,0],[100,0,100],255]])
		
		if(modo == "CS"): # listaColores: =>  [[R,G,B]]
			# a toda la paleta le pone el mismo color
			for i in range(0,256):
				self.paleta[i][0] = listaColores[0][0] #R
				self.paleta[i][1] = listaColores[0][1] #G
				self.paleta[i][2] = listaColores[0][2] #B
		
		if(modo == "MC"): # listaColores => [[R,G,B],[R,G,B]]
			#interpolar entre el color listaColores[0] y listaColores[1] <<-- (Desde y hasta).
			colorDesde = listaColores[0]
			colorHasta = listaColores[1]
			self.paleta = self.interpolarRGB(colorDesde,colorHasta,0,255)[:]
			
		if(modo == "NCS"): # listaColores => [[R,G,B,hasta],[R,G,B,hasta], ...]
			desde = 0
			for l in listaColores:
				hasta = l[3]+1
				for i in range(desde,hasta):
					self.paleta[i][0] = l[0]
					self.paleta[i][1] = l[1]
					self.paleta[i][2] = l[2]
				desde = l[3]+1
		
		if(modo == "NMC"): #listaColores => [[[R,G,B],[R,G,B],hasta],[[R,G,B],[R,G,B],hasta], ...]
			# interpolar por partes, en lista colores se guarda una tupla, que tiene 3 items cada una; dos colores y hasta donde va ese tramo.
			desde = 0
			hasta = 0
			for l in listaColores:
				hasta = l[2]
				self.paleta[desde:hasta] = self.interpolarRGB(l[0],l[1],desde,hasta)[:]
				desde = hasta + 1
				
		#for i in range(0,256):
		#	print i, self.paleta[i], '' 
		
	def interpolarRGB(self,colorDesde,colorHasta,desde,hasta):
		#interpolacion lineal para colores, dados los puntos de inicio y fin y los colores en esos puntos, se calculan todos los intermedios(de manera lineal).
		paletaTemporal = []
		delta = hasta - desde
		pasoRojo = float(colorHasta[0] - colorDesde[0])/delta
		pasoVerde= float(colorHasta[1] - colorDesde[1])/delta
		pasoAzul = float(colorHasta[2] - colorDesde[2])/delta

		paletaTemporal.append(colorDesde)
		
		# recordar que paleta es un array de 256 posiciones, donde cada item de la lista es un nivel de intensidad.
		#for i in range(desde + 1, hasta + 1): 
		for i in range(1, delta + 1): 
			rojo  = int(round(colorDesde[0] + (pasoRojo * i)))
			verde = int(round(colorDesde[1] + (pasoVerde * i)))	
			azul  = int(round(colorDesde[2] + (pasoAzul * i)))
			paletaTemporal.append([rojo,verde,azul])
	
		return paletaTemporal
		
		
class Pantalla:
	def __init__(self,canvas):
		self.altoPantalla = Propiedades.altoPantalla   	# alto de la pantalla
		self.anchoPantalla = Propiedades.anchoPantalla 	# ancho de la pantalla
		self.tile = Propiedades.tile                   	# alto y ancho del tile
		self.matrizPantalla = []		         		# matriz con la intensidad de cada tile de la pantalla.
		self.paleta = Paleta()					 		# mapeo de colores. de 0 a 255, cada item de paleta relaciona un valor de intensidad con un color, dependiendo del criterio de coloreado. Por ejemplo, si es color solido, paleta se vera asi: [[255,0,0],[255,0,0],[255,0,0],[255,0,0],[255,0,0],...]
		self.colorFondo = Propiedades.colorFondo		# color del fondo.

		self.iniciarMatrizPantalla()
		self.iniciarPantallaGrafica(canvas)
		
	def iniciarMatrizPantalla(self):
		self.matrizPantalla = []
		for i in range(0,(self.anchoPantalla)/self.tile):
			self.matrizPantalla.append([])
			for j in range(0,(self.altoPantalla)/self.tile):
				self.matrizPantalla[i].append(random.choice(range(0,255))) # el cero insertado es la intensidad, y puede ser de 0 a 255.
				#self.matrizPantalla[i].append(250) 
		#print self.matrizPantalla
	
	def dibujar(self): # esta es la funcion principal del programa :)
		salto = self.tile/2
		pasoX = salto
		pasoY = salto
		for i in range(0,(self.anchoPantalla/self.tile)):
			for j in range(0,(self.altoPantalla/self.tile)):
				radio = (self.matrizPantalla[i][j]/255.0)*(self.tile/2) # esto es para pasar de 0 a 255 a un valor entre 0 y el radio maximo(que dependiendo de la pantalla es un valor distinto).
				color = self.pasarRGBaHexa(self.paleta.paleta[self.matrizPantalla[i][j]]) # paleta es un mapa que guarda el color asignado a cada intensidad.
				self.dibujarCirculo(pasoX,pasoY,radio,color)
				pasoY += self.tile
			pasoX += self.tile
			pasoY = salto
			
	def dibujarCirculo(self,x,y,radio,color):			
		# EVENTUALMENTE VA A DIBUJAR UN CIRCULO en un tile			
		self.canvas.create_circle(x, y, radio, fill=color,width=0)
		
	def iniciarPantallaGrafica(self,canvas):
		self.canvas = canvas
	
	@classmethod
	def pasarRGBaHexa(self,color):
		result = "#"
		#print color
		for c in color:
			aux = str(hex(c))[2:]
			if(len(aux) == 1):
				result += "0" + aux
			else:
				result += aux
			
		#print result
		return result
	


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

		
def main():
	
	root = tk.Tk()
	canvas = tk.Canvas(root, width=Propiedades.anchoPantalla, height=Propiedades.altoPantalla, borderwidth=0, highlightthickness=0, bg=Pantalla.pasarRGBaHexa(Propiedades.colorFondo))
	canvas.grid()
	tk.Canvas.create_circle = _create_circle	
	
	root.wm_title("Circulos")
	pantalla1 = Pantalla(canvas)
	pantalla1.paleta.setearPaleta("MC",[[0,0,0],[255,255,255]])
	
	for i in range(0,5):
		pantalla1.canvas.delete("all")
		pantalla1.iniciarMatrizPantalla()
		pantalla1.dibujar()
		raw_input("Presione una tecla para contiunar...")
		
	root.mainloop()
	
if __name__ == '__main__':
	main()

		
#Pantalla1 = Pantalla(40,40,10)

#Pantalla1.matrizPantalla = [[255,242,226,210],[194,178,162,146],[130,114,88,72],[64,48,32,16]]

#Pantalla1.dibujar()
#raw_input("Presione una tecla para contiunar...")		