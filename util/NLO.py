import pygame
from util.Enemy import *

class NLO(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.enemyPlayerEnd = pygame.image.load("../assets/nlo.png").convert_alpha()
        self.enemyPlayer = pygame.image.load("../assets/nloFirst.png").convert_alpha()
    def updateNlos(self):
        for p in self.enemys:
                if(p[0]%3==0):
                    # print(p[0])
                    self.enemyPlayer = pygame.image.load("../assets/bac.png")
                else:
                    self.enemyPlayer = pygame.image.load("../assets/nloFirst.png").convert_alpha()
                if p[-1] == 1:
                    p[0] += 1
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 1
                    if p[0] <= 0:
                        p[-1] = 1
