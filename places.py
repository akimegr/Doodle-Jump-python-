import pygame

from util.settings import *
from util.Doodle import *
from util.JetPack import *
from util.NLO import *
from util.Spring import *
from util.Platform import *
from util.Bullets import *
from view.GameView import doodleDraw
from view.GameView import drawPlatforms, drawBullet,  drawLose, drawStart, drawSpring, fillBackground

chanceJet = 970
chanceGreenPlatfrom = 800


doodle = DoodleJump()
enemy = Enemy()
nlo = NLO()
jetPack = JetPack()
masEnemy = []
masEnemy2 = []
springForGreen = Spring()
plat = Platform()
checkForshot = 0
checkSoungShoot = 0




chanceEnemy = 940


class Game:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        self.font2 = pygame.font.SysFont("Arial", 42)
        self.font3 = pygame.font.SysFont("Arial", 62)
        self.font4 = pygame.font.SysFont("Arial", 45)
        self.bullet_png = pygame.image.load("../assets/ice-snow-16.png")
        self.bullet_png = pygame.transform.scale(self.bullet_png, (20,20))

    def updatePlayer(self):
        if not doodle.jump:
            doodle.playery += doodle.gravity
            doodle.gravity += 1
        elif doodle.jump:
            doodle.playery -= doodle.jump
            doodle.jump -= 1
        if(doodle.jump and doodle.withoutJet and doodle.withoutSpring):
            pygame.mixer.Sound.play(jump_sound)
        key = pygame.key.get_pressed()

        if key[K_RIGHT]:
            if doodle.xmovement < 12:  # максимальная скорость
                doodle.xmovement += 1
            doodle.direction = 0

        elif key[K_LEFT]:
            if doodle.xmovement > -12:
                doodle.xmovement -= 1
            doodle.direction = 1

        else:
            if doodle.xmovement > 0:
                doodle.xmovement -= 1
            elif doodle.xmovement < 0:
                doodle.xmovement += 1


        if doodle.playerx > 850:
            doodle.playerx = -50
        elif doodle.playerx < -50:
            doodle.playerx = 850
        doodle.playerx += doodle.xmovement
        if (doodle.withoutSpring and doodle.withoutJet and not doodle.playerDead):
            if doodle.playery - doodle.cameray <= 500:
                doodle.cameray -= 7
        elif (not doodle.withoutJet and not doodle.playerDead):
            if doodle.playery - doodle.cameray <= 500:
                doodle.cameray -= 90
                doodle.visible = False
                pygame.mixer.Sound.play(pow_sound)
        else:
            if doodle.playery - doodle.cameray <= 500:
                doodle.cameray -= 50
                doodle.visible = False
                pygame.mixer.Sound.play(spring_sound)


                # self.visible = False
        if (doodle.jump < 15 and not doodle.playerDead):
            doodle.withoutSpring = True
            doodle.withoutJet = True
            doodle.visible = True
        global checkDirection, checkSoungShoot

        doodleDraw(doodle)

    def updatePlatforms(self):
        for p in plat.platforms:
            rect = pygame.Rect(p[0], p[1], plat.green.get_width() - 10, plat.green.get_height())
            player = pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width() - 10,
                                 doodle.playerRight.get_height())
            if rect.colliderect(player) and doodle.gravity and doodle.playery < (
                    p[1] - doodle.cameray) and doodle.visible:
                if p[2] != 2:
                    doodle.jump = 15
                    doodle.gravity = 0
                else:
                    p[-1] = 1

            if(p[2]==2 and p[-1]==1):
                p[1]+=8

            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1



    def logicPlatforms(self, timeShootImg):
        global masEnemy2, masEnemy, chanceGreenPlatfrom, chanceEnemy, score, chanceJet
        for p in plat.platforms:
            check = plat.platforms[1][1] - doodle.cameray
            if check > 800:  # на какой высоте появляться
                platform = random.randint(0, 1000)
                if platform < chanceGreenPlatfrom:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2
                #
                plat.platforms.append([random.randint(0, 700), plat.platforms[-1][1] - 50, platform, 0])
                #
                coords3 = plat.platforms[-1]
                checkForJetPack = random.randint(0,1000)

                if(score%50000==1):
                    chanceJet-=5
                if (score % 50000 == 1):
                    chanceGreenPlatfrom-=100
                if (checkForJetPack > chanceJet and platform == 0):
                    jetPack.jetPacks.append([coords3[0], coords3[1] - 25, 0])
                #
                #
                coords2 = plat.platforms[-1]
                checkForEnemy = random.randint(0, 1000)

                if(score%350000==0):
                    chanceEnemy-=5
                if (checkForEnemy > chanceEnemy and platform == 0):
                    newEnemy = Enemy()
                    masEnemy.append(newEnemy)
                    enemy.enemys.append([coords2[0], coords2[1] - 25, 0])
                #
                coords = plat.platforms[-1]
                checkForNlo = random.randint(0, 1000)
                if (checkForNlo > 980 and platform == 0):
                    newEnemy = NLO()
                    masEnemy2.append(newEnemy)
                    nlo.enemys.append([coords2[0], coords2[1] - 25, 0])
                check = random.randint(0, 1000)
                if check > 950 and platform == 0:  # шанс рандом для пружины
                    springForGreen.springs.append([coords[0], coords[1] - 25, 0])
                plat.platforms.pop(0)
                score += 100
            drawPlatforms(p,plat, doodle)
        #

        # drawEnemies(masEnemy,enemy,doodle, deadMostr_sound)
        global scoreEnemy

        if (masEnemy):
            count = 0
            for enem in enemy.enemys:
                screen.blit(masEnemy[count].enemyPlayer, (enem[0], enem[1] - doodle.cameray - 53))
                if(doodle.visible and doodle.gravity and pygame.Rect(enem[0], enem[1],
                                                   masEnemy[len(masEnemy) - 1].enemyPlayer.get_width(),
                                                   masEnemy[
                                                       len(masEnemy) - 1].enemyPlayer.get_height() - 53).colliderect(
                    pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                                doodle.playerRight.get_height()))):
                    enem[0] = -1000
                    enem[1] = 1000
                    print(doodle.gravity)

                    scoreEnemy+=1

                elif (doodle.visible and pygame.Rect(enem[0], enem[1],
                                                   masEnemy[len(masEnemy) - 1].enemyPlayer.get_width(),
                                                   masEnemy[
                                                       len(masEnemy) - 1].enemyPlayer.get_height() - 53).colliderect(
                    pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                                doodle.playerRight.get_height()))):
                    pygame.mixer.Sound.play(deadMostr_sound)
                    doodle.jump = 20
                    doodle.cameray -= 20
                    doodle.gravity = 10
                    doodle.cameray += 10
                    doodle.visible = False
                    doodle.playerDead = True
                count += 1

        # drawJet(jetPack,doodle)

        for jet in jetPack.jetPacks:
            screen.blit(jetPack.jetPackImg, (jet[0], jet[1] - doodle.cameray - 53))
            if doodle.visible and pygame.Rect(jet[0], jet[1], jetPack.jetPackImg.get_width(),
                                              jetPack.jetPackImg.get_height()).colliderect(
                pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                            doodle.playerRight.get_height())):
                doodle.jump = 100
                doodle.withoutJet = False

        if(masEnemy2):
            for newNlo in nlo.enemys:

                count = 0
                global checkSoungShoot
                if timeShootImg%15!=0:
                    # print(timeShootImg)
                    screen.blit(masEnemy2[count].enemyPlayer, (newNlo[0], newNlo[1] - doodle.cameray - 53))

                if (doodle.visible and doodle.gravity and pygame.Rect(newNlo[0], newNlo[1],masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width(), masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_height() - 53).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),doodle.playerRight.get_height()))):

                        newNlo[0] = -1000
                        newNlo[1] = 1000
                        scoreEnemy += 1
                elif (doodle.visible and pygame.Rect(newNlo[0], newNlo[1],masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width(), masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_height() - 53).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),doodle.playerRight.get_height()))):
                    pygame.mixer.Sound.play(deadNLO_sound)
                    doodle.jump = 5
                    doodle.cameray -= 1
                    doodle.gravity = 1
                    doodle.cameray += 5
                    doodle.visible = False
                    doodle.playerDead = True
                    masEnemy2[count].enemyPlayer = nlo.enemyPlayerEnd
                count += 1



        #
        for spring in springForGreen.springs:
            drawSpring(spring,springForGreen,doodle)
            if doodle.visible and pygame.Rect(spring[0], spring[1], springForGreen.spring.get_width(), springForGreen.spring.get_height()).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),doodle.playerRight.get_height())):
                doodle.jump = 50
                doodle.withoutSpring = False

    def check_kill(self):
        global scoreEnemy
        for bul in doodle.bullets:

            countEnemy = 0
            for enem in enemy.enemys:
                if (pygame.Rect(bul.x, bul.realY, self.bullet_png.get_width(),
                               self.bullet_png.get_height()).colliderect(enem[0], enem[1],
                                masEnemy[len(masEnemy) - 1].enemyPlayer.get_width(),
                                    masEnemy[len(masEnemy) - 1].enemyPlayer.get_height())) or (doodle.visible and doodle.gravity and pygame.Rect(enem[0], enem[1],
                                                   masEnemy[len(masEnemy) - 1].enemyPlayer.get_width(),
                                                   masEnemy[
                                                       len(masEnemy) - 1].enemyPlayer.get_height() - 53).colliderect(
                    pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                                doodle.playerRight.get_height()))):
                    enem[0] = -1000
                    enem[1] = 1000
                    print(doodle.gravity)

                    doodle.bullets.remove(bul)
                    scoreEnemy+=1
                    break
                countEnemy+=1
            countEnemy = 0
            for newNlo in nlo.enemys:
               # print("self.bullet_png.get_width() "+str(masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width()) +" "+ str(masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_height()) )
                if pygame.Rect(bul.x, bul.realY, self.bullet_png.get_width(), self.bullet_png.get_height()).colliderect(newNlo[0], newNlo[1],  masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width(), masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_height() - 53):
                    newNlo[0] = -1000
                    newNlo[1] = 1000
                    doodle.bullets.remove(bul)
                    scoreEnemy+=1
                    break
                countEnemy += 1



    def run(self):

        start = False
        clock = pygame.time.Clock()
        plat.generatePlatforms()
        wait = True
        global score, scoreEnemy
        check = 0

        while True:
            timeShootImg=0
            key = pygame.key.get_pressed()

            for ev in pygame.event.get():
                if ev.type == QUIT:
                    sys.exit()

            if(key[K_SPACE]):
                wait = True
                start = True
                pygame.mixer.music.pause()
            if(key[K_ESCAPE]):
                pygame.quit()
                sys.exit()
            while wait:
                pygame.mixer.music.play(-1)
                clock.tick(60)
                key = pygame.key.get_pressed()
                for ev in pygame.event.get():
                    if ev.type == QUIT:
                        sys.exit()
                if(key[K_ESCAPE]):
                    wait = False
                    start = False
                if (score <= 700):
                    bgX = bg
                    fillBackground(score, bgX)
                elif (score <= 1000):
                    bgX = bgS
                    fillBackground(score,bgX)
                elif (score <= 1500):
                    bgX = bg3
                    fillBackground(score,bgX)
                elif (score <= 2000):
                    bgX = bgF
                    fillBackground(score,bgX)

                elif (score <= 3000):
                    bgX = bg2
                    fillBackground(score,bgX)
                elif (score <= 5000000):
                    bgX = bgE
                    fillBackground(score, bgX)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()

                if math.fabs(doodle.playery - doodle.cameray > 740):
                    global masEnemy2, masEnemy
                    doodle.cameray = 0
                    f = open("../res.txt", "ab+")
                    f.write((str(score) + '\n').encode())
                    f.close()
                    check = score
                    score = 0
                    scoreEnemy = 0
                    springForGreen.springs = []
                    enemy.enemys =[]

                    jetPack.jetPacks = []
                    nlo.enemys = []
                    nlo.enemyPlayer = pygame.image.load("../assets/nloFirst.png").convert_alpha()
                    masEnemy2 = []
                    masEnemy = []
                    doodle.bullets = []
                    plat.platforms = [[400, 500, 0, 0]]
                    plat.generatePlatforms()
                    doodle.playerx = 400
                    doodle.playery = 400
                    doodle.visible = True
                    doodle.playerDead = False
                    wait = False


                    # platform.drawGrid()
                self.check_kill()

                self.logicPlatforms(timeShootImg)
                self.updatePlayer()
                self.updatePlatforms()
                nlo.updateNlos()
                global checkForshot, checkSoungShoot
                if (doodle.direction != 2):
                    checkForshot = doodle.direction
                    # print(checkForshot)
                else:
                    if(timeShootImg%25==0):
                        checkSoungShoot += 1
                        doodle.direction = checkForshot
                        # print("d" + str(doodle.direction))
                doodle.shoot()
                # if(doodle.bullets):
                    # screen.blit(doodle.playerShoot, (doodle.playerx, doodle.playery - doodle.cameray))
                for bullet in doodle.bullets:
                    drawBullet(self.bullet_png,bullet.x, bullet.y)

                timeShootImg+=1

                screen.blit(self.font.render("Ваш счёт: "+str(score), -1, (0, 0, 0)), (25, 25))
                screen.blit(self.font.render("Убито врагов: "+str(scoreEnemy), -1, (0, 0, 0)), (25, 50))
                # print(doodle.direction)
                lastResult2 = lastResult()
                maxResult2 = maxResult()
                if(not wait):

                    drawLose(self.font2, self.font3, self.font4,check, str(lastResult2), maxResult())
                    pygame.mixer.music.unpause()

                if(not start):
                    wait = False
                    drawStart(self.font2, self.font3, self.font4, lastResult2, maxResult2)
                    pygame.mixer.music.unpause()


                pygame.display.flip()




class Bullet:
    def __init__(self, x, y, plY):
        self.y = y+5
        self.x = x+30
        self.realY = plY


    def move(self):
        self.y -= 20
        self.realY-=20

    def off_screen(self):
        return not self.y>0

import math

import pygame
from pygame.locals import *
import sys

from util.Bullets import Bullet


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

        if (key[K_SPACE] and self.cool_down_counts==0):
            bullet = Bullet(self.playerx, self.playery+math.fabs(self.cameray), self.playery)
            self.bullets.append(bullet)
            self.cool_down_counts = 1
            self.direction = 2


        for bullet in self.bullets:
            bullet.move()
            if(bullet.off_screen()):
                self.bullets.remove(bullet)


import random
import pygame

class Enemy:
    def __init__(self):
        check = random.randint(0,7)
        self.enemyPlayerEmpty = pygame.image.load("../assets/mnogon.png").convert_alpha()
        self.enemyPlayerEmpty = pygame.transform.scale(self.enemyPlayerEmpty,(0,0))
        self.enemyPlayer = 0
        if(check==0):
            self.enemyPlayer = pygame.image.load("../assets/mnogon.png").convert_alpha()
        elif(check==1):
            self.enemyPlayer = pygame.image.load("../assets/mostr1.png").convert_alpha()
        elif(check==2):
            self.enemyPlayer = pygame.image.load("../assets/mostr2.png").convert_alpha()
        elif(check==3):
            self.enemyPlayer = pygame.image.load("../assets/mostr3.png").convert_alpha()
        elif(check==4):
            self.enemyPlayer = pygame.image.load("../assets/mostr4.png").convert_alpha()
        elif(check==5):
            self.enemyPlayer = pygame.image.load("../assets/mostr5.png").convert_alpha()
        else:
            self.enemyPlayer = pygame.image.load("../assets/mosntr6.png").convert_alpha()

        self.enemys = []
        self.rect = self.enemyPlayer.get_rect()

import pygame

class JetPack:
    def __init__(self):
        self.jetPackImg = pygame.image.load("../assets/Jet.png").convert_alpha()
        self.jetPacks = []
        self.rect = self.jetPackImg.get_rect()

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

import pygame
import random

class Platform:

    def __init__(self):
        self.green = pygame.image.load("../assets/green.png").convert_alpha()
        self.platforms = [[400, 500, 0, 0]]

        self.blue = pygame.image.load(
            "../assets/blue.png").convert_alpha()  #ипикселей, что и на экране
        self.red = pygame.image.load("../assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("../assets/red_1.png").convert_alpha()



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


import pygame

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('doodle jump')
score = 1
scoreEnemy = 0
pygame.init()
pygame.mixer.music.load("../sounds/intro.mp3")
pygame.mixer.music.set_volume(1)
jump_sound = pygame.mixer.Sound('../sounds/jump.wav')
jump_sound.set_volume(0.2)
deadMostr_sound = pygame.mixer.Sound('../sounds/deadMostr.wav')
deadMostr_sound.set_volume(0.2)
deadNLO_sound = pygame.mixer.Sound('../sounds/deadNLO.wav')
deadNLO_sound.set_volume(0.2)
soundshoot = pygame.mixer.Sound('../sounds/shot.wav')

pow_sound = pygame.mixer.Sound("../sounds/pow.wav")
pow_sound.set_volume(0.2)

spring_sound = pygame.mixer.Sound("../sounds/spring.wav")
spring_sound.set_volume(0.2)


bg = pygame.image.load("../assets/background.png")
bg = pygame.transform.scale(bg, (800, 800))
bgS = pygame.image.load("../assets/soccer-bck@2x.png")
bgS = pygame.transform.scale(bgS, (800, 800))
bgF = pygame.image.load("../assets/underwater-bck@2x.png")
bgF = pygame.transform.scale(bgF, (800, 800))
bg2 = pygame.image.load("../assets/secondLocation.png")
bg2 = pygame.transform.scale(bg2, (800, 800))
bg3 = pygame.image.load("../assets/bk3.png")
bg3 = pygame.transform.scale(bg3, (800, 800))
bgE = pygame.image.load("../assets/space-bck@2x.png")
bgE = pygame.transform.scale(bgE, (800, 800))


def maxResult():
    f = open("../res.txt", "r")

    max = 0
    for i in f:
        i = i.strip("\n")
        max = int(max)
        if max < int(i):
            max = int(i)
    f.close()
    return str(max)

def lastResult():
    f = open("../res.txt", "r")
    a = []
    for i in f:
        a.append(i.strip('\n'))
    f.close()
    return a[len(a)-2]

import pygame


class Spring:
    def __init__(self):
        self.spring = pygame.image.load("../assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("../assets/spring_1.png").convert_alpha()
        self.springs = []