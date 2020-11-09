# -*- coding: utf-8 -*-
import math
import random

import Pantalla

class color_iterador:
    def __iter__(self):
        self.color = 0
        return self
        
    def __next__(self):
        self.color = self.color + 10 if self.color + 10 < 255 else 0
        
        return [255, 255, 255]

class PantallaAutomata(Pantalla.Pantalla):

    def to_bin(self, decimal, digitos):
        return str(bin(decimal)[2:].zfill(digitos))
        
    def __init__(self, *args, **kargs):
        super(PantallaAutomata, self).__init__(*args, **kargs)
        
        self.color_pixel = iter(color_iterador())

        self.vecindad = kargs["vecindad"]
        
        if "reglas" in kargs.keys():
            if type(kargs["reglas"]) is int:
                # reglas = self.to_bin(kargs["reglas"], 8)
                reglas = self.to_bin(kargs["reglas"], 2**len(self.vecindad))
            
            else:
                reglas = kargs["reglas"]
        else:
            reglas = "10000101"
           
        self.reglas = {}

        for i in range(0, 2**len(self.vecindad)):
            indice = self.to_bin(i, len(self.vecindad))
            
            self.reglas[indice] = int(reglas[2**len(self.vecindad) - 1 - i])
           
           
        # self.reglas = {
            # '00000': int(reglas[31]),
            # '00001': int(reglas[30]),
            # '00010': int(reglas[29]),
            # '00011': int(reglas[28]),
            # '00100': int(reglas[27]),
            # '00101': int(reglas[26]),
            # '00110': int(reglas[25]),
            # '00111': int(reglas[24]),
            # '01000': int(reglas[23]),
            # '01001': int(reglas[22]),
            # '01010': int(reglas[21]),
            # '01011': int(reglas[20]),
            # '01100': int(reglas[19]),
            # '01101': int(reglas[18]),
            # '01110': int(reglas[17]),
            # '01111': int(reglas[16]),
            # '10000': int(reglas[15]),
            # '10001': int(reglas[14]),
            # '10010': int(reglas[13]),
            # '10011': int(reglas[12]),
            # '10100': int(reglas[11]),
            # '10101': int(reglas[10]),
            # '10110': int(reglas[9]),
            # '10111': int(reglas[8]),
            # '11000': int(reglas[7]),
            # '11001': int(reglas[6]),
            # '11010': int(reglas[5]),
            # '11011': int(reglas[4]),
            # '11100': int(reglas[3]),
            # '11101': int(reglas[2]),
            # '11110': int(reglas[1]),
            # '11111': int(reglas[0])
        # }            
        
        # self.reglas = {
            # "000": int(reglas[7]),
            # "001": int(reglas[6]),
            # "010": int(reglas[5]),
            # "011": int(reglas[4]),
            # "100": int(reglas[3]),
            # "101": int(reglas[2]),
            # "110": int(reglas[1]),
            # "111": int(reglas[0]),
        # }
    
        self.limites = {
            "arriba": 0,
            "derecha": self.ancho,
            "abajo": self.alto,
            "izquierda": 0
        }
        
        self.auto = Automata(self.ancho, self.vecindad, self.reglas)
        
    def accion_loop(self):
        for i in range(0, self.auto.dimension):
            
            if self.auto.grilla[i]:
                self.pintar_pixel([i, self.auto.pasos], next(self.color_pixel))
    
        if self.auto.pasos < self.alto:
            self.auto.iterar()
            # print(self.auto.pasos)
    
    def post_loop(self):
        self.capturar_imagen()
        
    # def salir_loop(self):
        # return self.auto.pasos >= self.alto
    
class Automata:
    def __init__(self, dimension, vecindad, reglas):

        self.dimension = dimension
        self.vecindad = vecindad
        self.reglas = reglas
        
        self.pasos = 0
        
        self.grilla = [0 for _ in range(0, self.dimension)]

        self.grilla[int(self.dimension / 2)] = 1

    def iterar(self):
        grilla_sig = [0 for _ in range(0, self.dimension)]
    
        
        for i in range(0, self.dimension):
            indice=""
            for vecino in self.vecindad:
                if i + vecino < 0 or i + vecino > self.dimension - 1:
                    indice += "0"
                    
                else:
                    indice += str(self.grilla[i+vecino])
            
            # izq = str(self.grilla[i-1] if i > 0 else 0)
            # cen = str(self.grilla[i])
            # der = str(self.grilla[i+1] if i < self.dimension-1 else 0)
            
            # indice = izq + cen + der
    
            grilla_sig[i] = self.reglas[indice]
        
        self.pasos += 1
        
        self.grilla = grilla_sig
        return grilla_sig
        
p = PantallaAutomata(
        # "Automatones Celularoides Xd1!",
        'Automatas celulares',
        ancho=1150,
        alto=800,
        refresco=1,
        usar_grilla=False,
        vecindad=[-1,0,1],
        reglas=150
    )

# - vecindad=[-2,-1,0,1,2], reglas=32130

# p.auto.grilla[0] = 1
# p.auto.grilla[1] = 1
# p.auto.grilla[2] = 1
# p.auto.grilla[int(p.ancho*1/8)] = 1
# p.auto.grilla[int(p.ancho*1/8) + 1] = 1
# p.auto.grilla[int(p.ancho*2/8)] = 1
# p.auto.grilla[int(p.ancho*3/8)] = 1
# p.auto.grilla[int(p.ancho*4/8)] = 1
# p.auto.grilla[int(p.ancho*5/8)] = 1
# p.auto.grilla[int(p.ancho*6/8)] = 1
# p.auto.grilla[int(p.ancho*7/8)] = 1

p.loop()