# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, '../../graficos')

import Pantalla

class DrumExVisual(Pantalla.Pantalla):
    def __init__(self, *args, **kargs):
        super(DrumExVisual, self).__init__(*args, **kargs)
        
        self.mostrar_grilla = True
        self.color_grilla = [255, 0, 0]
        
        self.celda = 60
        self.columnas = 5
        self.filas = 5
        
        self.ancho = self.celda * self.columnas
        self.alto = self.celda * self.filas
        
        self.setear_tamano()
        
    def pre_loop(self, *args, **kargs):
        self.pintar_grilla()
        
        self.pintar_rectangulo_magnetico(0,0,3,3,5,2,[255,255,0], [255,255,255])
        self.pintar_rectangulo_magnetico(0,0,2,2,5,2,[255,0,255], [255,255,255])
        self.pintar_rectangulo_magnetico(0,0,1,1,5,2,[0,255,255], [255,255,255])
        
        self.pintar_rectangulo_magnetico(2,2,2,2,5,2,[255,0,0])


DEV = DrumExVisual(nombre="Drum Ex Visual",celda=60, ancho=5, alto=5, refresco=10, usar_grilla=True)
DEV.loop()