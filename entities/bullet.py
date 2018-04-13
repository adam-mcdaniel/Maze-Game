import pygame
import os
import sys
from .wall import *
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


class Bullet(Sprite):
    def __init__(self, pos, direction):
        super().__init__(pos[0]+direction[0]*16+96/2-16, pos[1]+direction[1]*16+96/2-16, image=path("bullet.png"))
        self.xvel = direction[0] * 32
        self.yvel = direction[1] * 32

    def update(self, screen):
    	self.move(self.xvel, self.yvel)
    	self.hitWall(screen)

    def hitWall(self, screen):
        for entity in screen:
            if isinstance(entity, Wall):
                if self.collide(entity):
                	screen.remove(self)