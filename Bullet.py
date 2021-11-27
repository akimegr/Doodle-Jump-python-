import pygame

class Bullet:
    def __init__(self, x, y, plY):
        self.y = y
        self.x = x
        self.realY = plY


    def move(self):
        self.y -= 100
        self.realY-=100

    def off_screen(self):
        return not self.y>0

