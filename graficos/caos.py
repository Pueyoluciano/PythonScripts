# -*- coding: utf-8 -*-
import random
import Pantalla

class PantallaCaos(Pantalla.Pantalla):
    """
        Que influencio este trabajo?
        https://www.youtube.com/watch?v=fDSIRXmnVvk
    """
    def pre_loop(self):
        self.limites = {
            "arriba": 150,
            "derecha": 200,
            "abajo": -250,
            "izquierda": -200
        }
        
        self.t = 0.001
        
        self.p1_c = [0.1,0.2,0.3]
        
        a = 10.0 
        b = 99.96
        c = 8/3
        
        self.p1_x = lambda x,y,z,t: x + t * (a * (y - x))
        self.p1_y = lambda x,y,z,t: y + t * (x * (b - z) - y)
        self.p1_z = lambda x,y,z,t: z + t * (x * y - c * z)
        
        self.i = 0

    def accion_loop(self):
    
        self.i += 1
        
        self.pintar_coordenada(self.p1_c[1], self.p1_c[2], [255,255,(self.i) % 255])

        # t = t + salto
        
        self.p1_c = [
                self.p1_x(self.p1_c[0], self.p1_c[1], self.p1_c[2], self.t),
                self.p1_y(self.p1_c[0], self.p1_c[1], self.p1_c[2], self.t),
                self.p1_z(self.p1_c[0], self.p1_c[1], self.p1_c[2], self.t)
            ]
        
    def estrellas(self):
        color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        pos = [random.randint(0,self.ancho - 1), random.randint(0,self.alto - 1)]
        
        pygame.draw.line(self.screen , color, pos, pos)
    
        
pantalla = PantallaCaos("Ecuaciones CAOTICAS XD", ancho=800, alto=800, refresco=1)
pantalla.loop()