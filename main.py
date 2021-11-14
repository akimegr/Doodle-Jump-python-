import time
import math

import pygame
from pygame.locals import *
import sys
import random

screen = pygame.display.set_mode((800, 800))

bg = pygame.image.load("assets/background.png")
bg = pygame.transform.scale(bg, (800, 800))
score = 0


class DoodleJump1:
    def __init__(self):
        self.visible = True
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()  # player
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()  # player
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()  # player
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()  # player
        self.playerDeadImg = pygame.image.load("assets/deadDoodle.png").convert_alpha()
        self.playerDead = False
        self.direction = 0  # player
        self.playerx = 400  # player
        self.playery = 400  # player
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.withoutSpring = True

    def updatePlayer(self):

        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1  # вниз
        elif self.jump:
            self.playery -= self.jump  # вверх?
            self.jump -= 1
        key = pygame.key.get_pressed()  # для зажатия клавиши
        if key[K_RIGHT]:
            if self.xmovement < 12:  # максимальная скорость
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -12:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if (self.withoutSpring):
            if self.playery - self.cameray <= 500:
                self.cameray -= 5
        else:
            if self.playery - self.cameray <= 500:
                self.cameray -= 50
                # self.visible = False
        if (self.jump < 2):
            self.withoutSpring = True
        if not self.direction and not self.playerDead:
            if self.jump:
                screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        elif self.direction and not self.playerDead:
            if self.jump:
                screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
        if (self.playerDead):
            screen.blit(self.playerDeadImg, (self.playerx, self.playery - self.cameray))


doodle = DoodleJump1()


class Enemy:
    def __init__(self):
        self.enemyPlayer = pygame.image.load("assets/mnogon.png").convert_alpha()
        self.enemys = []
        self.rect = self.enemyPlayer.get_rect()
        self.enemyPlayer = pygame.transform.scale(self.enemyPlayer, (100, 100))
        self.enemyPlayer.set_colorkey((255, 255, 255))


enemy = Enemy()


class Platform:
    def __init__(self):
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        self.platforms = [[400, 500, 0, 0]]  # ширина где появ,
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()  # spring
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()  # spring
        self.springs = []
        self.blue = pygame.image.load(
            "assets/blue.png").convert_alpha()  # platform move #используются для преобразования поверхностей в тот же формат пикселей, что и на экране
        self.red = pygame.image.load("assets/red.png").convert_alpha()  # platform hurt
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()  # platform hurt2

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width() - 10,
                                 doodle.playerRight.get_height())
            if rect.colliderect(player) and doodle.gravity and doodle.playery < (
                    p[1] - doodle.cameray) and doodle.visible:
                if p[2] != 2:
                    doodle.jump = 15
                    doodle.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - doodle.cameray
            if check > 800:  # на какой высоте появляться
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2
                #
                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                #
                coords2 = self.platforms[-1]
                check2 = random.randint(0, 1000)

                if (check2 > 950 and platform == 0):
                    enemy.enemys.append([coords2[0], coords2[1] - 25, 0])
                #
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:  # шанс рандом для пружины
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                global score
                score += 100
            if p[2] == 0:  # прорисовка зелёных
                screen.blit(self.green, (p[0], p[1] - doodle.cameray))
            elif p[2] == 1:  # прорисовка синих
                screen.blit(self.blue, (p[0], p[1] - doodle.cameray))
            elif p[2] == 2:
                if not p[3]:
                    screen.blit(self.red, (p[0], p[1] - doodle.cameray))
                else:
                    screen.blit(self.red_1, (p[0], p[1] - doodle.cameray))
        #
        for enem in enemy.enemys:
            screen.blit(enemy.enemyPlayer, (enem[0], enem[1] - doodle.cameray - 69))
            if (doodle.visible and pygame.Rect(enem[0], enem[1], enemy.enemyPlayer.get_width(),
                                               enemy.enemyPlayer.get_height() - 69).colliderect(
                    pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                                doodle.playerRight.get_height()))):
                doodle.jump = 20
                doodle.cameray -= 20
                doodle.gravity = 10
                doodle.cameray += 10
                doodle.visible = False
                doodle.playerDead = True

                # while doodle.cameray!=0:
                #     doodle.cameray+=1
                #     doodle.playery+=1
                #     doodle.updatePlayer()
                #
                # score = 0
                # self.springs = []
                # self.platforms = [[400, 500, 0, 0]]
                # self.generatePlatforms()
                # doodle.playerx = 400
                # doodle.playery = 400
        #
        for spring in self.springs:
            if spring[-1]:
                screen.blit(self.spring_1, (spring[0], spring[1] - doodle.cameray))
            else:
                screen.blit(self.spring, (spring[0], spring[1] - doodle.cameray))
            if doodle.visible and pygame.Rect(spring[0], spring[1], self.spring.get_width(),
                                              self.spring.get_height()).colliderect(
                    pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                                doodle.playerRight.get_height())):
                doodle.jump = 50
                doodle.withoutSpring = False

    def generatePlatforms(self):  # генерация первых платформ
        on = 800
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0  # зеленые
            elif platform < 900:
                platform = 1  # синие
            else:
                platform = 2  # красные
            self.platforms.append([x, on, platform, 0])
            on -= 50


class Game:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)

    def run(self):
        start = True
        platform = Platform()
        clock = pygame.time.Clock()
        platform.generatePlatforms()
        while True:
            clock.tick(60)
            screen.fill([255, 255, 255])
            screen.blit(bg, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if math.fabs(doodle.playery - doodle.cameray > 700):
                global score
                doodle.cameray = 0
                score = 0
                platform.springs = []
                platform.platforms = [[400, 500, 0, 0]]
                platform.generatePlatforms()
                doodle.playerx = 400
                doodle.playery = 400
                doodle.visible = True
                doodle.playerDead = False

            # platform.drawGrid()
            platform.drawPlatforms()
            doodle.updatePlayer()
            platform.updatePlatforms()
            screen.blit(self.font.render(str(doodle.playery), -1, (0, 0, 0)), (25, 25))
            screen.blit(self.font.render(str(doodle.cameray), -1, (0, 0, 0)), (200, 25))
            screen.blit(self.font.render(str(score), -1, (0, 0, 0)), (400, 25))
            pygame.display.flip()


Game().run()
