# -*- coding: utf-8 -*-
import math
import pygame

class Pantalla:
    """
        Clase para aplicaciones con interfaz grafica.
        
    """
    def __init__(self,nombre="Pantalla Grafica", ancho=400, alto=400, refresco=10, *args, **kargs):
        self.nombre = nombre
        
        self.alto = alto
        self.ancho = ancho
        
        self.refresco = refresco
        
        # El ratio es para compensar las dimensiones en pixeles que no sean 1:1
        ratio = self.ancho / self.alto
        
        self.limites = {
            "arriba": 100,
            "derecha": 100 * ratio,
            "abajo": -100,
            "izquierda": -100 * ratio
        }
        
        self.screen = pygame.display.set_mode([self.ancho, self.alto])
        pygame.display.set_caption(self.nombre)
        
        self.iniciar(*args, **kargs)

    def iniciar(self, *args, **kargs):
        pass
        
    def pre_loop(self):
        pass
        
    def post_loop(self):
        pass
        
    def accion_loop(self):
        pass
    
    def salir_loop(self):
        return False
        
        
    def loop(self):
        pygame.init()
        
        salir = False
        
        self.pre_loop()
        
        while not salir:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir = True
            
            self.accion_loop()
            
            pygame.display.flip()
            pygame.time.delay(self.refresco)
    
            salir = salir or self.salir_loop()
        self.post_loop()
    
    def capturar_imagen(self, archivo_salida=None):
        if not archivo_salida:
            archivo_salida = type(self).__name__ + "_captura_imagen.bmp"
            
        pygame.image.save(self.screen, archivo_salida)
        
        
    def pintar_pixel(self, p, color):
        pygame.draw.line(self.screen , color, p, p)
        
    def pintar_coordenada(self, cx, cy, color):
        p = self.mapear_coordenada_a_pixel(cx,cy)
        pygame.draw.line(self.screen , color, p, p)
    
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