# -*- coding: utf-8 -*-
from functools import *
import sys

import time
import pygame.midi

sys.path.insert(0, '../intefaz')
from consola import *


class Interfaz:
    """
    """
    def __init__(self):
        self.player = None
        
        self.menu = Menu(
                Nodo("Escalas Generator 1.0", "Pequeña implementacion para generar acordes, escalas y otras yerbas", True, 
                    Nodo("Acordes", "Reproducir un acorde", True, *[Accion(acorde, True, lambda x: print(x), acorde) for acorde in Musica.acordes.keys()]),
                    Nodo("Escalas", "", False),
                    Nodo("Inversiones", "", False),
                    Nodo("Progresiones", "", False)
                )
            )   

    def loop(self):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0)

        try:
            self.menu.iniciar()
            
            
        finally:    
            del self.player
            pygame.midi.quit()
        
        
class Nota:
    """
    """
    _notas = {
        'sostenidos': ['C' , 'C#','D' , 'D#','E' ,'F' , 'F#','G' , 'G#','A' , 'A#','B'],
        'bemoles': ['C' , 'Db','D' , 'Eb','E' ,'F' , 'Gb','G' , 'Ab','A' , 'Bb','B']
    }

    def __init__(self, nota_string, notacion="sostenidos"):
        """
            Podemos crear una nota de varias maneras:
            - type(nota_string) is Nota:
                Hacemos una copia de la que recibimos por parametro, asi
                 podemos hacer Notas a partir de otras.
            
            - type(nota_string) is int:
                Podemos crear una nota a partir de su indice. A saber:
                      0 - C0 (Esta se la nota mas baja que podemos tocar)
                      1 - B0 
                       ...
                    127 - G9 (Esta es la nota mas alta que podemos tocar)  
                    
                    Es importante notar que el estandar MIDI define:
                    
                        21 - A0
                    
                    pero en nuestra implementacion:
                    
                         9 - A0
                    
                    Por eso al hacer sonar una nota, le sumamos 12 al indice.
                
                A partir del indice podemos calcular directamente la nota y la octava:
                
                    - La musica occidental convencional usa la escala temperada, que
                        divide la octava en 12 partes iguales llamadas semitonos.
                        Es por esto que podemos trabajar las notas musicales 
                        con aritmetica modular, en particular modulo 12.
                        
                    - Es por esto que:
                        
                        El resto de dividir el indice por 12 nos da su posicion 
                        en el array de notas.
                      
                        La division entera del indice por 12 nos da la octava.
                        
            - type(nota_string) is str:
                Por ultimo podemos crear la nota a partir de un String.
                    - El primer caracter denota la altura (A, B, C ...)
                    
                    - Si el string mide dos caracteres:
                        -- el segundo es la octava.
                    
                    - Si el string mide 3 caracteres es un sostenido o bemol:
                        -- el segundo es la alteracion. # = sostenido | b = bemol
                        -- el tercero es la octava.
                        
                    con estos valores podemos calcular el indice.
              
              
            Si usamos la notacion de sostenidos, usamos los sostenidos en
            la escala cromatica, de igual forma si la notacion es en bemoles,
            veremos la escala cromatica notada en bemoles.
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

    def reproducir(self):
        """
            Las notas MIDI y las que usamos aca estan desfazadas 12 pasos.
            
            en MIDI:
                21 = A0
            
            nosotros:
                0 = C0
                9 = A0
        """
        nota_midi = self.indice + 12
        player.note_on(nota_midi, 127)
    
    def detener(self):
        nota_midi = self.indice + 12
        player.note_off(nota_midi, 127)
        
    
    def disminuir(self, grados):
        """
            Podemos disminuir una nota una cantidad arbitraria de 
            semitonos.
        """
        self.indice -= grados
        self.octava = (self.indice) // 12
        self.clave = (self.indice) % 12
        
        return self
        
    def aumentar(self, grados):
        """
            Podemos aumentar una nota una cantidad arbitraria de 
            semitonos.
        """
        self.indice += grados
        self.octava = (self.indice) // 12
        self.clave = (self.indice) % 12
    
        return self
        
    def octavar(self, octavas):
        """
            Podemos octavar una nota (subir o disminuir su octava) 
            una cantidad entera arbitraria.
        """
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
        'dom7': [1, 3, 5, '7b'],
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

# pygame.midi.init()
# player = pygame.midi.Output(0)
# player.set_instrument(0)

# try:
    # """
    # a = Escala('mayor', 'C')
    # b = Escala('menor', 'C')
    # c = Acorde('maj11', 'C')

    # print(a)
    # a.arpegiar()

    # # print(b)
    # # b.arpegiar()

    # print(c)
    # c.rasguear()
    # """
    
    # # for i in range(0, 61):
        # # a = Nota(i)
        # # print(i, a)
        # # a.reproducir(Musica.figuras['negra'])
        
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("Escalas Mayores: ")

    # for tonica in Musica.notas['sostenidos']:
        # a = Escala('mayor', tonica)
        # print(a)
        # # a.arpegiar()
     
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("Acordes Mayores:")    

    # for tonica in Musica.notas['sostenidos']:
        # a = Acorde('mayor', tonica)
        # print(a)
        # #a.rasguear(Musica.figuras['corchea'])
        # #a.rasguear(Musica.figuras['semicorchea'])
        # #a.rasguear(Musica.figuras['fusa'])
        # #a.rasguear(Musica.figuras['rasgueado'])
    
    # # print("------------------------------------------------------------------------")
    # # print("------------------------------------------------------------------------")
    # # print("------------------------------------------------------------------------")
    # # print("Acordes Maj11:")    

    # # for tonica in Musica.notas['sostenidos']:
        # # a = Acorde('maj11', tonica)
        # # print(a)
        # # a.rasguear(Musica.figuras['corchea'])
        # # a.rasguear(Musica.figuras['semicorchea'])
        # # a.rasguear(Musica.figuras['fusa'])
        # # a.rasguear(Musica.figuras['rasgueado'])
        
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("------------------------------------------------------------------------")
    # print("Acordes dom7:")    

    # for tonica in Musica.notas['sostenidos']:
        # a = Acorde('dom7', tonica)
        # print(a)
        # a.arpegiar()
        # a.rasguear(Musica.figuras['corchea'])
        # a.rasguear(Musica.figuras['semicorchea'])
        # a.rasguear(Musica.figuras['fusa'])
        # a.rasguear(Musica.figuras['rasgueado'])        
    
# finally:    
    # del player
    # pygame.midi.quit()


escalasGenerator = Interfaz().loop()    