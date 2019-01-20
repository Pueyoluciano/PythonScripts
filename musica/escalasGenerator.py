from functools import *
import sys
import time
import pygame.midi

class MIDI:
    pass


class Interfaz:
    """
    """
    def __init__(self):
        pass
        
    def __del__(self):
        pass
        
    def presentacion(self):
        print("-------------------------------------------------")
        print("- Musica: escalas acordes y esas cosas ----------")
        print("-------------------------------------------------")

    def acciones(self):
        print("1. Escalas")
        print("2. Acordes")
        print("3. Progresiones")
        eleccion = input("> ")
        
        if eleccion == "1":
            pass
        
    def loop(self):
        self.presentacion()
        self.acciones()
            

class Nota:
    _notas = {
        'sostenidos': ['C' , 'C#','D' , 'D#','E' ,'F' , 'F#','G' , 'G#','A' , 'A#','B'],
        'bemoles': ['C' , 'Db','D' , 'Eb','E' ,'F' , 'Gb','G' , 'Ab','A' , 'Bb','B']
    }

    def __init__(self, nota_string, notacion="sostenidos"):
        """
        """
        
        # Si Recibo una Nota, simplemente copio sus atributos.
        if type(nota_string) is Nota:
            self.indice = nota_string.indice
            self.clave = nota_string.clave
            self.octava = nota_string.octava
            self.notacion = nota_string.notacion
    
        else:
            # Si recibo un numero, es entonces lo uso de indice
            if type(nota_string) is int:
                self.indice = nota_string
                self.clave = nota_string % 12
                self.octava = nota_string // 12
                self.notacion = notacion
        
            else:
                # Si recibo un String, calculo el indice y la octava
                if len(nota_string) == 2:
                    nota = nota_string[0]
                    self.octava = int(nota_string[1])
                    self.notacion = "sostenidos"
                    
                else:
                    #Si es un sostenido o un bemol, ocupa 3 caracteres
                    nota = nota_string[0:2]
                    self.octava = int(nota_string[2])
                    self.notacion = "sostenidos" if nota_string[1] == "#" else "bemoles"
        
                self.clave = Nota._notas[self.notacion].index(nota)
                
                self.indice = self.clave + (self.octava * 12)
    
    def frecuencia(self):
        """
            La formula general es:
                frecuencia = 440hz * (a ** n)
                
            donde:
                - 440hz es la frecuencia de A4 (Afinacion estandar con A4 = 440Hz)
                - a es 2 ** (1/12). este numero es fijo.
                - n son los semitonos de separacion entre A4 y la nota que se busca obtener su frecuencia.
            
        """
        n = self.indice - 57
        return 440 * ((2**(1/12)) ** n)        
    
    # def reproducir(self, figura=0.5):
        # nota_string = str(self)
        
        # sys.stdout.write(nota_string)
        # sys.stdout.flush()
        
        # nota_midi = self.indice + 12
        
        # player.note_on(nota_midi, 127)
        # time.sleep(figura)
        # player.note_off(nota_midi, 127)
    
        # sys.stdout.write("\b" * len(nota_string))
        # sys.stdout.write(" " * len(nota_string))
        # sys.stdout.write("\b" * len(nota_string))
    
    def reproducir(self):
        nota_midi = self.indice + 12
        player.note_on(nota_midi, 127)
    
    def detener(self):
        nota_midi = self.indice + 12
        player.note_off(nota_midi, 127)
        
    
    def disminuir(self, grados):
        self.indice -= grados
        self.octava = (self.indice) // 12
        self.clave = (self.indice) % 12
        
        return self
        
    def aumentar(self, grados):
        self.indice += grados
        self.octava = (self.indice) // 12
        self.clave = (self.indice) % 12
    
        return self
        
    def octavar(self, octavas):
        if octavas >= 0:
            self.aumentar(12 * octavas)
            
        else:
            self.disminuir(12 * octavas)
    
        return self
        
    def cambiar_notacion(self):
        if self.notacion == "sostenidos":
            self.notacion = "bemoles"
            
        if self.notacion == "bemoles":
            self.notacion = "sostenidos"
    
    def __str__(self):
        return Nota._notas[self.notacion][self.clave] + str(self.octava)
    
    def __repr__(self):
        return self.__str__()
    
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

    
    _cromaticoSostenidos = [
        Nota('C4'), 
        Nota('C#4'), 
        Nota('D4'), 
        Nota('D#4'), 
        Nota('E4'), 
        Nota('F4'), 
        Nota('F#4'), 
        Nota('G4'), 
        Nota('G#4'), 
        Nota('A4'), 
        Nota('A#4'), 
        Nota('B4')
    ]
    
    _cromaticoBemoles= [
        Nota('C4'), 
        Nota('Db4'), 
        Nota('D4'), 
        Nota('Eb4'), 
        Nota('E4'), 
        Nota('F4'), 
        Nota('Gb4'), 
        Nota('G4'), 
        Nota('Ab4'), 
        Nota('A4'), 
        Nota('Bb4'), 
        Nota('B4')
    ]
    
    # _cromaticoSostenidos = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4']
    # _cromaticoBemoles = ['C4', 'Db4', '4D', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4']
    
    # _cromaticoSostenidos = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # _cromaticoBemoles = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    
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
    
    #Los grados son en funcion del modo mayor.
    acordes = {
        'mayor': [1, 3, 5],
        'maj7': [1, 3, 5, 7],
        'maj9': [1, 3, 5, 7, 9],
        'maj11': [1, 3, 5, 7, 9, 11],
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
    
    figuras = {
        'redonda': 1,
        'blanca': 1/2,
        'negra': 1/4,
        'corchea': 1/8,
        'semicorchea': 1/16,
        'fusa': 1/32,
        'semifusa': 1/64,
        'rasgueado': 0
    }
    
    
class Secuencia:
    def __init__(self, modo, tonica):
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
        self.tonica = Nota(tonica)
        self.notas = []
        
    def texto(self):
        return self.tipo + " " + str(self.modo) + " de " + str(self.tonica) + ": "

    def arpegiar(self, figura=Musica.figuras['blanca']):
        for nota in self.notas:
            nota_string = str(nota)
            sys.stdout.write(nota_string)
            sys.stdout.flush()

            nota.reproducir()
            time.sleep(figura)
            nota.detener()
        
            sys.stdout.write("\b" * len(nota_string))
            sys.stdout.write(" " * len(nota_string))
            sys.stdout.write("\b" * len(nota_string))

        time.sleep(Musica.figuras['blanca'])

    
    def rasguear(self, figura=Musica.figuras['rasgueado']):
        for nota in self.notas:
            nota_string = str(nota)
            sys.stdout.write(nota_string)
            sys.stdout.flush()

            nota.reproducir()
            time.sleep(figura)
        
            sys.stdout.write("\b" * len(nota_string))
            sys.stdout.write(" " * len(nota_string))
            sys.stdout.write("\b" * len(nota_string))
            
        time.sleep(1.5)
        
        for nota in self.notas:
            nota.detener()
       
    def __len__(self):
        return len(self.notas)
    
    def __str__(self):
        return  self.texto() + reduce(lambda x, y :str(x) + " - " + str(y),  self.notas)
  

class Escala(Secuencia):
    def __init__(self, modo, tonica):
        """
            modo: debe ser una entrada en el diccionario de Musica.modos. (lista de intervalos que definen la escala).
            tonica: tonica de la escala.
            notacion: mostrar las notas en sostenidos o bemoles.
        """
        super().__init__(modo, tonica)
        self.tipo = "Escala"
        
        auxiliar = Nota(str(self.tonica))
        
        for i in Musica.modos[modo]:
            self.notas.append(Nota(str(auxiliar)))
            
            auxiliar.aumentar(i)
    

class Acorde(Secuencia):
    def __init__(self, nombre, tonica, notacion=Musica.notacion[0], modo='mayor'):
        """
            nombre: nombre del acorde (debe ser una entrada en el diccionario de Musica.acordes.
            
            modo: escala de la cual se toman los grados. Por defecto se usa el modo Mayor.
            
            tonica: tonica del acorde.
            
            notacion: mostrar las notas en sostenidos o bemoles.
            
            base: Escala de base.
        """
        
        super().__init__(modo, tonica)
        self.tipo = "Acorde"
        self.nombre = nombre
        
        self.base = Escala(modo, tonica)
        
        for grado in Musica.acordes[nombre]:
            if type(grado) is int:
                indice = grado - 1
                nota = self.base.notas[indice % len(self.base)]

            else:
                indice = (int(grado[0]) - 1) 
                if grado[1] == 'b':
                    #Disminuido
                    nota = self.base.notas[indice % len(self.base)].disminuir(1)
                    
                else:
                    #Aumentado
                    nota = self.base.notas[indice % len(self.base)].aumentar(1)
                    
            self.notas.append(nota.octavar(indice // len(self.base)))

    def texto(self):
        return self.tipo + " " + str(self.tonica) + " " + str(self.nombre) + ": "

        
class Progresion():
    pass
"""    
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

print("Acordes Maj11:")    

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
    
"""

"""
inter = Interfaz()
inter.loop()
"""

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

try:
    """
    a = Escala('mayor', 'C')
    b = Escala('menor', 'C')
    c = Acorde('maj11', 'C')

    print(a)
    a.arpegiar()

    # print(b)
    # b.arpegiar()

    print(c)
    c.rasguear()
    """
    
    # for i in range(0, 61):
        # a = Nota(i)
        # print(i, a)
        # a.reproducir(Musica.figuras['negra'])
        
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    print("Escalas Mayores: ")

    for tonica in Musica.notas['sostenidos']:
        a = Escala('mayor', tonica)
        print(a)
        # a.arpegiar()
     
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    print("Acordes Mayores:")    

    for tonica in Musica.notas['sostenidos']:
        a = Acorde('mayor', tonica)
        print(a)
        #a.rasguear(Musica.figuras['corchea'])
        #a.rasguear(Musica.figuras['semicorchea'])
        #a.rasguear(Musica.figuras['fusa'])
        #a.rasguear(Musica.figuras['rasgueado'])
    
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("Acordes Maj11:")    

    # for tonica in Musica.notas['sostenidos']:
        # a = Acorde('maj11', tonica)
        # print(a)
        # a.rasguear(Musica.figuras['corchea'])
        # a.rasguear(Musica.figuras['semicorchea'])
        # a.rasguear(Musica.figuras['fusa'])
        # a.rasguear(Musica.figuras['rasgueado'])
        
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    print("Acordes sus2:")    

    for tonica in Musica.notas['sostenidos']:
        a = Acorde('sus2', tonica)
        print(a)
        a.arpegiar()
        a.rasguear(Musica.figuras['corchea'])
        a.rasguear(Musica.figuras['semicorchea'])
        a.rasguear(Musica.figuras['fusa'])
        a.rasguear(Musica.figuras['rasgueado'])        
    
finally:    
    del player
    pygame.midi.quit()
    