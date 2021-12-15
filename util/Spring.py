import pygame


class Spring:
    def __init__(self):
        self.spring = pygame.image.load("../assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("../assets/spring_1.png").convert_alpha()
        self.springs = []