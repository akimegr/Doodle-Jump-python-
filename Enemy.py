import random
import pygame

class Enemy:
    def __init__(self):
        check = random.randint(0,7)
        self.enemyPlayerEmpty = pygame.image.load("assets/mnogon.png").convert_alpha()
        self.enemyPlayerEmpty = pygame.transform.scale(self.enemyPlayerEmpty,(0,0))
        self.enemyPlayer = 0
        if(check==0):
            self.enemyPlayer = pygame.image.load("assets/mnogon.png").convert_alpha()
        elif(check==1):
            self.enemyPlayer = pygame.image.load("assets/mostr1.png").convert_alpha()
        elif(check==2):
            self.enemyPlayer = pygame.image.load("assets/mostr2.png").convert_alpha()
        elif(check==3):
            self.enemyPlayer = pygame.image.load("assets/mostr3.png").convert_alpha()
        elif(check==4):
            self.enemyPlayer = pygame.image.load("assets/mostr4.png").convert_alpha()
        elif(check==5):
            self.enemyPlayer = pygame.image.load("assets/mostr5.png").convert_alpha()
        else:
            self.enemyPlayer = pygame.image.load("assets/mosntr6.png").convert_alpha()

        self.enemys = []
        self.rect = self.enemyPlayer.get_rect()

