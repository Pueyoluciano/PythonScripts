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
        self.notas = itertools.cycle(notes)
     
        self.note = 0
     
    def __next__(self):
        self.note = next(self.notas)
        return next(self.euclideo)

        
class Matrix:
    """
        La matrix es la que gestiona todo el flujo de la Drum Ex Machina.
    """
    
    def __init__(self, tempo, volumen):
        self.tempo = 120
        self.volumen = 100
        
        segundos = (60 / tempo) * 1000
        self.figuras = {
                        'redonda': int(segundos * 4),
                        'blanca': int(segundos * 2),
                        'negra': int(segundos),
                        'corchea': int(segundos / 2),
                        'semicorchea': int(segundos / 4),
                        'fusa': int(segundos / 8),
                        'semifusa': int(segundos / 16)
                    }
        
        self.canales = [
                        Canal(nombre='Canal 1', pulsos=5, ritmo=7, rotacion=0, notes=[44], velocity=127, channel=9, instrument=0),
                        Canal(nombre='Canal 2', pulsos=3, ritmo=7, rotacion=0, notes=[37, 36, 37], velocity=127, channel=9, instrument=0),
                        Canal(nombre='Canal 3', pulsos=1, ritmo=14, rotacion=0, notes=[60, 62, 63], velocity=127, channel=0, instrument=5),
                        Canal(nombre='Canal 3', pulsos=1, ritmo=14, rotacion=0, notes=[63, 65, 66], velocity=127, channel=0, instrument=5),
                    ]
        
    def iniciar_midi(self):
        pygame.midi.init()
        self.midi_player = pygame.midi.Output(0)
        
    def configuracionInicial(self):
        for canal in self.canales:
            self.midi_player.set_instrument(canal.instrument, canal.channel)
        
    def actualizarConfiguracion(self):
        pass
        
    def loop(self):
        self.iniciar_midi()
        
        try:
            salir = False
            
            self.configuracionInicial()
            
            while not salir:
                for canal in self.canales:
                    if next(canal):
                        self.midi_player.note_on(canal.note, canal.velocity, canal.channel)
                        
                        # Hay que definir una forma de note_offear las notas
                        # self.midi_player.note_off(canal.note, ,canal.velocity, canal.channel)

                        self.actualizarConfiguracion()

                pygame.time.delay(self.figuras['corchea'])
                 
        finally:
            del self.midi_player
            pygame.midi.quit()
            
            
dem = Matrix(180, 100)
dem.loop()