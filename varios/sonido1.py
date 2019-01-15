import pygame

volumen = 1
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
sound = pygame.mixer.music.load('b.mp3')
vol = 0.0625
pygame.mixer.music.set_volume(vol)
pygame.init()

entrada = ''

while (entrada !='salir'):
	entrada = raw_input("> ")

	if (entrada == '1'):
		pygame.mixer.music.play(1)

	if (entrada == '2'):
		pygame.mixer.music.stop()

	if (entrada == '3'):
		vol  = vol + 0.0625
		pygame.mixer.music.set_volume(vol)
		pygame.mixer.music.play(1)
	
	if (entrada == '4'):
		vol  = vol - 0.0625
		pygame.mixer.music.set_volume(vol)
		pygame.mixer.music.play(1)
