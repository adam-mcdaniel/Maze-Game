import pygame
import os
import sys
import math
from .wall import Wall
from random import *
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


def getXVelocity(speed, angle): return speed * math.sin(math.radians(abs(angle)))
def getYVelocity(speed, angle): return speed * math.cos(math.radians(abs(angle)))


def orbit(angle, tangent_angle, x0, y0, x, y):
	turn = 0
	if ((x-x0 > 0) and (y-y0 < 0)):
		turn = -90-angle-math.degrees(math.atan2((y0-y),(x0-x)))+tangent_angle
	if ((x-x0 < 0) and (y-y0 > 0)):
		turn = 180-angle+(90-(math.degrees(math.atan2((y0-y),(x0-x)))))+tangent_angle
	if ((x-x0 > 0) and (y-y0 > 0)):
		turn = -90-angle-math.degrees(math.atan2((y0-y),(x0-x)))+tangent_angle
	if ((x-x0 < 0) and (y-y0 < 0)):
		turn = 180-angle+(90-(math.degrees(math.atan2((y0-y),(x0-x)))))+tangent_angle

	angle += turn
	if angle > 360:
		angle += -360
	if angle < 0:
		angle += 360

	if angle % 90 == 0:
		angle += 10

	return getXVelocity(1, angle), getYVelocity(1, angle)


class Follower(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, image=path("follower.png"))
        # super(Sprite, self).__init__(x, y, image=path("fatbot.png"))
        self.xvel = 0
        self.yvel = 0
        self.angle = 0
        self.max_vel = 18

    def update(self, screen):
        # self.move(self.xvel, 0)
        # self.hitWall(self.xvel, 0, screen)
        # self.move(0, self.yvel)
        # self.hitWall(0, self.yvel, screen)
        self.move(self.xvel,
        		  self.yvel)

    def follow(self, entity):
    	tangent_angle = 90
    	if self.getDistance(entity) > 100:
    		tangent_angle = 60
    	else:
    		tangent_angle = 95
    	self.xvel, self.yvel = orbit(self.angle,
			tangent_angle,
			self.rect.x,
			self.rect.y,
			entity.rect.x+96/2,
			entity.rect.y+96/2)

    	self.xvel *= self.max_vel * uniform(0.5, 1.5)
    	self.yvel *= self.max_vel * uniform(0.5, 1.5)


    def hitWall(self, xvel, yvel, screen):
        for entity in screen:
            if isinstance(entity, Wall):
                if self.collide(entity):
                    if xvel > 0:
                        self.rect.right = entity.rect.left
                    if xvel < 0:
                        self.rect.left = entity.rect.right
                    if yvel > 0:
                        self.rect.bottom = entity.rect.top
                    if yvel < 0:
                        self.rect.top = entity.rect.bottom