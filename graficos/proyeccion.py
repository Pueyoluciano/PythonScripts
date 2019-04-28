# -*- coding: utf-8 -*-
import math

class Matriz:
    """
        https://stackoverflow.com/questions/43849117/projecting-3d-model-onto-2d-plane
        
        https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/mathematics-computing-2d-coordinates-of-3d-points
    """
    def __init__(self, filas, columnas):
        self.cuerpo = [[0 for _ in range(0,columnas)] for _ in range(0,filas)]
        self.filas = filas
        self.columnas = columnas
    
    def __copy__(self, a):
        return type(self)(a.filas, a.columnas)
    
    def __add__(self, a):
        """
            OJO que pre(a.columnas == b.columnas && a.filas == b.filas )
        """
        if self.columnas == a.columnas and self.filas == a.filas:
            retorno = Matriz(self.filas, self.columnas)           
            
            for y in range(0,self.filas):
                for x in range(0, self.columnas):
                    retorno[y][x] = self[y][x] + a[y][x]
                
            
            return retorno
        
        else:
            raise TypeError("Las matrices tienen dimensiones diferentes")
    
    def __getitem__(self, index):
        return self.cuerpo[index]
    
    def __mul__(self, a):
        """
            OJO que pre(self.columnas == a.filas)
        """
                    
        if self.columnas == a.columnas and self.filas == a.filas:
            retorno = Matriz(self.filas, self.columnas)           
                
            for y in range(0, retorno.filas):
                for x in range(0, retorno.columnas):
                
                    for i in range(0, retorno.filas):
                        retorno[y][x] += self[y][i] * a[i][x]

            return retorno
        
        else:
            raise TypeError("Las matrices tienen dimensiones diferentes")

    def esCuadrada(self):
        return self.filas == self.columnas
    
    def _det1x1(self):
        if self.esCuadrada():
            return self[0][0]
        
        else:
            raise TypeError("La matriz no es cuadrada")
        
    def _det2x2(self):
        if self.esCuadrada():
            a = self[0][0] * self[1][1] * self[2][2]
            b = self[0][1] * self[1][2] * self[2][0]
            c = self[0][2] * self[1][0] * self[2][1]
            
            d = self[2][0] * self[1][1] * self[0][2]
            e = self[2][1] * self[1][2] * self[0][0]
            f = self[2][2] * self[1][0] * self[0][1]
       
            return a + b + c - ( d + e + f ) 
        
        else:
            raise TypeError("La matriz no es cuadrada") 
    
    def _det3x3(self):
        if self.esCuadrada():
            return self[0][0]* self[1][1] - self[0][1] * self[1][0]
        
        else:
            raise TypeError("La matriz no es cuadrada") 
    
    def determinante(self):
        if self.filas > 3:
            return -1
    
        if self.filas == 3:
            return self._det3x3()
    
        if self.filas == 2:
            return self._det2x2()
    
        if self.filas == 1:
            return self._det1x1()
            
        return 1
        
    def esInvertible(self):
        return True
        
    def inversa(self):
        
        if self.esInveritble():
            retorno = self.__copy__(self)
            
        else:
            raise TypeError("La matriz no es invertible")
        
    def invertir(self):
        pass
        
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        return str(self.cuerpo)
        
        
a = Matriz(3,3)
b = Matriz(3,3)

i = 1
for y in range(0, a.filas):
    for x in range(0, a.columnas):
        a[y][x] = i
        
        i += 1

for y in range(0, b.filas):
    for x in range(0, b.columnas):
        if y == x:
            b[y][x] = 1

print(a)
print(a * b)
print(a.determinante())
print(b.determinante())
print((a*b).determinante())

