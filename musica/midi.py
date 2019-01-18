import sys
import time
import random
import threading
import pygame.midi

pygame.midi.init()

player = pygame.midi.Output(0)

print(pygame.midi.get_count())

print(pygame.midi.get_device_info(0))
print(pygame.midi.get_device_info(1))

"""
redonda = 1
blanca = 1/2
negra = 1/4
corchea = 1/8
semicorchea = 1/16
fusa = 1/32
semifusa = 1/64

tempo = 140

140 = 140 negras en 60 segundos

1 negra = 2,34 
"""


player.set_instrument(0,channel=9)

# player.write([[[0xc0,0,0],20000],[[0x90,60,100],20500]])
# time.sleep(3)


for i in range(0,128):
    sys.stdout.write(str(i))
    sys.stdout.flush()
    
    player.note_on(i, 127, channel=9)
    time.sleep(0.1)
    player.note_off(i, 127, channel=9)
    
    sys.stdout.write("\b"*len(str(i)))

sys.stdout.write("\b"*3)
sys.stdout.write(" "*3)
sys.stdout.write("\b"*3)
 

def tocar_nota(nota):
    for i in range(0, 25):
        print(nota)
        player.note_on(nota, 127, channel=1)
        time.sleep(0.1)
        player.note_off(nota, 127, channel=1)
    
        print("asd")

        
hilo1 = threading.Thread(args=[35], target=tocar_nota)

time.sleep(3)
hilo1.start()



    
#del player

pygame.midi.quit()



