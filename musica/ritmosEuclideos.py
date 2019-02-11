import itertools
import time

class Euclideo:
    def __init__(self, pulsos, ritmo):
        self.posicion = 0
        
        # Pongo algunas validaciones para que no rompa la funcion
        self.pulsos = abs(pulsos)
        self.ritmo = abs(ritmo)
        
        if self.pulsos > self.ritmo:
            self.pulsos = self.ritmo
        
        # Armo una lista parcial con "cajas".
        # Cada caja es un pulso.
        # Cada caja cuenta los ceros que le suceden.
        
        resultado_parcial = [0 for _ in range(0,self.pulsos)]
        
        huecos = self.ritmo - self.pulsos
        
        indice = 0
        while huecos > 0:
            resultado_parcial[indice] += 1
            
            huecos -= 1
            indice = (indice + 1) % self.pulsos        
        
        # Cuando tengo los ceros repartidos, armo una lista de 0s y 1s.
        self.ritmo = []
        for x in resultado_parcial:
            self.ritmo.append(1)
            
            for _ in range(0, x):
                self.ritmo.append(0)
    
        self._generarCiclo()
        
    def _generarCiclo(self):
        self.ciclo = itertools.cycle(self.ritmo)
    
    def rotar(self, pasos=1):
        for _ in range(0, pasos):
            self.ritmo.insert(0, self.ritmo.pop())
        
        self._generarCiclo()
    
    def __next__(self):
        return next(self.ciclo)
    
    def __str__(self):
        return str(self.ritmo)