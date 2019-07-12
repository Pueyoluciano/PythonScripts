        
def rotar(lista, pasos=1):
    for _ in range(0, pasos):
        lista.insert(0, lista.pop())

def ritmo_euclideo(pulsos, ritmo, rotaciones):
    """
        Un ritmo euclideo es una lista de 1s y 0s.
        Nn 1 significa un golpe, una nota, etc. y un 0 un silencio.
        1 y 0 tienen la misma duracion (negras, corcheas, etc).
        
        Para generar un ritmo euclideo existen muchos algoritmos,
        este en particular lo hace de una forma "humana", no demasiado rebuscada,
        Seguramente existen verisones mucho mas optimas.
        
        A la cantidad total de figuras (1s o 0s) lo llamamos Ritmo.
        A los 1s los llamamos Pulsos.
        a los 0s los llamamos Silencios.
        
        La idea general es repartir "equitativamente" los Silencios entre todos los Pulsos dentro del Ritmo.
        
        Si por ejemplo tenemos:
            pulsos = 4
            ritmo = 8
            
        estamos tratando con un total de 8 figuras (1s y 0s), de las cuales 4 son pulsos (1s).
        Si lo graficaramos, tendremos algo como esto:
        
            11110000
        
        el ritmo euclideo (4,8) ser ve de la siguiente forma:
            
            => 10101010 
        
        Podemos validar entonces que cada Pulso recibió la misma cantindad de Silencios. Para esto basta mirar
        cuantos Silencios hay a la derecha de cada Pulso.
        
        el ritmo euclideo (5, 8) por ejemplo:
            11111000
            
            => 10101011
            
        Como este caso no tenemos suficientes Silencios para todos los Pulsos,
         los primeros Pulsos tendran un Silencio, y los 2 ultimos restantes no.    
    """
    
    #Creo una lista para contar los silencios asociados a cada pulso.
    silencios_por_pulso = [0 for _ in range(0, pulsos)]
        
    silencios = ritmo - pulsos
    
    indice = 0
    while silencios > 0:
        silencios_por_pulso[indice] += 1
        
        silencios -= 1
        indice = (indice + 1) % pulsos
        
    # Cuando tengo los ceros repartidos, armo la lista de 0s y 1s.
    ritmoEuclideo = []
    
    for x in silencios_por_pulso:
        ritmoEuclideo.append(1)
        
        for _ in range(0, x):
            ritmoEuclideo.append(0)

    
    rotar(ritmoEuclideo, rotaciones)
    
    return ritmoEuclideo


class Modulo:
    def __init__(self, pulsos, ritmo, rotaciones=0):
        self.crear_patron(pulsos, ritmo, rotaciones)

    def crear_patron(self, pulsos, ritmo, rotaciones):
        self.pulsos = pulsos
        self.ritmo = ritmo
        self.rotaciones = rotaciones
        
        self.patron = ritmo_euclideo(pulsos, ritmo, rotaciones)
        self._indice = 0
    
    def __iter__(self):
        self._indice = 0
        return self
    
    def actual(self):
        return self.patron[self._indice]
    
    def __next__(self):
        retorno = self.patron[self._indice]
        
        self._indice = (self._indice + 1) % len(self.patron)
        
        print(retorno)
        return retorno
      
    def __str__(self):
        return str(self.patron)

class DrumExMachina:
    def __init__(self, *modulos):
        self.modulos = modulos
    
    def __iter__(self):
        return self
        
    def __next__(self):
        for modulo in self.modulos:
            next(modulo)
            
        return self
        
    def __str__(self):
        retorno = ""
        for modulo in self.modulos:
            retorno +=str(modulo) + '\n'
            
        return retorno
        
a = Modulo(5,8)
b = Modulo(3,7)

c = DrumExMachina(a,b)