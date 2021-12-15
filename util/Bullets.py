
class Bullet:
    def __init__(self, x, y, plY):
        self.y = y
        self.x = x
        self.realY = plY


    def move(self):
        self.y -= 20
        self.realY-=20

    def off_screen(self):
        return not self.y>0

