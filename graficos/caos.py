# -*- coding: utf-8 -*-

import pygame
import random

class Pantalla:
    """
        Que influencio este trabajo?
        https://www.youtube.com/watch?v=fDSIRXmnVvk
    """
    def __init__(self, ancho=1500, alto=900):
        self.alto = alto
        self.ancho = ancho
        
        self.limites = {
            "arriba": 150,
            "derecha": 200,
            "abajo": -250,
            "izquierda": -200
        }
        
        self.screen = pygame.display.set_mode([self.ancho, self.alto])
        pygame.display.set_caption("Ecuaciones CAOTICAS XD")

    def loop(self):
        pygame.init()
        
        t = 0.001
        
        p1_c = [0.1,0.2,0.3]
        p1_p = self.mapear_coordenada_a_pixel(p1_c[1], p1_c[2])
        
        a = 10.0 
        b = 99.96
        c = 8/3
        
        p1_x = lambda x,y,z,t: x + t * (a * (y - x))
        p1_y = lambda x,y,z,t: y + t * (x * (b - z) - y)
        p1_z = lambda x,y,z,t: z + t * (x * y - c * z)
        
        i = 0
        salir = False
        while not salir:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir = True
            
            # self.estrellas()
            
            i += 1
            
            pygame.draw.line(self.screen , [255,255,(i) % 255], p1_p, p1_p)
            # t = t + salto
            
            p1_c = [
                    p1_x(p1_c[0], p1_c[1], p1_c[2], t),
                    p1_y(p1_c[0], p1_c[1], p1_c[2], t),
                    p1_z(p1_c[0], p1_c[1], p1_c[2], t)
                ]
            
            p1_p = self.mapear_coordenada_a_pixel(p1_c[1], p1_c[2])            
            
            pygame.display.flip()
            pygame.time.delay(1)
    
    def estrellas(self):
        color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        pos = [random.randint(0,self.ancho - 1), random.randint(0,self.alto - 1)]
        
        pygame.draw.line(self.screen , color, pos, pos)
    
    def mapear_pixel_a_coordenada(self, p_x, p_y):
        
        delta_x = (abs(self.limites["izquierda"]) + abs(self.limites["derecha"])) / (self.ancho - 1)
        delta_y = (abs(self.limites["arriba"]) + abs(self.limites["abajo"])) / (self.alto - 1)
        
        c_x = self.limites["izquierda"] + delta_x * p_x
        c_y = delta_y * p_y - self.limites["arriba"]
    
        return [int(c_x), int(c_y)]
        
    def mapear_coordenada_a_pixel(self, c_x, c_y):
        """
            x:
            cx = izq + dx*px
            cx - izq = dx*px
            (cx - izq) / dx = px
            =>
            px = (cx - izq) / dx
            
            y:
            cy = dy*py - arr
            cy + arr = dy*py
            (cy + arr) / dy = py
            =>
            py = (cy + arr) / dy
            
        """
        delta_x = (abs(self.limites["izquierda"]) + abs(self.limites["derecha"])) / (self.ancho - 1)
        delta_y = (abs(self.limites["arriba"]) + abs(self.limites["abajo"])) / (self.alto - 1)
        
        p_x = (c_x - self.limites["izquierda"]) / delta_x
        p_y = (c_y + self.limites["arriba"]) / delta_y
        
        return [p_x, p_y]
        
        
pantalla = Pantalla()
pantalla.loop()