import time
import math

import sys
import random
from settings import *
from Doodle import *
from JetPack import *
from Enemy import *
from NLO import *
from Spring import *
from Platform import *
from  Bullet import *
import pygame
from Bullet import *

chanceJet = 950



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
        self.bullet_png = pygame.image.load("assets/bac.png")
        self.bullet_png = pygame.transform.scale(self.bullet_png, (20,20))

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

        if(doodle.direction==2 and not doodle.playerDead and doodle.withoutJet):
            screen.blit(doodle.playerShoot, (doodle.playerx, doodle.playery - doodle.cameray))
            if checkSoungShoot == 0:
                pygame.mixer.Sound.play(soundshoot)


        elif doodle.direction==0 and not doodle.playerDead and doodle.withoutJet:
            checkSoungShoot = 0
            if doodle.jump:
                screen.blit(doodle.playerRight_1, (doodle.playerx, doodle.playery - doodle.cameray))
            else:
                screen.blit(doodle.playerRight, (doodle.playerx, doodle.playery - doodle.cameray))

        elif(doodle.direction==1 and not doodle.playerDead and doodle.withoutJet):
            checkSoungShoot = 0
            if doodle.jump:
                screen.blit(doodle.playerLeft_1, (doodle.playerx, doodle.playery - doodle.cameray))
            else:
                screen.blit(doodle.playerLeft, (doodle.playerx, doodle.playery - doodle.cameray))

        if (doodle.playerDead):
            screen.blit(doodle.playerDeadImg, (doodle.playerx, doodle.playery - doodle.cameray))
        if not doodle.withoutJet:
            if not doodle.direction:
                screen.blit(doodle.playerRightRacket, (doodle.playerx, doodle.playery-doodle.cameray))

            else:
                screen.blit(doodle.playerLeftRacket , (doodle.playerx, doodle.playery-doodle.cameray))


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
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawBullet(self, x, y):
        screen.blit(self.bullet_png, (x+5, y))

    def drawPlatforms(self, timeShootImg):
        global masEnemy2, masEnemy
        for p in plat.platforms:
            check = plat.platforms[1][1] - doodle.cameray
            if check > 800:  # на какой высоте появляться
                platform = random.randint(0, 1000)
                if platform < 800:
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
                global chanceEnemy, score, chanceJet
                if(score%350000==0):
                    chanceJet-=10
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
                if (checkForNlo > 970 and platform == 0):
                    newEnemy = NLO()
                    masEnemy2.append(newEnemy)
                    nlo.enemys.append([coords2[0], coords2[1] - 25, 0])
                check = random.randint(0, 1000)
                if check > 950 and platform == 0:  # шанс рандом для пружины
                    springForGreen.springs.append([coords[0], coords[1] - 25, 0])
                plat.platforms.pop(0)
                score += 100
            if p[2] == 0:  # прорисовка зелёных
                screen.blit(plat.green, (p[0], p[1] - doodle.cameray))
            elif p[2] == 1:  # прорисовка синих
                screen.blit(plat.blue, (p[0], p[1] - doodle.cameray))
            elif p[2] == 2:
                if not p[3]:
                    screen.blit(plat.red, (p[0], p[1] - doodle.cameray))
                else:
                    screen.blit(plat.red_1, (p[0], p[1] - doodle.cameray))
        #
        if(masEnemy):
            count = 0
            for enem in enemy.enemys:
                screen.blit(masEnemy[count].enemyPlayer, (enem[0], enem[1] - doodle.cameray - 53))

                if (doodle.visible and pygame.Rect(enem[0], enem[1], masEnemy[len(masEnemy)-1].enemyPlayer.get_width(), masEnemy[len(masEnemy)-1].enemyPlayer.get_height() - 53).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(), doodle.playerRight.get_height()))):
                    pygame.mixer.Sound.play(deadMostr_sound)
                    doodle.jump = 20
                    doodle.cameray -= 20
                    doodle.gravity = 10
                    doodle.cameray += 10
                    doodle.visible = False
                    doodle.playerDead = True
                count+=1


        for jet in jetPack.jetPacks:
            screen.blit(jetPack.jetPackImg, (jet[0],jet[1]-doodle.cameray-53) )
            if doodle.visible and pygame.Rect(jet[0],jet[1],jetPack.jetPackImg.get_width(), jetPack.jetPackImg.get_height()).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(), doodle.playerRight.get_height())):
                doodle.jump = 100
                doodle.withoutJet = False

        if(masEnemy2):
            for newNlo in nlo.enemys:

                count = 0
                global checkSoungShoot
                if timeShootImg%15!=0:
                    print(timeShootImg)
                    screen.blit(masEnemy2[count].enemyPlayer, (newNlo[0], newNlo[1] - doodle.cameray - 53))


                if (doodle.visible and pygame.Rect(newNlo[0], newNlo[1],masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width(), masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_height() - 53).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),doodle.playerRight.get_height()))):
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
            if spring[-1]:
                screen.blit(springForGreen.spring_1, (spring[0], spring[1] - doodle.cameray))
            else:
                screen.blit(springForGreen.spring, (spring[0], spring[1] - doodle.cameray))
            if doodle.visible and pygame.Rect(spring[0], spring[1], springForGreen.spring.get_width(), springForGreen.spring.get_height()).colliderect(pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),doodle.playerRight.get_height())):
                doodle.jump = 50
                doodle.withoutSpring = False

    def check_kill(self):
        global scoreEnemy
        for bul in doodle.bullets:

            countEnemy = 0
            for enem in enemy.enemys:
                if pygame.Rect(bul.x, bul.realY, self.bullet_png.get_width(), self.bullet_png.get_height()).colliderect(enem[0], enem[1], masEnemy[len(masEnemy) - 1].enemyPlayer.get_width(), masEnemy[len(masEnemy) - 1].enemyPlayer.get_height()):
                    enem[0] = -1000
                    enem[1] = 1000

                    doodle.bullets.remove(bul)
                    scoreEnemy+=1
                    break
                countEnemy+=1
            countEnemy = 0
            for newNlo in nlo.enemys:

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
                    screen.blit(bg, (0, 0))
                elif (score <= 1000):
                    screen.blit(bg2, (0, 0))
                elif (score <= 5000000):
                    screen.blit(bg3, (0, 0))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()

                if math.fabs(doodle.playery - doodle.cameray > 740):
                    global masEnemy2, masEnemy
                    doodle.cameray = 0
                    f = open("res.txt", "ab+")
                    f.write((str(score) + '\n').encode())
                    f.close()
                    check = score
                    score = 0
                    scoreEnemy = 0
                    springForGreen.springs = []
                    enemy.enemys =[]

                    jetPack.jetPacks = []
                    nlo.enemys = []
                    nlo.enemyPlayer = pygame.image.load("assets/nloFirst.png").convert_alpha()
                    masEnemy2 = []
                    masEnemy = []
                    plat.platforms = [[400, 500, 0, 0]]
                    plat.generatePlatforms()
                    doodle.playerx = 400
                    doodle.playery = 400
                    doodle.visible = True
                    doodle.playerDead = False
                    wait = False


                    # platform.drawGrid()
                self.drawPlatforms(timeShootImg)
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
                    self.drawBullet(bullet.x, bullet.y)

                self.check_kill()
                timeShootImg+=1

                screen.blit(self.font.render("Ваш счёт: "+str(score), -1, (0, 0, 0)), (25, 25))
                screen.blit(self.font.render("Убито врагов: "+str(scoreEnemy), -1, (0, 0, 0)), (25, 50))
                # print(doodle.direction)

                if(not wait):
                    screen.fill((255, 255, 255))
                    screen.blit(self.font2.render(str("О НЕТ!!!"), -1, (255, 0, 0)), (300, 100))
                    screen.blit(self.font2.render(str("ВЫ ПРОИГРАЛИ!!!"), -1, (255, 0, 0)), (250, 200))
                    screen.blit(self.font3.render(str("Набрано очков " + str(check)), -1, (0, 255, 0)), (180, 300))
                    screen.blit(self.font2.render(str("Последний результат: " + self.lastResult()), -1, (255, 0, 0)), (190, 400))
                    screen.blit(self.font3.render(str("Рекорд " + str(self.maxResult())), -1, (0, 0, 255)), (260, 500))
                    screen.blit(self.font4.render(str("НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ"), -1, (255, 0, 0)), (20, 650))
                    pygame.mixer.music.unpause()

                if(not start):
                    wait = False
                    screen.fill((255, 255, 255))
                    screen.blit(self.font2.render(str("Последний результат: " + self.lastResult()), -1, (255, 0, 0)), (190, 300))
                    screen.blit(self.font3.render(str("Рекорд " + str(self.maxResult())), -1, (0, 0, 255)), (260, 400))
                    screen.blit(self.font4.render(str("НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ"), -1, (255, 0, 0)), (20, 550))
                    pygame.mixer.music.unpause()


                pygame.display.flip()



Game().run()
