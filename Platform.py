import pygame
import random

class Platform:

    def __init__(self):
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        self.platforms = [[400, 500, 0, 0]]  # ширина где появ,

        self.blue = pygame.image.load(
            "assets/blue.png").convert_alpha()  # platform move #используются для преобразования поверхностей в тот же формат пикселей, что и на экране
        self.red = pygame.image.load("assets/red.png").convert_alpha()  # platform hurt
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()  # platform hurt2



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

