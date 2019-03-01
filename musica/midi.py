import sys
import time
import random
import threading
import pygame.midi

from ritmosEuclideos import *

from escalasGenerator import *

"""
redonda = 1
blanca = 1/2
negra = 1/4
corchea = 1/8
semicorchea = 1/16
fusa = 1/32
semifusa = 1/64
"""

tempo = 200
segundos = (60 / tempo) * 1000

figuras = {
    'redonda': int(segundos * 4),
    'blanca': int(segundos * 2),
    'negra': int(segundos),
    'corchea': int(segundos / 2),
    'semicorchea': int(segundos / 4),
    'fusa': int(segundos / 8),
    'semifusa': int(segundos / 16)
}

print(figuras)
#140 = 140 negras en 60 segundos
#1 negra = 2,34 




# player.write([[[0xc0,0,0],20000],[[0x90,60,100],20500]])
# time.sleep(3)


# for i in range(0,128):
    # sys.stdout.write(str(i))
    # sys.stdout.flush()
    
    # player.note_on(i, 127, channel=9)
    # time.sleep(0.1)
    # player.note_off(i, 127, channel=9)
    
    # sys.stdout.write("\b"*len(str(i)))

# sys.stdout.write("\b"*3)
# sys.stdout.write(" "*3)
# sys.stdout.write("\b"*3)
 

def tocar_nota(nota):
    for i in range(0, 25):
        print(nota)
        player.note_on(nota, 127, channel=1)
        time.sleep(0.1)
        player.note_off(nota, 127, channel=1)
    
        print("asd")

        
# hilo1 = threading.Thread(args=[35], target=tocar_nota)

# hilo1.start()

pygame.midi.init()

player = pygame.midi.Output(0)

print(pygame.midi.get_count())

print(pygame.midi.get_device_info(0))
print(pygame.midi.get_device_info(1))


player.set_instrument(0,channel=9)

tick = 0
"""
a = Euclideo(3,7)
b = Euclideo(3,7)
c = Euclideo(1,7)
d = Euclideo(1,4)

notaa = Euclideo(1,14)
notab = Euclideo(5, 14)
notac = Euclideo(8, 14)

escala = Escala('mayor', 'C3')
escala2 = EscalaCustom([2,2,1,2,2,2,1,2,2,1,2,2,2,1], 'C4')
escala3 = EscalaCustom([12,0,12,0,12], 'C2')

b.rotar(2)
c.rotar(4)


print(a)
print(b)
print(c)
print(d)
print(notaa)
print(notab)
print(notac)
print(escala)
print(escala2)
print(escala3)
"""

for i in range(0, 128):
    """
        La formula general es:
            frecuencia = 440hz * (a ** n)
            
        donde:
            - 440hz es la frecuencia de A4 (Afinacion estandar con A4 = 440Hz)
            - a es 2 ** (1/12). este numero es fijo.
            - n son los semitonos de separacion entre A4 y la nota que se busca obtener su frecuencia.
        
    """
    n = i - 69
    print(i, 440 * ((2**(1/12)) ** n))
    
    
    player.note_on(i, 127, channel=1)
    pygame.time.delay(figuras['semicorchea'])

contador = 0
while True:
    # if(tick % 32 == 0):
        # player.note_on(44, 127, channel=9)
        # player.write_short(0x90,63,100)
        # player.write_short(0x80,65,100)
    
    # if(tick % 64 == 0):
        # player.note_on(40, 127, channel=9)
        # player.write_short(0x90,65,100)
        # player.write_short(0x80,65,100)
    
    if next(a):
        player.note_on(42, 127, channel=9)
        
    if next(b):
        player.note_on(37, 127, channel=9)
        
    if next(c):
        player.note_on(36, 80, channel=9) 
    
    if next(d):
        player.note_on(42, 127, channel=9)

    if next(notaa):
        # contador = (contador + 2) % 6
        # player.note_on(32 + contador, 127, channel=1)
        next(escala).reproducir(player)
    
    if next(notab):
        next(escala2).reproducir(player)
        
    if next(notac):
        next(escala3).reproducir(player)
        # notac.rotar(2)
        
    pygame.time.delay(figuras['corchea'])
    tick += 1

   
"""

figuras = {
    'redonda': 64,
    'blanca': 32,
    'negra': 16,
    'corchea': 8,
    'semicorchea': 4,
    'fusa': 2,
    'semifusa': 1
}
 
"""
 
class Cancion:    
    def __init__(self):
        self.partitura = []
        self.duracion = 0
        self.loop = False
    
    def reproducir(self):
        pass
    
    
    
del player

pygame.midi.quit()

