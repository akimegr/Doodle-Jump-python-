import math

import pygame
from pygame.locals import *

import sys

from util.Bullets import Bullet

soundshoot = pygame.mixer.Sound('../sounds/coin.wav')
soundshoot.set_volume(0.7)

class DoodleJump:
    def __init__(self):
        self.visible = True
        self.playerRight = pygame.image.load("../assets/ice-right_2x.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("../assets/ice-right-odskok_2x.png").convert_alpha()
        self.playerLeft = pygame.image.load("../assets/ice-left_2x.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("../assets/ice-left-odskok_2x.png").convert_alpha()
        self.playerDeadImg = pygame.image.load("../assets/deadDoodle.png").convert_alpha()
        self.playerShoot = pygame.image.load("../assets/ice-puca_2x.png").convert_alpha()
        self.playerShoot = pygame.transform.scale(self.playerShoot,(90,90))
        self.playerDead = False
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.withoutSpring = True
        self.withoutJet = True
        self.playerRightRacket = pygame.image.load("../assets/racketright (2).png").convert_alpha()
        self.playerLeftRacket = pygame.image.load("../assets/racket.png").convert_alpha()
        self.playerLeftRacket = pygame.transform.scale(self.playerLeftRacket, (150,150))
        self.playerRightRacket = pygame.transform.scale(self.playerRightRacket, (150,150))
        self.bullets = []
        self.cool_down_counts = 0
        self.continuesKillEneme = False

    def coolDown(self):
        if self.cool_down_counts > 50:
           self.cool_down_counts = 0
        elif self.cool_down_counts > 0:
           self.cool_down_counts += 1

    def shoot(self):
        key = pygame.key.get_pressed()
        self.coolDown()
        for ev in pygame.event.get():
            if ev.type == QUIT:
                sys.exit()

        if (key[K_SPACE] and self.cool_down_counts==0 and not self.playerDead and self.withoutJet and self.withoutSpring):

            bullet = Bullet(self.playerx, self.playery+math.fabs(self.cameray), self.playery)
            pygame.mixer.Sound.play(soundshoot)
            self.bullets.append(bullet)
            self.cool_down_counts = 1
            self.direction = 2


        for bullet in self.bullets:
            bullet.move()
            if(bullet.off_screen()):
                self.bullets.remove(bullet)
