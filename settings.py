import pygame

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('doodle jump')
score = 0
scoreEnemy = 0
pygame.init()
pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(1)
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.2)
deadMostr_sound = pygame.mixer.Sound('sounds/deadMostr.wav')
deadMostr_sound.set_volume(0.2)
deadNLO_sound = pygame.mixer.Sound('sounds/deadNLO.wav')
deadNLO_sound.set_volume(0.2)
soundshoot = pygame.mixer.Sound('sounds/shot.wav')

pow_sound = pygame.mixer.Sound("sounds/pow.wav")
pow_sound.set_volume(0.2)

spring_sound = pygame.mixer.Sound("sounds/spring.wav")
spring_sound.set_volume(0.2)


bg = pygame.image.load("assets/background.png")
bg = pygame.transform.scale(bg, (800, 800))
bg2 = pygame.image.load("assets/secondLocation.png")
bg2 = pygame.transform.scale(bg2, (800, 800))
bg3 = pygame.image.load("assets/bk3.png")
bg3 = pygame.transform.scale(bg3, (800, 800))