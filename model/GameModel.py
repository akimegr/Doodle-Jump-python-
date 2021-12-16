from util.settings import *
from util.Doodle import *
from util.JetPack import *
from util.NLO import *
from util.Spring import *
from util.Platform import *
from util.Bullets import *
from view.GameView import doodleDraw
from view.GameView import drawPlatforms, drawBullet, drawEnemies, drawJet, drawLose, drawStart, drawSpring, fillBackground

chanceJet = 970



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
                    chanceJet-=5
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

        drawEnemies(masEnemy,enemy,doodle, deadMostr_sound)

        drawJet(jetPack,doodle)

        if(masEnemy2):
            for newNlo in nlo.enemys:

                count = 0
                global checkSoungShoot
                if timeShootImg%15!=0:
                    # print(timeShootImg)
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
            drawSpring(spring,springForGreen,doodle)
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
                print("bul.x" + str(bul.x) + " bul.realY+" + str(bul.realY)+ " newNlo[0]" + str(newNlo[0]) + " newNlo[1]" + str(newNlo[1]))
                print("masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width()" + str(masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width()) + "masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width()" + str(masEnemy2[len(masEnemy2) - 1].enemyPlayer.get_width()))
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
                    bgX = bgS
                    fillBackground(score,bgX)
                elif (score <= 2000):
                    bgX = bgF
                    fillBackground(score,bgX)

                elif (score <= 1500):
                    bgX = bg3
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
                    score = 1
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

                self.check_kill()
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


