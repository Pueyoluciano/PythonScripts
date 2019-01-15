#----------------------------------------------------------------------
#----------------------------------------------------------------------
#-----------------------------FUNCIONES--------------------------------
#circulo(x,y,amp,oancho,oalto,rojo,verde,azul):
#-- x,y: centro del circulo.
#-- amp: radio.
#-- oancho: ovalo ancho, cantidad de estiramiento horizontal
#-- oalto: ovalo alto, cantidad de estiramiento vertical
#-- RGB: colores.

#cuadrado(xi,yi,xf,yf,rojo,verde,azul):
#-- xi,yi: esquina sup. derecha.
#-- xf,yf: esquina inf. izquierda.
#-- RGB: colores.

#poligono(x,y,amp,lados,des,rojo,verde,azul):
#-- x,y: centro del poligono.
#-- amp: radio.
#-- Lados: esquinas del P.
#-- des: Desfasaje.
#-- RGB: colores.

#pygame.draw.line(screen, color, origen, destino)
#pygame.draw.line(screen, (0, 0, 255), (0, 0), (300, 150))
#pygame.display.flip() --- Refresh.



import pygame
import os
import math
import time

ancho = 500
alto = 300
tiempo = 0.01

screen = pygame.display.set_mode((ancho, alto))
def arcoiris():
    rojo = 0
    verde = 0
    azul = 0
    frojo = 0
    fverde = 0
    fazul = 0
    resp = 0
    x = 50
    os.system("clear")    
    while resp == 0:
        x = x + 1    
        if frojo == 0:
            if rojo < 255:
                rojo = rojo +1
            if rojo == 255:
                frojo = 1
        if frojo == 1:
            if verde < 255:
                verde = verde + 1
            if verde == 255:
                fverde = 1
            if fverde == 1:
                if rojo > 0:
                    rojo = rojo - 1
                if rojo == 0:
                    frojo = 2
        if frojo == 2:       
            if azul < 255:
                azul = azul + 1
            if azul == 255:
                fazul = 1
            if fazul == 1:
                if verde > 0:
                    verde = verde - 1
                if verde == 0:
                    frojo = 3
        if frojo == 3:
            if rojo < 255:
                rojo = rojo +1
            if rojo == 255:
                fverde = 2
            if fverde == 2:
                if verde < 255:       
                    verde = verde + 1       
                if verde == 255:
                    resp = 1   
        pygame.draw.line(screen, (rojo,verde,azul), (x, 50), (x, 50))
    pygame.display.flip()   

def pantalla():
    screen.fill((0, 0, 0))
    #eje X
    pygame.draw.line(screen, (100, 100, 100), (10, int(alto/2)), (ancho-10,int(alto/2)))
    #eje Y   
    pygame.draw.line(screen, (100, 100, 100), (int(ancho/2), 10), (int(ancho/2),alto-10))
    pygame.display.flip()
   
def loop():
    enMarcha = 1
    while enMarcha:
        evento = pygame.event.poll()
        if evento.type == pygame.QUIT:
            enMarcha = 0
def linea():
    dist = 10
    for i in range (100,300,dist):
        pygame.draw.line(screen, (255, 0, 0), (i, i), (i, i))
        pygame.display.flip()   


def circulo(x,y,amp,oancho,oalto,rojo,verde,azul):
    for i in range (0,360):       
        seno = (amp*oalto)*(math.sin((i * math.pi)/180))
        coseno = (amp*oancho)*(math.cos((i * math.pi)/180))

        pygame.draw.line(screen, (rojo,verde,azul), (x+coseno,y+seno), (x+coseno,y+seno))

def cuadrado(xi,yi,xf,yf,rojo,verde,azul):
    pygame.draw.line(screen, (rojo,verde,azul), (xi,yi), (xf,yi))
    pygame.draw.line(screen, (rojo,verde,azul), (xi,yi), (xi,yf))
    pygame.draw.line(screen, (rojo,verde,azul), (xi,yf), (xf,yf))
    pygame.draw.line(screen, (rojo,verde,azul), (xf,yi), (xf,yf))
   
def poligono(x,y,amp,lados,des,rojo,verde,azul):   
    ang = 360/lados   
    ang2 = 0   
    for i in range(0,lados):
        seno = amp*(math.sin(((ang2+des) * math.pi)/180))
        coseno = amp*(math.cos(((ang2+des)* math.pi)/180))       
        senosig = amp*(math.sin(((ang2+ang+des) * math.pi)/180))
        cosenosig = amp*(math.cos(((ang2+ang+des) * math.pi)/180))        
        pygame.draw.line(screen, (rojo,verde,azul), (x+coseno,y+seno), (x+cosenosig,y+senosig))       
        #-----lineas flasheras       
        #senosig = amp*(math.sin(((ang2+ang) * math.pi)/180)*2)
        #cosenosig = amp*(math.cos(((ang2+ang) * math.pi)/180)*2)
        #pygame.draw.line(screen, (rojo,verde,azul), (x+coseno,y+seno), (x+cosenosig,y+senosig))               
        ang2 = ang2 + ang
   
   
   
pantalla()

roj = 0
for i in range(2,12):
    poligono(ancho/2,alto/2,100,i,0,100+roj,0,0)
    time.sleep(tiempo)   
    roj=roj+15   
    pygame.display.flip()

roj = 30
jjj = 15

for i in range(20,0,-5):
    circulo((ancho/2+20),(alto/2-30),jjj,1.2,1,roj,255,roj)
    roj= roj+40
    jjj = jjj - 3   
    time.sleep(tiempo)   
    pygame.display.flip()

for i in range (0,30):
    poligono((ancho/2)-40-(i*1.5),(alto/2)-55-(i*2),15-(i/2),5,0+i*3,255,255,255)
    poligono((ancho/2)+60+(i*1.5),(alto/2)-58-(i*2),15-(i/2),5,0-i*2,255,255,255)   
    time.sleep(tiempo)   
    pygame.display.flip()

for i in range (0,10):
    poligono((ancho/2)-70-(i*2),(alto/2)-40-(i*2),10-i,5,15+i*5,255,255,255)
    poligono((ancho/2)+85+(i*2),(alto/2)-43-(i*2),10-i,5,15-i*5,255,255,255)   
    time.sleep(tiempo)   
    pygame.display.flip()

for i in range (0,10):
    poligono((ancho/2)-15-(i/2),(alto/2)-80-(i*2),10-i,5,15+i*5,255,255,255)
    poligono((ancho/2)+35+(i/2),(alto/2)-83-(i*2),10-i,5,15-i*5,255,255,255)   
    time.sleep(tiempo)   
    pygame.display.flip()

for i in range (0,7):
    poligono((ancho/2)-50-(i*2),(alto/2)+80+(i*2),7-i,5,15-i*10,255,255,255)
    poligono((ancho/2)+65+(i*2),(alto/2)+75+(i*2),7-i,5,15-i*10,255,255,255)   
    time.sleep(tiempo)   
    pygame.display.flip()

loop()