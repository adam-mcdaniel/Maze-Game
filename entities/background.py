import pygame
import os
import sys
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


class Background(Sprite):
    def __init__(self):
        super().__init__(0, 0, image=path("background.png"))