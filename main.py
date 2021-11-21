import time
import math

import pygame
from pygame.locals import *
import sys
import random

screen = pygame.display.set_mode((800, 800))

bg = pygame.image.load("assets/background.png")
bg = pygame.transform.scale(bg, (800, 800))
bg2 = pygame.image.load("assets/secondLocation.png")
bg2 = pygame.transform.scale(bg2, (800, 800))
bg3 = pygame.image.load("assets/bk3.png")
bg3 = pygame.transform.scale(bg3, (800, 800))

score = 0


class DoodleJump:
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
        self.withoutJet = True
        self.playerRightRacket = pygame.image.load("assets/racketright (2).png").convert_alpha()
        self.playerLeftRacket = pygame.image.load("assets/racket.png").convert_alpha()
        self.playerLeftRacket = pygame.transform.scale(self.playerLeftRacket, (150,150))
        self.playerRightRacket = pygame.transform.scale(self.playerRightRacket, (150,150))

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
        if (self.withoutSpring and self.withoutJet and not self.playerDead):
            if self.playery - self.cameray <= 500:
                self.cameray -= 5
        elif (not self.withoutJet and not self.playerDead):
            if self.playery - self.cameray <= 500:
                self.cameray -= 90
                self.visible = False
        else:
            if self.playery - self.cameray <= 500:
                self.cameray -= 50
                self.visible = False


                # self.visible = False
        if (self.jump < 15 and not self.playerDead):
            self.withoutSpring = True
            self.withoutJet = True
            self.visible = True
        if not self.direction and not self.playerDead and self.withoutJet:
            if self.jump:
                screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))

        elif self.direction and not self.playerDead and self.withoutJet:
            if self.jump:
                screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
        if (self.playerDead):
            screen.blit(self.playerDeadImg, (self.playerx, self.playery - self.cameray))
        if not self.withoutJet:
            if not self.direction:
                screen.blit(self.playerRightRacket, (self.playerx, self.playery-self.cameray))

            else:
                screen.blit(self.playerLeftRacket , (self.playerx, self.playery-self.cameray))



doodle = DoodleJump()

class JetPack:
    def __init__(self):
        self.jetPackImg = pygame.image.load("assets/Jet.png").convert_alpha()
        self.jetPacks = []
        self.rect = self.jetPackImg.get_rect()

class Enemy:
    def __init__(self):
        check = random.randint(0,7)
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
        self.enemyPlayer = pygame.transform.scale(self.enemyPlayer, (100, 100))
        self.enemyPlayer.set_colorkey((255, 255, 255))

# class NLO(Enemy):
#     super.enemyPlayer = pygame.image.load("assets/nlo.png").convert_alpha()


enemy = Enemy()
jetPack = JetPack()
masEnemy = []

class Spring:
    def __init__(self):
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()  # spring
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()  # spring
        self.springs = []
springForGreen = Spring()


class Platform:

    def __init__(self):
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        self.platforms = [[400, 500, 0, 0]]  # ширина где появ,

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
                coords3 = self.platforms[-1]
                checkForJetPack = random.randint(0,1000)

                if (checkForJetPack > 950 and platform == 0):
                    jetPack.jetPacks.append([coords3[0], coords3[1] - 25, 0])
                #
                #
                coords2 = self.platforms[-1]
                checkForEnemy = random.randint(0, 1000)

                if (checkForEnemy > 940 and platform == 0):
                    newEnemy = Enemy()
                    masEnemy.append(newEnemy)
                    enemy.enemys.append([coords2[0], coords2[1] - 25, 0])
                #
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 950 and platform == 0:  # шанс рандом для пружины
                    springForGreen.springs.append([coords[0], coords[1] - 25, 0])
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
        if(masEnemy):
            count = 0
            for enem in enemy.enemys:
                screen.blit(masEnemy[count].enemyPlayer, (enem[0], enem[1] - doodle.cameray - 53))
                if (doodle.visible and pygame.Rect(enem[0], enem[1], masEnemy[len(masEnemy)-1].enemyPlayer.get_width(), masEnemy[len(masEnemy)-1].enemyPlayer.get_height() - 53).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(), doodle.playerRight.get_height()))):
                    doodle.jump = 20
                    doodle.cameray -= 20
                    doodle.gravity = 10
                    doodle.cameray += 10
                    doodle.visible = False
                    doodle.playerDead = True
                count+=1


        for jet in jetPack.jetPacks:
            screen.blit(jetPack.jetPackImg, (jet[0],jet[1]-doodle.cameray-53) )
            if doodle.visible and pygame.Rect(jet[0],jet[1],jetPack.jetPackImg.get_width(), jetPack.jetPackImg.get_height()-53).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(), doodle.playerRight.get_height())):
                doodle.jump = 100
                doodle.withoutJet = False


        #
        for spring in springForGreen.springs:
            if spring[-1]:
                screen.blit(springForGreen.spring_1, (spring[0], spring[1] - doodle.cameray))
            else:
                screen.blit(springForGreen.spring, (spring[0], spring[1] - doodle.cameray))
            if doodle.visible and pygame.Rect(spring[0], spring[1], springForGreen.spring.get_width(), springForGreen.spring.get_height()).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),doodle.playerRight.get_height())):
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
        self.font2 = pygame.font.SysFont("Arial", 42)
        self.font3 = pygame.font.SysFont("Arial", 62)
        self.font4 = pygame.font.SysFont("Arial", 45)

    def maxResult(self):
        f = open("res.txt", "r")

        max = 0
        for i in f:
            i = i.strip("\n")
            max = int(max)
            if max<int(i):
                max = int(i)
        f.close()
        return str(max)

    def lastResult(self):
        f = open("res.txt", "r")
        a = []
        for i in f:
            a.append(i.strip('\n'))
        f.close()
        return a[len(a)-2]




    def run(self):
        start = False
        platform = Platform()
        clock = pygame.time.Clock()
        platform.generatePlatforms()
        wait = True
        global score
        check = 0

        while True:

            key = pygame.key.get_pressed()

            for ev in pygame.event.get():
                if ev.type == QUIT:
                    sys.exit()

            if(key[K_SPACE]):
                wait = True
                start = True
            while wait:
                clock.tick(60)
                if (score <= 700):
                    screen.blit(bg, (0, 0))
                elif (score <= 1000):
                    screen.blit(bg2, (0, 0))
                elif (score <= 5000000):
                    screen.blit(bg3, (0, 0))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()

                if math.fabs(doodle.playery - doodle.cameray > 740):
                    doodle.cameray = 0
                    f = open("res.txt", "ab+")
                    f.write((str(score) + '\n').encode())
                    f.close()
                    check = score
                    score = 0
                    springForGreen.springs = []
                    enemy.enemys =[]
                    jetPack.jetPacks = []
                    platform.platforms = [[400, 500, 0, 0]]
                    platform.generatePlatforms()
                    doodle.playerx = 400
                    doodle.playery = 400
                    doodle.visible = True
                    doodle.playerDead = False
                    wait = False


                    # platform.drawGrid()
                platform.drawPlatforms()
                doodle.updatePlayer()
                platform.updatePlatforms()
                screen.blit(self.font.render(str(doodle.playery), -1, (0, 0, 0)), (25, 25))
                screen.blit(self.font.render(str(doodle.cameray), -1, (0, 0, 0)), (200, 25))
                screen.blit(self.font.render(str(score), -1, (0, 0, 0)), (400, 25))
                if(not wait):
                    screen.fill((255, 255, 255))
                    screen.blit(self.font2.render(str("О НЕТ!!!"), -1, (255, 0, 0)), (300, 100))
                    screen.blit(self.font2.render(str("ВЫ ПРОИГРАЛИ!!!"), -1, (255, 0, 0)), (250, 200))
                    screen.blit(self.font3.render(str("Набрано очков " + str(check)), -1, (0, 255, 0)), (180, 300))
                    screen.blit(self.font2.render(str("Последний результат: " + self.lastResult()), -1, (255, 0, 0)), (190, 400))
                    screen.blit(self.font3.render(str("Рекорд " + str(self.maxResult())), -1, (0, 0, 255)), (260, 500))
                    screen.blit(self.font4.render(str("НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ"), -1, (255, 0, 0)), (20, 650))
                if(not start):
                    wait = False
                    screen.fill((255, 255, 255))
                    screen.blit(self.font2.render(str("Последний результат: " + self.lastResult()), -1, (255, 0, 0)), (190, 300))
                    screen.blit(self.font3.render(str("Рекорд " + str(self.maxResult())), -1, (0, 0, 255)), (260, 400))
                    screen.blit(self.font4.render(str("НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ"), -1, (255, 0, 0)), (20, 550))

                pygame.display.flip()



Game().run()
