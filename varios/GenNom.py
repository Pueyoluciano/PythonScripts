"""
    GenNom V.1.0.0
    
    Generador de Nombres.
"""
import random

vocales = set('aeiou')
consonantes = set('bcdfghjklmnñpqrstvwxyz')

class Reglas:
    
    def __init__(self):
        pass
    
    @classmethod
    def es_consonante(cls, letra):
        return letra in consonantes
    
    @classmethod
    def es_vocal(cls, letra):
        return letra in vocales
    
    @classmethod
    def q_siempre_con_u(cls, nombre, abc):
        if len(nombre) > 0 and nombre[-1].lower() == 'q':
            return {'u'}
            
        return abc

    @classmethod
    def qu_siempre_con_vocal(cls, nombre, abc):
        if len(nombre) >= 2 and nombre[-2:].lower() == 'qu':
            return vocales - abc
        
        return abc
        
    @classmethod
    def dos_consonantes_maximo(cls, nombre, abc):
        if len(nombre) >= 2 and cls.es_consonante(nombre[-1]) and cls.es_consonante(nombre[-2]):
            return vocales - abc
            
        return abc
    
    @classmethod
    def tres_vocales_maximo(cls, nombre, abc):
        if len(nombre) >= 3 and cls.es_vocal(nombre[-3]) and cls.es_vocal(nombre[-2]) and cls.es_vocal(nombre[-1]):
            return consonantes - abc
            
        return abc
            

class Distribucion:
    def __init__(self):
        self.valores = {
            'a': 12.53,
            'b': 1.42,
            'c': 4.68,
            'd': 5.86,
            'e': 13.68,
            'f': 0.69,
            'g': 1.01,
            'h': 0.70,
            'i': 6.25,
            'j': 0.44,
            'k': 0.02,
            'l': 4.97,
            'm': 3.15,
            'n': 6.71,
            'ñ': 0.31,
            'o': 8.68,
            'p': 2.51,
            'q': 0.88,
            'r': 6.87,
            's': 7.98,
            't': 4.63,
            'u': 3.93,
            'v': 0.90,
            'w': 0.01,
            'x': 0.22,
            'y': 0.90,
            'z': 0.52         
        }

    def elegir(self, abc=None):
        """
            abc: parametro opcional que son las letras elegibles.
                Si viene vacio se usa el abcdario completo.
                Si es no vacio debe ser un conjunto con las letras elegibles.
                
            Para elegir una letra se pasan a entero los porcentajes
            de distribucion de cada letra. Como son numeros con 2 cifras decimales,
            podemos multiplicar por 100 y siempre obtenemos un entero ( con parte decimal = 0).
            
            Se asigna un rango a cada letra, que parte donde termina el rango anterior (o 0 si
            es la primer letra).
            
            Luego se toma un entero al azar y se busca en que rango se encuentra contenido,
            como son rangos disjuntos y el numero al azar se toma entre 0 y la suma total de rangos - 1
            siempre se obtiene una letra.
            
            por ejemplo:
            
                a: 50.31
                b: 20.13 
                c: 29,56
                
            1 - se pasan a entero:
            
                a: 5031
                b: 2013
                c: 2956
                
            2 - se arman los rangos:
            
                {
                    'a': [0, 5030],
                    'b': [5031, 7043],
                    'c': [7044, 9999]
                }
                
                * el total es 10000
                
            3 - se toma un numero al azar entre 0 y 9999
            
            4 - por ultimo se busca que rango contiene a este numero.
        """    
        muestras = {}
        marcador = 0
        
        for letra, porcentaje in self.valores.items():
            if not abc or letra in abc:
                porcentaje_int = int(porcentaje * 100)
                muestras[letra] = range(marcador, marcador + porcentaje_int)
                marcador += porcentaje_int
            
        muestra = random.randint(0, marcador - 1)
        
        for clave, rango in muestras.items():
            if muestra in rango:
                return clave
        
    def testear(self):
        contador = { letra:0 for letra in vocales | consonantes}

        for i in range(10000):
            contador[self.elegir()] += 1
            
        print(contador)
        
        
class GenNom:
    abcdario = vocales | consonantes 
    # set('abcdefghijklmnñopqrstuvwxyz')
       
    def __init__(self, longitud=5):
        self.longitud = longitud
        self.reglas = [
                        Reglas.q_siempre_con_u,
                        Reglas.dos_consonantes_maximo,
                        Reglas.tres_vocales_maximo,
                        Reglas.qu_siempre_con_vocal
                    ]
                    
        self.modos_eleccion_caracter = {
                                        'ponderado': self.elegir_ponderado, 
                                        'aleatorio': self.elegir_aleatorio
                                    }
                                    
        self.modo_eleccion_seleccionado = 'ponderado'
    
        self.distribucion = [
        
        ]
    
    def generar(self, longitud=None):
        nombre = ''
        
        if not longitud:
            longitud = self.longitud
            
        for i in range(0, longitud):
            nombre += self.nuevo_caracter(nombre)
            
        return nombre
        
    def nuevo_caracter(self, nombre):
        abc = self.abcdario.copy()
        
        for regla in self.reglas:
            abc = abc.intersection(regla(nombre, abc))
        
        return self.elegir_caracter(abc)
        
    def elegir_caracter(self, abc):
        return str(self.modos_eleccion_caracter[self.modo_eleccion_seleccionado](abc)[0])
    
    def elegir_aleatorio(self, abc):
        return random.sample(abc, 1)
        
    def elegir_ponderado(self, abc):
        dis = Distribucion()
        return dis.elegir(abc)
        
        
if __name__ == '__main__':
    gn = GenNom(5)
    
    for i in range(0, 10):
        print(gn.generar(5), gn.generar(3), gn.generar(4))
