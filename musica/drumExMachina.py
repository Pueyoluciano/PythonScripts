import time
import itertools
import pygame.midi

from ritmosEuclideos import *
from midi_instruments import *

"""
    TODOS:
        1 - enviar Midi a un Midi input - (Fruty loops)
        2 - interfaz grafica !
            a - fasade para enviar mensajes y actualizar la configuracion ON THE FLY
        
        3 - interfaz por consola:
            a - mostrar toda la partitura (y tal vez las notas)
        
        4 - Mejorar el armado de las partituras, listas de Secciones ?
"""


class Nota:
    _lista = {
        'sostenidos': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
        'bemoles': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    }

    def __init__(self, nota_string):
        """
            nota_string: string que identifica una nota musical.
                Debe respetar el siguiente orden:
                
                NOTA (en notacion americana) + ALTERACION(opcional / # o b) + OCTAVA (0 - 9) 
                
                Por ejemplo:
                    C4 
                    Bb1 (o su equivalente A#1)
                    A#2 (o su equivalente Bb2)
        """
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
                self.octava = int(nota_string[2])
                
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
    
    def octavar(self, octavas):
        self.indice += 12 * (octavas)
        self.octava += octavas

        return self
        
    def __repr__(self):
        return self._lista[self.notacion][self.altura] + str(self.octava)
    
    def __str__(self):
        return self.__repr__()
    
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
        
        retorno:
        [60, 62, 64, 65, 67, 69, 71, 72]
        
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

class Acorde:
    """
        Acorde.generar('C4', [1, '3b', 5, 7, 9, 11]) Dmaj11
        Acorde('C4', [1, '3b', 5, 7, 9, 11]).notas   Dmaj11
        Acorde('C4', 'mayor')
    """
    _modo_mayor = [2,2,1,2,2,2,1]

    _listado = {
        'mayor': [1,3,5],
        'menor':  [1,'3b',5],
        'aumentado': [1,3,'5#'],
        'disminuido': [1,'3b','5b'],
        'maj7': [1,3,5,7],
        'maj9': [1,3,5,7,9],
        'maj11': [1,3,5,7,9,11]
    }
    
    def __init__(self, tonica, grados, arpegiado='rasgueado'):
        self.arpegiado = 'rasgueado'
        self.tonica = tonica
        self.grados = grados
        self.notas = self.generar(tonica, grados)
    
    @classmethod    
    def generar(cls, tonica, grados):
        retorno = []
        
        escala = Escala.generar(tonica, cls._modo_mayor)
        
        grados_lista = grados
        
        if type(grados) is str:
            grados_lista = cls._listado[grados]
        
        for grado in grados_lista:
            # Si es justo es un numero
            if type(grado) is int:
                orden = grado % (len(cls._modo_mayor) + 1)
                octava = grado // (len(cls._modo_mayor) + 1)
                alteracion = 0
                
            # Si no, viene acompañado de un # o un b
            else:
                orden = int(grado[0]) % (len(cls._modo_mayor) + 1)
                octava = orden // (len(cls._modo_mayor) + 1)
                
                if grado[1] == 'b': # bemol
                    alteracion = -1
                    
                else: # sostenido
                    alteracion = 1
        
            # los pasos son:
            # 1 - Obetener la nota (independientemente de su alteracion, # o b) de la escala.
            # 2 - como la escala tiene los indices, convierto ese valor a Nota().
            # 3 - altero la nota segun corresponda: 0 si es justa, +1 si es #, -1 si es b.
            # 4 - obtengo su indice, ya que es la parte que me interesa de la nota.
            
            retorno.append(Nota(escala[orden - 1]).aumentar(alteracion).octavar(octava).indice)
            
        return retorno

    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return str(self.notas)


class Seccion:
    def __init__(self, duracion, pulsos, ritmo, rotacion, notas):
        self.duracion = duracion
        self.pulsos = pulsos
        self.ritmo = ritmo
        self.rotacion = rotacion
        
        # Si la lista de notas son notas ( osea, strings) las convierto al tipo Nota,
        # Si son Acordes, las dejo como estan
        self.notas = [Nota(nota) if type(nota) is int else nota for nota in notas]

        
class Partitura:
    def __init__(self, *secciones):
        self.secciones = secciones
    
        
class Pista:
    def __init__(self, nombre, partitura, velocity, channel, instrument, duracion=0, activo=True):
    # def __init__(self, nombre, pulsos, ritmo, rotacion, notes, velocity, channel, instrument, duracion=4, activo=True):
        self.nombre = nombre
        self.activo = activo
        self.partitura = partitura
        
        # self.pulsos = pulsos
        # self.ritmo = ritmo
        # self.rotacion = rotacion
        
        self.velocity = velocity
        self.channel = channel
        self.instrument = instrument
        
        self.note = 0
        self.note_duracion = duracion
        
        # self.euclideo = Euclideo(pulsos, ritmo, rotacion)
        # self.notas = itertools.cycle(notes)
        # self._listado = notes
        
        self._generar_partitura()
    
    def _generar_partitura(self):
        self.secciones = len(self.partitura.secciones)
        self.seccion_actual = -1
        
        self._avanzar_seccion()
        
    def _avanzar_seccion(self):
        self.seccion_actual = (self.seccion_actual + 1)  % self.secciones
        
        duracion = self.partitura.secciones[self.seccion_actual].duracion
        self._loop = duracion == 0
        
        pulsos = self.partitura.secciones[self.seccion_actual].pulsos
        ritmo = self.partitura.secciones[self.seccion_actual].ritmo
        rotacion = self.partitura.secciones[self.seccion_actual].rotacion
        notas = self.partitura.secciones[self.seccion_actual].notas
        
        self._contador = duracion * ritmo
        
        self.euclideo = Euclideo(pulsos, ritmo, rotacion)
        self.notas = itertools.cycle(notas)
        self._listado = notas
    
    def __next__(self):
        if not self._loop:
            if self._contador == 0:
                self._avanzar_seccion()
            
            self._contador -= 1
        
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
    
    def __init__(self, tempo, pulso, volumen):
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
        
        self.arpegiados = {
                'rasgueado': 0
            }
        
        self.pulso = self.figuras[pulso]
        
        self.pistas = []
        
        self.ticks = 0
        self.silencios = []
        
    def agregar_pista(self, pista):
        self.pistas.append(pista)
    
    def iniciar_midi(self):
        pygame.midi.init()
        self.midi_player = pygame.midi.Output(0)
        
    def configuracion_inicial(self):
        for pista in self.pistas:
            self.midi_player.set_instrument(pista.instrument, pista.channel)
        
            print(pista.nombre, pista.euclideo, pista._listado)
            
    def actualizar_configuracion(self):
        pass
    
    def silenciar_notas(self):
        for silencio in self.silencios:  
            if self.ticks == silencio.time:
                self.midi_player.note_off(silencio.note, 0, silencio.channel)
                
        self.silencios[:] = itertools.filterfalse(lambda x: x.time == self.ticks, self.silencios)    
    
    def reproducir_notas(self):
        out = ""
        for pista in self.pistas:
            out += str(pista.note) + " "
            
            if next(pista):
                self._reproducir(pista)
                
        # print(out)
    
    def _reproducir(self, pista):
        # Si la nota es un Acorde, hay que reproducir las notas al mismo tiempo.
        if type(pista.note) is Acorde:
            for nota in pista.note.notas:
                self.midi_player.note_on(int(nota), pista.velocity, pista.channel)
                self.silencios.append(Silencio(int(nota),pista.channel, self.ticks + pista.note_duracion))
        
        else: 
            if type(pista.note) is Nota:
                self.midi_player.note_on(int(pista.note.indice), pista.velocity, pista.channel)
                self.silencios.append(Silencio(int(pista.note.indice),pista.channel, self.ticks + pista.note_duracion))
                
            else: 
                if type(pista.note) is int: 
                    self.midi_player.note_on(int(pista.note), pista.velocity, pista.channel)
                    self.silencios.append(Silencio(int(pista.note),pista.channel, self.ticks + pista.note_duracion))
            
    def loop(self):
        self.iniciar_midi()
        
        try:
            self.configuracion_inicial()

            salir = False
            
            while not salir:
                # Agrego una medicion de tiempo para compensar el tiempo que toman
                # los primeros 3 pasos.
                a = time.perf_counter() 

                self.silenciar_notas()
                
                self.reproducir_notas()

                self.actualizar_configuracion()
                
                # pygame.time.delay(self.pulso)
                pygame.time.delay(int(self.pulso - (time.perf_counter() - a) * 1000))
                
                self.ticks+= 1
                
        finally:
            del self.midi_player
            pygame.midi.quit()

            
def testeos():
    # Pista(nombre='Pista 1', pulsos=5, ritmo=7, rotacion=0, notes=[44], velocity=127, channel=9, instrument=0),
    # Pista(nombre='Pista 2', pulsos=3, ritmo=7, rotacion=0, notes=[37, 36, 37], velocity=127, channel=9, instrument=0),
    # Pista(nombre='Pista 3', pulsos=8, ritmo=14, rotacion=0, notes=[60, 62, 63], velocity=127, channel=0, instrument=5),
    # Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5),

    #Doble pedal bien RACK
    # Pista(nombre='Pista 1', pulsos=2, ritmo=8, rotacion=0, notes=[44,44,44,57], velocity=127, channel=9, instrument=0),
    # Pista(nombre='Pista 2', pulsos=8, ritmo=8, rotacion=4, notes=[36], velocity=127, channel=9, instrument=0),
    # Pista(nombre='Pista 3', pulsos=2, ritmo=8, rotacion=2, notes=[38], velocity=127, channel=9, instrument=0),
    # Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=Escala.generar('C4', [2,2,1,2,2,2,1,2]), velocity=127, channel=0, instrument=63),

    # GAME OF TRONES
    # Pista(nombre='Pista 3', pulsos=4, ritmo=10, rotacion=0, notes=[69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 66, 67, 69, 62, 66, 67,], velocity=127, channel=0, instrument=4),
    # Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5),


    #Bleed
    dem = Matrix(tempo=220, pulso='semicorchea', volumen=100)
    dem = Matrix(tempo=140, pulso='corchea', volumen=100)
    
    """
    dem.agregar_pista(Pista(nombre='Pista 1', pulsos=7, ritmo=7, rotacion=0, notes=[44,44,44,44,44,44,44,46,44,44,44,44,44,44], velocity=127, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 2', pulsos=4, ritmo=7, rotacion=0, notes=[36, 36, 37, 36], velocity=127, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 3', pulsos=1, ritmo=14, rotacion=0, notes=[Acorde('C4', [1,3,5,11]), Acorde('C4', [1,'3b',5,13]), Acorde('C4', [1,2,5,12])], velocity=30, channel=0, instrument=95,duracion=14))
    dem.agregar_pista(Pista(nombre='Pista 4', pulsos=3, ritmo=7, rotacion=0, notes=[Nota('C2')], velocity=127, channel=1, instrument=33))
    # dem.agregar_pista(Pista(nombre='Pista 5', pulsos=1, ritmo=4, rotacion=0, notes=Escala.generar('C4', [2,2,1,2,2,2,1,2]), velocity=50, channel=2, instrument=28))
    dem.agregar_pista(Pista(nombre='Pista 6', pulsos=1, ritmo=14, rotacion=0, notes=[Nota('C6'), Nota('C6').disminuir(1), Nota('C6').disminuir(3)], velocity=50,channel=2, instrument=74,duracion=14))
    """

    """
    p1 = Partitura(Seccion(duracion=2, pulsos=7, ritmo=7, rotacion=0, notas=[44,44,44,44,44,44,44,46,44,44,44,44,44,44]))
    p2 = Partitura(Seccion(duracion=1, pulsos=4, ritmo=7, rotacion=0, notas=[36, 36, 37, 36]))
    p3 = Partitura(Seccion(duracion=3, pulsos=1, ritmo=14, rotacion=0, notas=[Acorde('C4', [1,3,5,11]), Acorde('C4', [1,'3b',5,13]), Acorde('C4', [1,2,5,12])]))
    p4 = Partitura(Seccion(duracion=2, pulsos=4, ritmo=7, rotacion=0, notas=[Nota('C2')]),
                Seccion(duracion=2, pulsos=4, ritmo=7, rotacion=0, notas=[Nota('B1')]),
                Seccion(duracion=2, pulsos=4, ritmo=7, rotacion=0, notas=[Nota('A1')])
                )
    p5 = Partitura(Seccion(duracion=1, pulsos=1, ritmo=4, rotacion=0, notas=Escala.generar('C4', [2,2,1,2,2,2,1,2])))
    p6 = Partitura(Seccion(duracion=3, pulsos=1, ritmo=14, rotacion=0, notas=[Nota('C6'), Nota('C6').disminuir(1), Nota('C6').disminuir(3)]))

    dem.agregar_pista(Pista(nombre='Pista 1', partitura=p1, velocity=127, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 2', partitura=p2, velocity=127, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 3', partitura=p3, velocity=30, channel=0, instrument=95,duracion=14))
    dem.agregar_pista(Pista(nombre='Pista 4', partitura=p4, velocity=127, channel=1, instrument=33))
    # dem.agregar_pista(Pista(nombre='Pista 5', partitura=p5, velocity=50, channel=2, instrument=28))
    dem.agregar_pista(Pista(nombre='Pista 6', partitura=p6, velocity=50,channel=2, instrument=74,duracion=14))
    """

    """
    p1 = Partitura(Seccion(duracion=16, pulsos=2, ritmo=4, rotacion=0, notas=[44]),
                    Seccion(duracion=16, pulsos=2, ritmo=4, rotacion=0, notas=[46]),
                )
    p2 = Partitura(Seccion(duracion=16, pulsos=1, ritmo=4, rotacion=1, notas=[36]),
                    Seccion(duracion=16, pulsos=4, ritmo=4, rotacion=0, notas=[36])
                )
    p3 = Partitura(Seccion(duracion=1, pulsos=1, ritmo=4, rotacion=2, notas=[38]),
                    # Seccion(duracion=4, pulsos=4, ritmo=4, rotacion=0, notas=[48, 45, 43, 41])
                )            
    p4 = Partitura(Seccion(duracion=1,  pulsos=6, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=6, ritmo=8, rotacion=0, notas=[Nota('E2')]),
                    Seccion(duracion=2, pulsos=6, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=6, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=6, ritmo=8, rotacion=0, notas=[Nota('E2')]),
                    Seccion(duracion=2, pulsos=6, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    
                    Seccion(duracion=1, pulsos=7, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=7, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=7, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=7, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                    
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                )
    p5 = Partitura(
                    Seccion(duracion=8, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('D3', [1,'3b',5]), Acorde('E3', [1,'3b',5]), Acorde('F3', [1,3,5]), Acorde('F3', [1,3,5])]),
                    Seccion(duracion=4, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('C3', [1,3,5]), Acorde('D3', [1,'3b',5]), Acorde('C3', [1,3,5]), Acorde('Bb3', [1,3,5])]),
                    Seccion(duracion=4, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('D4', [1,'3b',5]), Acorde('F4', [1,3,5]), Acorde('C4', [1,3,5]), Acorde('Bb4', [1,3,5])]),
    )

   """
    # PET SEMATARY CHORDS
    # Dm, Em, F
    # C, Dm, C, Bb
    # Dm, F, C, Bb


    # p1 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=10, rotacion=0, notas=[36,37]),
                    # Seccion(duracion=1, pulsos=4, ritmo=4, rotacion=0, notas=[44]),
                # )
    # p2 = Partitura(Seccion(duracion=0, pulsos=2, ritmo=10, rotacion=0, notas=[53]),
                    # Seccion(duracion=4, pulsos=8, ritmo=8, rotacion=0, notas=[53]),
                    # Seccion(duracion=1, pulsos=2, ritmo=4, rotacion=0, notas=[36,38])
                # )

    # GAME OF TRONES
    # p5 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=10, rotacion=0, notas=[69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 65, 67, 69, 62, 66, 67, 69, 62, 66, 67,]))
    # p2 = Pista(nombre='Pista 4', pulsos=3, ritmo=14, rotacion=0, notes=[72, 74, 75], velocity=127, channel=0, instrument=5)
                

    # BLEED
    # p1 = Partitura(Seccion(duracion=0, pulsos=3, ritmo=8, rotacion=0, notas=[36,36,37]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=2, ritmo=4, rotacion=0, notas=[44]))
    
    # p1 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=6, rotacion=2, notas=[36]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=4, rotacion=0, notas=[44]))
    
    # p3 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=24, rotacion=16, notas=[38]))
    
    # p4 = Partitura(Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E2')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E2')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
                
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('F#1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('A2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#3')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
                
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('F#1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('A2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#3')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#2')]),
    # )
    
    # p5 = Partitura(Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E1')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E1')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
                
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('F#0')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G0')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('A1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
                
                # Seccion(duracion=4, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('F#0')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G0')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('A1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('E1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#2')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('G1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('C#1')]),
                # Seccion(duracion=1, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
                # Seccion(duracion=8, pulsos=4, ritmo=6, rotacion=2, notas=[Nota('D#1')]),
    # )
    
    
    """
    Bleed notes
    F#
    G
    A
    E
    C#
    G
    C#
    D#
    """
    
    # p4 = Partitura(Seccion(duracion=4, pulsos=3, ritmo=7, rotacion=0, notas=['G1']),
                # Seccion(duracion=2, pulsos=3, ritmo=7, rotacion=0, notas=['G1']),
                # Seccion(duracion=2, pulsos=3, ritmo=7, rotacion=0, notas=['F1']),
    # )
    
    # p5 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('C3', [1,3,5]), Acorde('G3', [1,3,5]), Acorde('A3',[1,'3b',5]), Acorde('F3',[1,3,5])]))
    # p5 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('C3', 'mayor'), Acorde('G3', 'mayor'), Acorde('A3','menor'), Acorde('F3','mayor')]))
    
    # p5 = Partitura(Seccion(duracion=2, pulsos=1, ritmo=14, rotacion=0, notas=[Acorde('G2', 'mayor')]),
                # Seccion(duracion=1, pulsos=1, ritmo=14, rotacion=0, notas=[Acorde('G2', 'menor')]),
                # Seccion(duracion=1, pulsos=1, ritmo=14, rotacion=0, notas=[Acorde('F2', 'mayor')]),
    # )
    
    # Rock
    p1 = Partitura(Seccion(duracion=0, pulsos=2, ritmo=4, rotacion=0, notas=[36, 38]))
    p2 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=1, rotacion=0, notas=[42]))
    # p5 = Partitura(Seccion(duracion=3, pulsos=4, ritmo=4, rotacion=0, notas=[Nota('A2')]),
    #                Seccion(duracion=1, pulsos=2, ritmo=2, rotacion=0, notas=[Nota('E2')]),
    #                Seccion(duracion=1, pulsos=2, ritmo=2, rotacion=0, notas=[Nota('G2')]))
    
    
    # Power metal 1
    # p1 = Partitura(Seccion(duracion=0, pulsos=16, ritmo=16, rotacion=0, notas=[36]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=8, ritmo=16, rotacion=0, notas=[42]))
    # p3 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=16, rotacion=2, notas=[38]))
    # p5 = Partitura(Seccion(duracion=1, pulsos=8, ritmo=16, rotacion=0, notas=[Nota('G#2')]),
                    # Seccion(duracion=1, pulsos=8, ritmo=16, rotacion=0, notas=[Nota('D#3')]),
                    # Seccion(duracion=1, pulsos=8, ritmo=16, rotacion=0, notas=[Nota('A#2')]),
                    # Seccion(duracion=1, pulsos=8, ritmo=16, rotacion=0, notas=[Nota('F3')]))
    
    
    # Power metal 2
    # p1 = Partitura(Seccion(duracion=0, pulsos=7, ritmo=16, rotacion=0, notas=[36]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=8, ritmo=16, rotacion=0, notas=[42]))
    # p3 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=16, rotacion=0, notas=[38]))
    # p5 = Partitura(Seccion(duracion=4, pulsos=4, ritmo=4, rotacion=0, notas=[Nota('C3')]),
                    # Seccion(duracion=4, pulsos=4, ritmo=4, rotacion=0, notas=[Nota('E3')]))
    

    
    # Power metal 3
    # p1 = Partitura(Seccion(duracion=0, pulsos=16, ritmo=16, rotacion=0, notas=[36]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=8, ritmo=16, rotacion=0, notas=[42]))
    # p3 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=16, rotacion=0, notas=[38]))
    # p5 = Partitura(Seccion(duracion=4, pulsos=4, ritmo=4, rotacion=0, notas=[Nota('C3')]),
                    # Seccion(duracion=4, pulsos=4, ritmo=4, rotacion=0, notas=[Nota('E3')]))
    

    # BLUES
    # 1 1 1 (Aca esta la jodita)
    # 1 0 0
    # p1 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=6, rotacion=0, notas=[36]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=3, ritmo=3, rotacion=0, notas=[44]))
    # p3 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=6, rotacion=3, notas=[38]))
    # p5 = Partitura(Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('A1')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('D2')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('A1')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('D2')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('E2')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('D2')]),)

    # PROGROCKS
    # p1 = Partitura(Seccion(duracion=0, pulsos=3, ritmo=7, rotacion=0, notas=[36,36,38]))
    # p2 = Partitura(Seccion(duracion=0, pulsos=7, ritmo=7, rotacion=0, notas=[44]))
    # p3 = Partitura(Seccion(duracion=0, pulsos=1, ritmo=7, rotacion=0, notas=[38]))
    # p5 = Partitura(Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('A1')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('D2')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('A1')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('D2')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('E2')]),
                    # Seccion(duracion=4, pulsos=2, ritmo=3, rotacion=0, notas=[Nota('D2')]),)
    
    dem.agregar_pista(Pista(nombre='Pista 1', partitura=p1, velocity=100, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 2', partitura=p2, velocity=100, channel=9, instrument=0))
    # dem.agregar_pista(Pista(nombre='Pista 3', partitura=p3, velocity=100, channel=9, instrument=0))
    # dem.agregar_pista(Pista(nombre='Pista 4', partitura=p4, velocity=100, channel=2, instrument=30, duracion=6))
    # dem.agregar_pista(Pista(nombre='Pista 5', partitura=p5, velocity=127, channel=3, instrument=33, duracion=6))
    dem.loop()

if __name__ == "__main__":
    testeos()
    


    
# Acciones - interfaz

# START / STOP / QUIT

# Agregar Pista
# Agregar Pista -> Partitura
# Agregar Pista -> Partitura -> Seccion

# Pista -> midi_channel, instrument, velocity, Partitura, nombre

# Partitura -> [Seccion]

# Seccion -> duracion, pulsos, ritmo, rotacion, [notas]

