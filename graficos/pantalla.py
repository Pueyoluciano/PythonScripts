# -*- coding: utf-8 -*-
import math
import pygame

class Pantalla:
    """
        Clase para aplicaciones con interfaz grafica.
        
    """
    def __init__(self,nombre="Pantalla Grafica", celda=1, ancho=400, alto=400, refresco=10, usar_grilla=False, *args, **kargs):
        self.nombre = nombre
        self.usar_grilla = usar_grilla
        
        if self.usar_grilla:
            self.celda = celda
            self.columnas = ancho
            self.filas = alto
        
        self.ancho = celda * ancho
        self.alto = celda * alto
        
        self.refresco = refresco
        
        self.args = args
        self.kargs = kargs

        self.setear_frontera(arriba=100, derecha=100, abajo=-100, izquierda=-100)
        
        self.setear_tamano()
        
        pygame.display.set_caption(self.nombre)

    def setear_tamano(self, ancho=None, alto=None):
        self.screen = pygame.display.set_mode([ancho if ancho else self.ancho, alto if alto else self.alto])
        
    def setear_frontera(self, arriba, derecha, abajo, izquierda):
        # El ratio es para compensar las dimensiones en pixeles que no sean 1:1
        ratio = self.ancho / self.alto
        
        self.limites = {
            "arriba": arriba,
            "derecha": derecha * ratio,
            "abajo": abajo,
            "izquierda": izquierda * ratio
        }

    def pre_loop(self, *args, **kargs):
        pass
        
    def post_loop(self, *args, **kargs):
        pass
        
    def accion_loop(self, *args, **kargs):
        pass
    
    def salir_loop(self, *args, **kargs):
        return False
        
    def loop(self, *args, **kargs):
        pygame.init()
        
        salir = False
        
        self.pre_loop(*args, **kargs)
        
        while not salir:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir = True
            
            self.accion_loop(*args, **kargs)
            
            pygame.display.flip()
            pygame.time.delay(self.refresco)
    
            salir = salir or self.salir_loop(*args, **kargs)
        self.post_loop(*args, **kargs)
    
    def capturar_imagen(self, archivo_salida=None):
        if not archivo_salida:
            archivo_salida = type(self).__name__ + "_captura_imagen.bmp"
            
        pygame.image.save(self.screen, archivo_salida)
    
    def pintar_grilla(self):
        if self.usar_grilla:
            delta_x = self.ancho / self.columnas
            delta_y = self.alto / self.filas
        
        
            for i in range(0, self.columnas + 1):
                self.pintar_linea((delta_x * i, 0), (delta_x * i, self.alto - 1), self.color_grilla)

            for i in range(0, self.filas + 1):
                self.pintar_linea((0, delta_y * i), (self.ancho - 1, delta_y * i), self.color_grilla)
                
        else:
            raise Exception("La grilla no está activada")
        
    def pintar_rectangulo(self, p, alto, ancho, borde, grosor, color_relleno=None, color_borde=None):
        # La version 1.9.6 de pygame no tiene border radius...
        # pygame.draw.rect(self.screen , color, (pi[0],pi[1], pi[0] + pf[0], pi[1] + pf[1]), grosor, borde)
        color_relleno and pygame.draw.rect(self.screen , color_relleno, (p[0],p[1], ancho, alto), 0)
        color_borde and pygame.draw.rect(self.screen , color_borde, (p[0],p[1], ancho, alto), grosor)
    
    def pintar_rectangulo_magnetico(self, columna_origen, fila_origen, ancho, alto, borde, grosor, color_relleno=None, color_borde=None):
        if self.usar_grilla:
            delta_x = self.ancho / self.columnas
            delta_y = self.alto / self.filas
            
            izq = columna_origen * delta_x
            arriba = fila_origen * delta_y
            ancho_ = ancho * delta_x
            alto_ = alto * delta_y
            
            self.pintar_rectangulo((izq, arriba), ancho_, alto_, borde, grosor, color_relleno, color_borde)
            
        else:
            raise Exception("La grilla no está activada")
        
    def pintar_linea(self, pi, pf, color):
        pygame.draw.line(self.screen , color, pi, pf)
    
    def pintar_pixel(self, p, color):
        self.pintar_linea(p, p, color)
        
    def pintar_coordenada(self, cx, cy, color):
        p = self.mapear_coordenada_a_pixel(cx,cy)
        pygame.draw.line(self.screen , color, p, p)
    
    def mapear_pixel_a_coordenada(self, p_x, p_y):
        
        delta_x = (abs(self.limites["izquierda"]) + abs(self.limites["derecha"])) / (self.ancho - 1)
        delta_y = (abs(self.limites["arriba"]) + abs(self.limites["abajo"])) / (self.alto - 1)
        
        c_x = self.limites["izquierda"] + delta_x * p_x
        c_y = delta_y * p_y - self.limites["arriba"]
    
        return [c_x, c_y]
        
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