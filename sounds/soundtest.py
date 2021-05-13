import pygame, time

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init(44100, -16, 2, 512)
soundObj = pygame.mixer.Sound('pew.wav')
print('playing')
soundObj.play()
print('played')
time.sleep(3) #wait and let the sound play for X second
soundObj.stop()
