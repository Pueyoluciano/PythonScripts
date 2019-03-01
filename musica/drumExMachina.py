import time
import itertools
import pygame.midi

from ritmosEuclideos import *

class Nota:
    _lista = {
        'sostenidos': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
        'bemoles': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    }

    def __init__(self, nota_string):
        if type(nota_string) is int:
            self.notacion = 'sostenidos'
            self.indice = 127 if nota_string > 127 else (0 if nota_string < 0 else nota_string)
            self.octava = (self.indice // 12) - 1
            self.altura = self.indice % 12
            
        else:
            if len(nota_string) == 2:
                self.notacion = 'sostenidos'
                self.altura = self._lista[self.notacion].index(nota_string[0])
                self.octava = int(nota_string[1])
                
            if len(nota_string) == 3:
                self.notacion = 'sostenidos' if nota_string[1] == "#" else 'bemoles'
                self.altura = self._lista[self.notacion].index(nota_string[:2])
                self.octava = int(nota_string[1])
                
            self.indice =  self.altura + 12 * (self.octava + 1)
    
    def aumentar(self, semitonos):
        self.indice += semitonos
        self.octava = (self.indice // 12) - 1
        self.altura = self.indice % 12
        
        return self
        
    def disminuir(self, semitonos):
        self.indice -= semitonos
        self.octava = (self.indice // 12) - 1
        self.altura = self.indice % 12
        
        return self
    
    def __str__(self):
        return self._lista[self.notacion][self.altura] + str(self.octava)
    
    @classmethod
    def octava(cls, nota):
        return (nota// 12) - 1

    @classmethod
    def signatura(cls, nota, notacion='sostenidos'):
        return cls._lista[notacion][nota % 12] + str(cls.octava(nota))
    
    @classmethod
    def frecuencia(cls, nota, afinacion=440):
        """
        La formula general es:
            frecuencia = 440hz * (a ** n)
            
        donde:
            - 440hz es la frecuencia de A4 (Afinacion estandar con A4 = 440Hz)
            - a es 2 ** (1/12). este numero es fijo.
            - n son los semitonos de separacion entre A4 y la nota que se busca obtener su frecuencia.
        """
        
        n = nota - 69
        return afinacion * ((2**(1/12)) ** n)
    
class Escala:
    """
        Escala.generar(60, [2,2,1,2,2,2,1])
        Escala.generar('C4', [2,2,1,2,2,2,1])
        Escala.generar(Nota(60), [2,2,1,2,2,2,1])
        Escala.generar(Nota('C4'), [2,2,1,2,2,2,1])
    """
    
    @classmethod
    def generar(cls, tonica, intervalos):
        if type(tonica) is Nota:
            tonica = tonica.indice
    
        if type(tonica) is str:
            tonica = Nota(tonica).indice
        
        retorno = []
        
        for intervalo in intervalos:
            retorno.append(tonica)
            
            tonica += intervalo
    
        return retorno
    
class Pista:
    def __init__(self, nombre, pulsos, ritmo, rotacion, notes, velocity, channel, instrument, activo=True):
        self.nombre = nombre
        self.rotacion = rotacion
        self.activo = activo
        
        self.velocity = velocity
        self.channel = channel
        self.instrument = instrument
        
        self.euclideo = Euclideo(pulsos, ritmo)
        self.euclideo.rotar(self.rotacion)
        self.notas = itertools.cycle(notes)
     
        self.note = 0
        self.note_duracion = 4
     
    def __next__(self):
        ret = next(self.euclideo)

        if ret:
            self.note = next(self.notas)
        
        return ret

        
class Silencio:
    def __init__(self, note, channel, time):
        self.note = note
        self.channel = channel
        self.time = time


class Matrix:
    """
        La matrix es la que gestiona todo el flujo de la Drum Ex Machina.
    """
    
    def __init__(self, tempo, volumen):
        self.tempo = tempo
        self.volumen = volumen
        
        segundos = (60 / self.tempo) * 1000
        self.figuras = {
                        'redonda': int(segundos * 4),
                        'blanca': int(segundos * 2),
                        'negra': int(segundos),
                        'corchea': int(segundos / 2),
                        'semicorchea': int(segundos / 4),
                        'fusa': int(segundos / 8),
                        'semifusa': int(segundos / 16)
                    }
        
        self.pulso = self.figuras['semicorchea']
        
        self.pistas = [
                        # Pista(nombre='Pista 1', pulsos=5, ritmo=7, rotacion=0, notes=[44], velocity=127, channel=9, instrument=0),
                        # Pista(nombre='Pista 2', pulsos=3, ritmo=7, rotacion=0, notes=[37, 36, 37], velocity=127, channel=9, instrument=0),
                        # Pista(nombre='Pista 3', pulsos=8, ritmo=14, rotacion=0, notes=[60, 62, 63], velocity=127, channel=0, instrument=5),
                        # Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5),

                        #Doble pedal bien RACK
                        Pista(nombre='Pista 1', pulsos=2, ritmo=8, rotacion=0, notes=[44,44,44,57], velocity=127, channel=9, instrument=0),
                        Pista(nombre='Pista 2', pulsos=8, ritmo=8, rotacion=4, notes=[36], velocity=127, channel=9, instrument=0),
                        Pista(nombre='Pista 3', pulsos=2, ritmo=8, rotacion=2, notes=[38], velocity=127, channel=9, instrument=0),
                        Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=Escala.generar('C4', [2,2,1,2,2,2,1,2]), velocity=127, channel=0, instrument=63),
                        
                        # GAME OF TRONES
                        # Pista(nombre='Pista 3', pulsos=4, ritmo=10, rotacion=0, notes=[69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 66, 67, 69, 62, 66, 67,], velocity=127, channel=0, instrument=4),
                        # Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5),
                    ]
        
        self.ticks = 0
        self.silencios = []
        
    def iniciar_midi(self):
        pygame.midi.init()
        self.midi_player = pygame.midi.Output(0)
        
    def configuracionInicial(self):
        for canal in self.pistas:
            self.midi_player.set_instrument(canal.instrument, canal.channel)
        
            print(canal.euclideo)
            
    def actualizarConfiguracion(self):
        pass
    
    def silenciar_notas(self):
        for silencio in self.silencios:  
            if self.ticks == silencio.time:
                self.midi_player.note_off(silencio.note, 0, silencio.channel)
                
        self.silencios[:] = itertools.filterfalse(lambda x: x.time == self.ticks, self.silencios)    
    
    def reproducir_notas(self):
        out = ""
        for canal in self.pistas:
            out += str(canal.note) + " "
            
            if next(canal):
                self.midi_player.note_on(int(canal.note), canal.velocity, canal.channel)
                
                self.silencios.append(Silencio(int(canal.note),canal.channel, self.ticks + canal.note_duracion))
                
        # print(out)
    
    def loop(self):
        self.iniciar_midi()
        
        try:
            self.configuracionInicial()

            salir = False
            
            while not salir:
                self.silenciar_notas()
                
                self.reproducir_notas()

                self.actualizarConfiguracion()
                
                pygame.time.delay(self.pulso)
                
                self.ticks+= 1
                
        finally:
            del self.midi_player
            pygame.midi.quit()


dem = Matrix(120, 100)
dem.loop()