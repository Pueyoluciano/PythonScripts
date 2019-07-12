# -*- coding: utf-8 -*-
import math
import random

import Pantalla

class Fractales(Pantalla.Pantalla):
    def iniciar(self, *args, **kargs):
        self.setear_frontera(3,3,-3,-3)

    def pre_loop(self):
        self.x = 0
        self.y = 0
        
        self.frac = Fractal(Mandelbrot, 35, 10)
        
    def accion_loop(self):
        punto = self.mapear_pixel_a_coordenada(self.x, self.y)
        c = complex(*punto)
        
        resultado = self.frac.evaluar(c)
        
        color = [(255 / 35) * resultado, (255 / 35) * resultado, (255 / 35) * resultado]
    
        self.pintar_pixel([self.x, self.y], color)
        
        self.x += 1
        if self.x == self.ancho:
            self.x = 0
            self.y += 1 
            
            if self.y == self.alto:
                self.y = 0
    
    
def Mandelbrot(zn, c, **kargs):
    return zn**2 + c
    
class Fractal:
    def __init__(self, funcion, resolucion, limite_divergencia):
        self.funcion = funcion
        self.resolucion = resolucion
        self.limite_divergencia = limite_divergencia
    
    
    def evaluar(self, c, **kargs):
        zn = 0
    
        for i in range(0, self.resolucion):
            zn = self.funcion(zn, c, **kargs)
            
            if abs(zn) > self.limite_divergencia:
                break
                
        return i
    
f = Fractales(alto=400, ancho=400,refresco=1)

f.loop()