import pygame
from pygame.locals import *


class DoodleJump:
    def __init__(self):
        self.visible = True
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.playerDeadImg = pygame.image.load("assets/deadDoodle.png").convert_alpha()
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
        self.playerRightRacket = pygame.image.load("assets/racketright (2).png").convert_alpha()
        self.playerLeftRacket = pygame.image.load("assets/racket.png").convert_alpha()
        self.playerLeftRacket = pygame.transform.scale(self.playerLeftRacket, (150,150))
        self.playerRightRacket = pygame.transform.scale(self.playerRightRacket, (150,150))



