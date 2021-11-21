import pygame

class JetPack:
    def __init__(self):
        self.jetPackImg = pygame.image.load("assets/Jet.png").convert_alpha()
        self.jetPacks = []
        self.rect = self.jetPackImg.get_rect()