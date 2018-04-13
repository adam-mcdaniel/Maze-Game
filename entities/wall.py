import pygame
import os
import sys
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


class Wall(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, image=path("brick.png"))
