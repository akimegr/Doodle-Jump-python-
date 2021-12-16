from util.settings import screen
from util.settings import soundshoot
import pygame

def doodleDraw(doodle, ):
    if (doodle.direction == 2 and not doodle.playerDead and doodle.withoutJet):
        screen.blit(doodle.playerShoot, (doodle.playerx, doodle.playery - doodle.cameray))
        # if checkSoungShoot == 0:
        #     pygame.mixer.Sound.play(soundshoot)


    elif doodle.direction == 0 and not doodle.playerDead and doodle.withoutJet:
        # checkSoungShoot = 0
        if doodle.jump:
            screen.blit(doodle.playerRight_1, (doodle.playerx, doodle.playery - doodle.cameray))
        else:
            screen.blit(doodle.playerRight, (doodle.playerx, doodle.playery - doodle.cameray))

    elif (doodle.direction == 1 and not doodle.playerDead and doodle.withoutJet):
        checkSoungShoot = 0
        if doodle.jump:
            screen.blit(doodle.playerLeft_1, (doodle.playerx, doodle.playery - doodle.cameray))
        else:
            screen.blit(doodle.playerLeft, (doodle.playerx, doodle.playery - doodle.cameray))

    if (doodle.playerDead):
        screen.blit(doodle.playerDeadImg, (doodle.playerx, doodle.playery - doodle.cameray))
    if not doodle.withoutJet:
        if not doodle.direction:
            screen.blit(doodle.playerRightRacket, (doodle.playerx, doodle.playery - doodle.cameray))

        else:
            screen.blit(doodle.playerLeftRacket, (doodle.playerx, doodle.playery - doodle.cameray))



def drawPlatforms(p, plat, doodle):
    if p[2] == 0:  # прорисовка зелёных
        screen.blit(plat.green, (p[0], p[1] - doodle.cameray))
    elif p[2] == 1:  # прорисовка синих
        screen.blit(plat.blue, (p[0], p[1] - doodle.cameray))
    elif p[2] == 2:
        if not p[3]:
            screen.blit(plat.red, (p[0], p[1] - doodle.cameray))
        else:
            screen.blit(plat.red_1, (p[0], p[1] - doodle.cameray))

def drawBullet(bullet_png, x, y):
    screen.blit(bullet_png, (x+5, y))

def drawEnemies(masEnemy, enemy,doodle, deadMostr_sound):
    if (masEnemy):
        count = 0
        for enem in enemy.enemys:
            screen.blit(masEnemy[count].enemyPlayer, (enem[0], enem[1] - doodle.cameray - 53))

            if (doodle.visible and pygame.Rect(enem[0], enem[1], masEnemy[len(masEnemy) - 1].enemyPlayer.get_width(),
                                               masEnemy[len(masEnemy) - 1].enemyPlayer.get_height() - 53).colliderect(
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

def drawJet(jetPack, doodle):
    for jet in jetPack.jetPacks:
        screen.blit(jetPack.jetPackImg, (jet[0], jet[1] - doodle.cameray - 53))
        if doodle.visible and pygame.Rect(jet[0], jet[1], jetPack.jetPackImg.get_width(),
                                          jetPack.jetPackImg.get_height()).colliderect(
                pygame.Rect(doodle.playerx, doodle.playery, doodle.playerRight.get_width(),
                            doodle.playerRight.get_height())):
            doodle.jump = 100
            doodle.withoutJet = False

def drawLose(font2, font3, font4, check, lastResult, maxResult):
    screen.fill((255, 255, 255))
    screen.blit(font2.render(str("О НЕТ!!!"), -1, (255, 0, 0)), (300, 100))
    screen.blit(font2.render(str("ВЫ ПРОИГРАЛИ!!!"), -1, (255, 0, 0)), (250, 200))
    screen.blit(font3.render(str("Набрано очков " + str(check)), -1, (0, 255, 0)), (180, 300))
    screen.blit(font2.render(str("Последний результат: " + lastResult), -1, (255, 0, 0)), (190, 400))
    screen.blit(font3.render(str("Рекорд " + str(maxResult)), -1, (0, 0, 255)), (260, 500))
    screen.blit(font4.render(str("НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ"), -1, (255, 0, 0)), (20, 650))

def drawStart(font2, font3, font4, lastResult, maxResult2):
    screen.fill((255, 255, 255))
    screen.blit(font2.render(str("Последний результат: " + lastResult), -1, (255, 0, 0)), (190, 300))
    screen.blit(font3.render(str("Рекорд " + str(maxResult2)), -1, (0, 0, 255)), (260, 400))
    screen.blit(font4.render(str("НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ"), -1, (255, 0, 0)), (20, 550))

def drawSpring(spring, springForGreen, doodle):
    if spring[-1]:
        screen.blit(springForGreen.spring_1, (spring[0], spring[1] - doodle.cameray))
    else:
        screen.blit(springForGreen.spring, (spring[0], spring[1] - doodle.cameray))

def fillBackground(score, bg):
    if (score <= 700):
        screen.blit(bg, (0, 0))
    elif (score <= 1000):
        screen.blit(bg, (0, 0))
    elif (score <= 5000000):
        screen.blit(bg, (0, 0))

