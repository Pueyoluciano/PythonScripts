# -*- coding: utf-8 -*-
import math
# import pygame
import random
import Pantalla

class PantallaCirculo(Pantalla.Pantalla):
    def pre_loop(self):
        self.x = 0
        self.y = 0
        
        self.ang = 0
        self.amp = 1
        
    def accion_loop(self):
        self.pintar_coordenada(self.x, self.y, [self.ang % 255, self.ang % 255, 255])
        
        self.x += ((self.amp + self.ang)/360) * ( (self.ang/50) % 15) * math.sin(self.ang)
        self.y += ((self.amp + self.ang)/360) * ( (self.ang/50) % 15) * math.cos(self.ang)
            
        self.ang += 1
        

pantalla = PantallaCirculo(ancho=600, alto=600, refresco=1)
pantalla.loop()
