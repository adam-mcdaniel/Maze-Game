import pygame
import os
import sys
from .wall import Wall
from .bullet import Bullet
from .fatbot import Fatbot
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import Surface
from easy_sdl.sprite import Screen
from easy_sdl.sprite import keyUp, keyDown


class Life(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, image=path("fatbot.png"))


class HealthBar(Surface):
	def __init__(self):
		self.lives = Fatbot.getFatbot().lives
		self.life_sprites = list(map(lambda a: Life(a * 96, Screen.getScreen().getHeight()-96), list(range(0, self.lives))))
		super().__init__(self.life_sprites)

	def update(self, screen):
		if Fatbot.getFatbot().lives < self.lives:
			self.life_sprites = self.pop()
			self.lives -= 1