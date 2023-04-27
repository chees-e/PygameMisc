import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    def __init__(self, x, y, type):
        Sprite.__init__(self)

        self.x = x
        self.y = y
        self.type = type
