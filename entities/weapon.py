import pygame
import os
import sys
from random import *
from .fatbot import *
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


class WeaponCube(Sprite):
	def __init__(self, x, y):
		super().__init__(x-17, y-15, image=path("weapon_cube.png"))
		self.types = ["PeaShooter"]
	def update(self, screen):
		self.hitPlayer(screen)

	def hitPlayer(self, screen):
		for entity in screen:
			if isinstance(entity, Fatbot):
				if self.collide(entity):
					entity.weapon = choice(self.types)
					screen.remove(self)