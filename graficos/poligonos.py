# -*- coding: utf-8 -*-

import pygame
import random
import math


class Pantalla:
    def __init__(self, ancho=800, alto=800):
        self.alto = alto
        self.ancho = ancho
        
        self.screen = pygame.display.set_mode([self.ancho, self.alto])
        pygame.display.set_caption("POLI POLIGONOS")

    def loop(self):
        pygame.init()
        
        i = 3
        
        salir = False
        while not salir:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir = True
            
            
                self.poligono(self.ancho/2, self.alto/2, 100, i, 0, 255, (i*10) % 255, i % 255)
            
                i+=1
                
            pygame.display.flip()
            pygame.time.delay(100)
            
            
    def poligono(self, x, y, amp, lados, des, rojo, verde, azul):   
        ang = 360/lados   
        ang2 = 0   
        for i in range(0,lados):
            seno = amp*(math.sin(((ang2+des) * math.pi)/180))
            coseno = amp*(math.cos(((ang2+des)* math.pi)/180))       
            senosig = amp*(math.sin(((ang2+ang+des) * math.pi)/180))
            cosenosig = amp*(math.cos(((ang2+ang+des) * math.pi)/180))        
            pygame.draw.aaline(self.screen, (rojo,verde,azul), (x+coseno,y+seno), (x+cosenosig,y+senosig))       
            ang2 = ang2 + ang
            
            
            
pantalla = Pantalla()

pantalla.loop()