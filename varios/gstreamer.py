import pygame
from boton import *
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# para crear un boton hay que usar la clase contenedor(), esta lleva un registro de todos los botones en un diccionario, con nombre de boton("btn0","btn1",)

	
#----------------------------------------------------------------------------------------------------
#-----datos iniciales-------
ancho = 400
alto = 150
fondo = (0,0,0)
titulo = "clase botones"
volumen = 1
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
sound = pygame.mixer.music.load('b.mp3')
pygame.mixer.music.set_volume(1)
#----inicializa el modulo pygame y setea la pantalla
pygame.init()
screen = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption(titulo)
screen.fill(fondo)
pygame.display.update()

#--- creo el contenedor para el objeto boton y su indice de nombre. 
contenedorbtns = contenedor()

#--- creo el objeto para el loop
httest = hittest()

#----funciones de los botones --------
#btn0:
#---------------
def btn0press():
	print "BTN0PRESS"
def btn0release():
	print "BTN0RELEASE"
	pygame.mixer.music.play(1)
def btn0over():
	print "BTN0OVER"
#----------------
#btn1:
#---------------
def btn1press():
	print "BTN1PRESS"
def btn1release():
	print "BTN1RELEASE"
	pygame.mixer.music.fadeout(1000)
def btn1over():
	print "BTN1OVER"
#----------------
#btn2:
#---------------
def btn2press():
	print "BTN2PRESS"
def btn2release():
	print "BTN2RELEASE"
	pygame.event.post(pygame.event.Event(pygame.QUIT))
def btn2over():
	print "BTN2OVER"
#----------------
#btn3:
#---------------
def btn3press():
	print "BTN3PRESS"
def btn3release():
	print "BTN3RELEASE"
	volumen = pygame.mixer.music.get_volume()	
	if volumen == 1:
		pygame.mixer.music.set_volume(0)
	else:
		pygame.mixer.music.set_volume(1)
def btn3over():
	print "BTN3OVER"
#----------------
#btn4:
#---------------
def btn4press():
	print "BTN4PRESS" 
def btn4release():
	print "BTN4RELEASE"
def btn4over():
	print "BTN4OVER" 
#----------------
#btnN:
#---------------
def btnNpress():
	pass
def btnNrelease():
	pass
def btnNover():
	pass
#----------------
#--------------------------------------------------------------
#------ cargo argumentos con los parametros que quiero --------
#--------------------------------------------------------------
#--- boton(estado,label,x,y,ancho,alto,press,release,over,rojo,verde,azul)
#--- botonimg(estado,img,label,x,y,press,release,over)

#btn0
contenedorbtns.boton_nuevo(0, "play", 30, alto/2, 150, 30, btn0press, btn0release, btn0over, 50, 50, 50)

#btn1
contenedorbtns.boton_nuevo(0, "stop", 80, alto/2, 30, 30, btn1press, btn1release, btn1over, 50, 50, 50)

#btn2
contenedorbtns.boton_nuevo(0, "salir", 200, alto/2, 30, 30, btn2press, btn2release, btn2over, 50, 50, 50)
contenedorbtns.botones["btn2"].texto("salir",(255,0,0))

#btn3
contenedorbtns.boton_nuevo(0, "off/on", 130, alto/2, 30, 30, btn3press, btn3release, btn3over, 50, 50, 50)

#btn4
contenedorbtns.boton_nuevo_c_img(0,"bttn.png","",20,20,btn4press,btn4release,btn4over)
contenedorbtns.botones["btn4"].texto("o",(255,0,0))

#----------------------------------

#----ciclo para chequear los botones.
while httest.salir == 0:
	httest.mouse()






