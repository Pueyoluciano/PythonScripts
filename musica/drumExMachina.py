import itertools
import pygame.midi

from ritmosEuclideos import *

class Canal:
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
        
        self.canales = [
                        # Canal(nombre='Canal 1', pulsos=5, ritmo=7, rotacion=0, notes=[44], velocity=127, channel=9, instrument=0),
                        # Canal(nombre='Canal 2', pulsos=3, ritmo=7, rotacion=0, notes=[37, 36, 37], velocity=127, channel=9, instrument=0),
                        # Canal(nombre='Canal 3', pulsos=8, ritmo=14, rotacion=0, notes=[60, 62, 63], velocity=127, channel=0, instrument=5),
                        # Canal(nombre='Canal 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5),

                        #Doble pedal bien RACK
                        Canal(nombre='Canal 1', pulsos=2, ritmo=8, rotacion=0, notes=[44,44,44,57], velocity=127, channel=9, instrument=0),
                        Canal(nombre='Canal 2', pulsos=8, ritmo=8, rotacion=4, notes=[36], velocity=127, channel=9, instrument=0),
                        Canal(nombre='Canal 3', pulsos=2, ritmo=8, rotacion=2, notes=[38], velocity=127, channel=9, instrument=0),
                        
                        # GAME OF TRONES
                        Canal(nombre='Canal 3', pulsos=4, ritmo=10, rotacion=0, notes=[69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 66, 67, 69, 62, 66, 67,], velocity=127, channel=0, instrument=4),
                        # Canal(nombre='Canal 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5),
                    ]
        
        self.ticks = 0
        self.silencios = []
        
    def iniciar_midi(self):
        pygame.midi.init()
        self.midi_player = pygame.midi.Output(0)
        
    def configuracionInicial(self):
        for canal in self.canales:
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
        for canal in self.canales:
            out += str(canal.note) + " "
            
            if next(canal):
                self.midi_player.note_on(canal.note, canal.velocity, canal.channel)
                
                self.silencios.append(Silencio(canal.note,canal.channel, self.ticks + canal.note_duracion))
                
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