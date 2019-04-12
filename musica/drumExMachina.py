import time
import itertools
import pygame.midi

from ritmosEuclideos import *
midi_instruments = {
    "Piano": [
        "1.Acoustic Piano",
        "2.BrtAcou Piano",
        "3.ElecGrand Piano",
        "4.Honky Tonk Piano",
        "5.Elec.Piano 1",
        "6.Elec.Piano 2",
        "7.Harsichord",
        "8.Clavichord",
    ],

    "Chromatic Percussion": [
        "9.Celesta",
        "10.Glockenspiel",
        "11.Music Box",
        "12.Vibraphone",
        "13.Marimba",
        "14.Xylophone",
        "15.Tubular Bells",
        "16.Dulcimer"
    ],

    "Organ": [
        "17.Drawbar Organ",
        "18.Perc. Organ",
        "19.Rock Organ",
        "20.Church Organ",
        "21.Reed Organ",
        "22.Accordian",
        "23.Harmonica",
        "24.Tango Accordian",
    ],

    "Guitar": [
        "25.Acoustic Guitar",
        "26.SteelAcous. Guitar",
        "27.El.Jazz Guitar",
        "28.Electric Guitar",
        "29.El. Muted Guitar",
        "30.Overdriven Guitar",
        "31.Distortion Guitar",
        "32.Guitar Harmonic",
    ],
    "Bass": [
        "33.Acoustic Bass",
        "34.El.Bass Finger",
        "35.El.Bass Pick",
        "36.Fretless Bass",
        "37.Slap Bass 1",
        "38.Slap Bass 2",
        "39.Synth Bass 1",
        "40.Synth Bass 2",
    ],

    "Strings": [
        "41.Violin",
        "42. Viola",
        "43.Cello",
        "44.Contra Bass",
        "45.Tremelo Strings",
        "46.Pizz. Strings",
        "47.Orch. Strings",
        "48.Timpani",
    ],
    
    "Ensemble": [
        "49.String Ens.1",
        "50.String Ens.2",
        "51.Synth.Strings 1",
        "52.Synth.Strings 2",
        "53.Choir Aahs",
        "54. Voice Oohs",
        "55. Synth Voice",
        "56.Orchestra Hit",
    ],
    
    "Brass": [
        "57.Trumpet",
        "58.Trombone",
        "59.Tuba",
        "60.Muted Trumpet",
        "61.French Horn",
        "62.Brass Section",
        "63.Synth Brass 1",
        "64.Synth Brass 2",
    ],
    
    "Reed": [
        "65.Soprano Sax",
        "66.Alto Sax",
        "67.Tenor Sax",
        "68.Baritone Sax",
        "69. Oboe",
        "70.English Horn",
        "71.Bassoon",
        "72.Clarinet",
    ],
    
    "Pipe": [
        "73.Piccolo",
        "74.Flute",
        "75.Recorder",
        "76.Pan Flute",
        "77.Blown Bottle",
        "78.Shakuhachi",
        "79.Whistle",
        "80.Ocarina",
    ],

    "Synth Lead": [
        "81.Lead1 Square",
        "82.Lead2 Sawtooth",
        "83.Lead3 Calliope",
        "84.Lead4 Chiff",
        "85.Lead5 Charang",
        "86.Lead6 Voice",
        "87.Lead7 Fifths",
        "88.Lead8 Bass Ld",
    ],
    
    "Synth Pad": [
        "89.Pad1 New Age",
        "90.Pad2 Warm",
        "91.Pad3 Polysynth",
        "92.Pad4 Choir",
        "93.Pad5 Bowed",
        "94.Pad6 Metallic",
        "95.Pad7 Halo",
        "96.Pad8 Sweep",
    ],
    
    "Synth F/X": [
        "97.FX1 Rain",
        "98.FX2 Soundtrack",
        "99.FX3 Crystal",
        "100.FX4 Atmosphere",
        "101.FX5 Brightness",
        "102.FX6 Goblins",
        "103.FX7 Echoes",
        "104.FX8 Sci-Fi",
    ],

    "Ethnic": [
        "105.Sitar",
        "106.Banjo",
        "107.Shamisen",
        "108.Koto",
        "109.Kalimba",
        "110. Bagpipe",
        "111. Fiddle",
        "112. Shanai",
    ],
    
    "Percussive": [
        "113.TinkerBell",
        "114.Agogo",
        "115.SteelDrums",
        "116.Woodblock",
        "117.TaikoDrum",
        "118.Melodic Tom",
        "119.SynthDrum",
        "120.Reverse Cymbal",
    ],
    
    "Sound F/X": [
        "121.Guitar Fret Noise",
        "122. Breath Noise",
        "123.Seashore",
        "124.BirdTweet",
        "125.Telephone",
        "126.Helicopter",
        "127.Applause",
        "128.Gunshot",
    ]
}

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
        return self.__str__()
    
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
    """
    _modo_mayor = [2,2,1,2,2,2,1]

    def __init__(self, tonica, grados, arpegiado='rasgueado'):
        self.arpegiado = 'rasgueado'
        self.tonica = tonica
        self.grados = grados
        self.notas = self.generar(tonica, grados)
    
    @classmethod    
    def generar(cls, tonica, grados):
        retorno = []
        
        escala = Escala.generar(tonica, cls._modo_mayor)
        
        for grado in grados:
            if type(grado) is int:
                orden = grado % len(cls._modo_mayor)
                octava = grado // len(cls._modo_mayor)
                alteracion = 0
                
            else:
                orden = int(grado[0]) % len(cls._modo_mayor)
                octava = orden // len(cls._modo_mayor)
                
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
        self.notas = notas

        
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


    dem = Matrix(tempo=180, pulso='corchea', volumen=100)
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


    p1 = Partitura(Seccion(duracion=16, pulsos=2, ritmo=4, rotacion=0, notas=[44]),
                    Seccion(duracion=16, pulsos=2, ritmo=4, rotacion=0, notas=[46]),
                )
    p2 = Partitura(Seccion(duracion=16, pulsos=1, ritmo=4, rotacion=1, notas=[36]),
                    Seccion(duracion=16, pulsos=4, ritmo=4, rotacion=0, notas=[36])
                )
    p3 = Partitura(Seccion(duracion=1, pulsos=1, ritmo=4, rotacion=2, notas=[38]),
                    # Seccion(duracion=4, pulsos=4, ritmo=4, rotacion=0, notas=[48, 45, 43, 41])
                )            
    p4 = Partitura(Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('E2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('E2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('E2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                    
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('D2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('F2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('C2')]),
                    Seccion(duracion=1, pulsos=8, ritmo=8, rotacion=0, notas=[Nota('Bb2')]),
                )
    p5 = Partitura(
                    Seccion(duracion=9, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('D3', [1,'3b',5]), Acorde('E3', [1,'3b',5]), Acorde('F3', [1,3,5])]),
                    Seccion(duracion=12, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('C3', [1,3,5]), Acorde('D3', [1,'3b',5]), Acorde('C3', [1,3,5]), Acorde('Bb3', [1,3,5])]),
                    Seccion(duracion=12, pulsos=1, ritmo=8, rotacion=0, notas=[Acorde('D4', [1,'3b',5]), Acorde('F4', [1,3,5]), Acorde('C4', [1,3,5]), Acorde('Bb4', [1,3,5])]),
    )

    # PET SEMATARY CHORDS
    # Dm, Em, F
    # C, Dm, C, Bb
    # Dm, F, C, Bb


    p1 = Partitura(Seccion(duracion=0, pulsos=6, ritmo=16, rotacion=0, notas=[36,37]),
                    # Seccion(duracion=1, pulsos=4, ritmo=4, rotacion=0, notas=[44]),
                )
    p2 = Partitura(Seccion(duracion=0, pulsos=4, ritmo=4, rotacion=0, notas=[44]),
                    # Seccion(duracion=1, pulsos=2, ritmo=4, rotacion=0, notas=[36,38])
                )


    dem.agregar_pista(Pista(nombre='Pista 1', partitura=p1, velocity=100, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 2', partitura=p2, velocity=100, channel=9, instrument=0))
    # dem.agregar_pista(Pista(nombre='Pista 3', partitura=p3, velocity=127, channel=9, instrument=0))
    dem.agregar_pista(Pista(nombre='Pista 4', partitura=p4, velocity=127, channel=1, instrument=33))
    dem.agregar_pista(Pista(nombre='Pista 5', partitura=p5, velocity=50, channel=2, instrument=29, duracion=7))
    dem.loop()

# if __name__ == "__main__":
    # testeos()