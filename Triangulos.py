import pygame
import random
from validador import *

pygame.init()

screen = pygame.display.set_mode((150,150))
pxarray = pygame.PixelArray(screen)
pygame.display.set_caption("triangulos")

alto = 4
ancho = 4

salir = False
saltoi = 150.0/alto
saltoj = 150.0/ancho

while not salir:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir = True

        for i in range(0,alto-1,2):
            for j in range(0,ancho-1,2):
                pygame.draw.polygon(screen, [random.randint(0,255),random.randint(0,255),random.randint(0,255)],[[i*saltoi,j*saltoj],[i*saltoi,(j+2)*saltoj],[(i+1)*saltoi,(j+1)*saltoj]])
                pygame.draw.polygon(screen, [random.randint(0,255),random.randint(0,255),random.randint(0,255)],[[(i+2)*saltoi,j*saltoj],[i*saltoi,j*saltoj],[(i+1)*saltoi,(j+1)*saltoj]])
                pygame.draw.polygon(screen, [random.randint(0,255),random.randint(0,255),random.randint(0,255)],[[i*saltoi,(j+2)*saltoj],[(i+2)*saltoi,(j+2)*saltoj],[(i+1)*saltoi,(j+1)*saltoj]])
                pygame.draw.polygon(screen, [random.randint(0,255),random.randint(0,255),random.randint(0,255)],[[(i+2)*saltoi,(j+2)*saltoj],[(i+2)*saltoi,(j)*saltoj],[(i+1)*saltoi,(j+1)*saltoj]])
                
    
    # pxarray[random.randint(0,149),random.randint(0,149)] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    pygame.display.flip()