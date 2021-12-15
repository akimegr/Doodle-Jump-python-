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

def drawBullet(bullet_png,x, y):
    screen.blit(bullet_png, (x+5, y))

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

