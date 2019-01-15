from functools import *

class Musica:
    """
        Clase Abastracta con varios conceptos recurrentes para la generacion de escalas y acordes.
        
        notacion: mostrar las notas en sostenidos o bemoles.
        notas: diccionario con la escala cromatica, una entrada esta escrita en
               notacion de sostenidos y la otra en notacion de bemoles.
                
        modos: defiene los intervalos que dan forma a las escalas.
        
        escalas: define escalas tomando los grados en funcion de otra escala, en
                 vez de hacerlo con intervalos en funcion de la escala cromatica.
        
        acordes: diccionario de acordes definidos como una lista de grados(tomados del modo mayor)
        
        progresion: define el tipo de acorde para cada grado de una escala.
    """
    notacion = ['sostenidos', 'bemoles']

    _cromaticoSostenidos = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    _cromaticoBemoles = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Cb']

    notas = {
        notacion[0]: _cromaticoSostenidos,
        notacion[1]: _cromaticoBemoles
    }

    #2 = tono
    #1 = semi-tono
    modos = {
        'mayor': [2, 2, 1, 2, 2, 2, 1],
        'menor': [2, 1, 2, 2, 1, 2, 2],
        'pentatonica mayor': [2, 2, 3, 2, 3],
        'pentatonica menor': [3, 2, 2, 3, 2]
    }
    
    escalas = {
        'cromatica': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'pentatonica mayor': [1, 2, 3, 5, 6],
        'pentatonica menor': [1, '3b', 4, 5, '7b']
    }
    
    acordes = {
        'mayor': [1, 3, 5],
        'maj7': [1, 3, 5, 7],
        'maj11': [1, 3, 5, 7, 11],
        'menor': [1,'3b',5],
        'min7': [1,'3b', 5, '7b'],
        'min11': [1,'3b', 5, '7b', 11],
        'aumentado': [1, 3,'5#'],
        'disminuido': [1, '3b', '5b'],
        'sus2': [1, 2, 5],
        'sus4': [1, 4, 5]
    }
    
    progresion = {
        'mayor': ['mayor', 'menor', 'menor', 'mayor', 'mayor', 'menor', 'disminuido'],
        'menor': ['menor', 'disminuido', 'mayor', 'menor', 'menor', 'mayor', 'mayor']
    }
    
    @classmethod
    def disminuir(cls, nota, notacion="sostenidos"):
        indice = cls.notas[notacion].index(nota)
        return cls.notas[notacion][(indice - 1) % 11]
        
    @classmethod
    def aumentar(cls, nota, notacion="sostenidos"):
        indice = cls.notas[notacion].index(nota)
        return cls.notas[notacion][(indice + 1) % 11]

    
class Secuencia:
    def __init__(self, modo, tonica, notacion=Musica.notacion[0]):
        """
            Clase padre. Cualuier sucesion de notas comparten estos conceptos.
            
            modo: las clases hija definen un sentido distinto para este atributo.
            |-> Escala.modo: nombre identificatorio de la sucesion de notas que forman una escala.
            |
            |-> Acorde.modo: escala de base a partir de la cual se toman los grados que forman el acorde.
            
            tonica: nota raiz de la cual devienen todas las notas siguientes.
            notacion: mostrar las notas en sostenidos o bemoles.
            
            notas: lista con las notas generadas.
        """
        
        self.tipo = "Secuencia"
        self.modo = modo
        self.tonica = tonica
        self.notacion = notacion
        self.notas = []
    
    def __len__(self):
        return len(self.notas)
        
    def texto(self):
        return self.tipo + " " + str(self.modo) + " de " + str(self.tonica) + ": "
    
    def __str__(self):
        return  self.texto() + reduce(lambda x, y :x + " - " + y,  self.notas)
  

class Escala(Secuencia):
    def __init__(self, modo, tonica, notacion=Musica.notacion[0]):
        """
            modo: debe ser una entrada en el diccionario de Musica.modos. (lista de intervalos que definen la escala).
            tonica: tonica de la escala.
            notacion: mostrar las notas en sostenidos o bemoles.
        """
        super().__init__(modo, tonica, notacion)
        self.tipo = "Escala"
        
        desplazamiento = 0
        inicio = Musica.notas[notacion].index(tonica)
        
        for i in Musica.modos[modo]:
            self.notas.append(Musica.notas[notacion][(inicio + desplazamiento) % 12])
            desplazamiento += i

    
class Acorde(Secuencia):
    def __init__(self, nombre, tonica, notacion=Musica.notacion[0], modo='mayor'):
        """
            nombre: nombre del acorde (debe ser una entrada en el diccionario de Musica.acordes.
            
            modo: escala de la cual se toman los grados. Por defecto se usa el modo Mayor.
            
            tonica: tonica del acorde.
            
            notacion: mostrar las notas en sostenidos o bemoles.
            
            base: Escala de base.
        """
        
        super().__init__(modo, tonica, notacion)
        self.tipo = "Acorde"
        self.nombre = nombre
        
        self.base = Escala(modo, tonica, notacion)
        
        for grado in Musica.acordes[nombre]:
            if type(grado) is int:
                indice = grado - 1
                nota = self.base.notas[indice % len(self.base)]

            else:
                indice = (int(grado[0]) - 1) 
                if grado[1] == 'b':
                    #Disminuido
                    nota = Musica.disminuir(self.base.notas[indice % len(self.base)])
                    
                else:
                    #Aumentado
                    nota = Musica.aumentar(self.base.notas[indice % len(self.base)])
                    
            self.notas.append(nota)

    def texto(self):
        return self.tipo + " " + str(self.tonica) + " " + str(self.nombre) + ": "
        
        
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")

print("Escalas Mayores: ")

for tonica in Musica.notas['sostenidos']:
    print(Escala('mayor', tonica, 'sostenidos'))

    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")

print("Escalas Menores: ")

for tonica in Musica.notas['sostenidos']:
    print(Escala('mayor', tonica, 'sostenidos'))

    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")

print("Pentatonicas Mayores: ")

for tonica in Musica.notas['sostenidos']:
    print(Escala('pentatonica mayor', tonica, 'sostenidos'))

    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")

print("Pentatonicas Menores: ")    
for tonica in Musica.notas['sostenidos']:
    print(Escala('pentatonica menor', tonica, 'sostenidos'))
    
    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("Acordes Mayores:")    

for tonica in Musica.notas['sostenidos']:
    print(Acorde('mayor', tonica))

    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")

print("Acordes Maj7:")    

for tonica in Musica.notas['sostenidos']:
    print(Acorde('maj7', tonica))
   
   
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")

print("Acordes Maj1:")    

for tonica in Musica.notas['sostenidos']:
    print(Acorde('maj11', tonica))

    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("Acordes Menores:")    

for tonica in Musica.notas['sostenidos']:
    print(Acorde('menor', tonica))
    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("Progresion de acordes para cada grado de la escala mayor:")

for tonica in Musica.notas['sostenidos']:
    escala = Escala('mayor', tonica)
    print(escala)
    
    for i in range(0, len(escala)):
        print(Acorde(Musica.progresion['mayor'][i], escala.notas[i]))
 
    print("")
    
    
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("------------------------------------------------------------------------")
print("Progresion de acordes para cada grado de la escala menor:")

for tonica in Musica.notas['sostenidos']:
    escala = Escala('menor', tonica)
    print(escala)
    
    for i in range(0, len(escala)):
        print(Acorde(Musica.progresion['menor'][i], escala.notas[i]))
 
    print("")
    
