import pygame
import os
import sys
import time as tm
from .boss import Boss
from .wall import Wall
from .bullet import Bullet
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


TheFatbot = None


class DamageAction:
    def __init__(self):
        self.start = tm.time()
        self.immune_time = 1
        self.immune = False
        self.last_time = 0

    def update(self, screen):
        if self.immune:
            if time.time() - self.last_time > self.immune_time:
                self.immune = False
        else:
            if Fatbot.getFatbot().collideEnemy(screen):
                Fatbot.getFatbot().damage()
                self.immune = True
                self.last_time = time.time()


class Fatbot(Sprite):
    def __init__(self, x, y):
        global TheFatbot
        super().__init__(x, y, image=path("fatbot.png"))
        # super(Sprite, self).__init__(x, y, image=path("fatbot.png"))
        self.xvel = 0
        self.yvel = 0
        self.direction = [0, 0]
        self.max_vel = 17

        self.shooting = False
        self.weapon = ""
        self.lives = 3
        TheFatbot = self

    def getFatbot():
        return TheFatbot

    def damage(self):
        self.lives -= 1

    def collideEnemy(self, screen):
        for entity in screen:
            if isinstance(entity, Boss):
                if self.collide(entity):
                    return True
        return False

    def death(self):
        pass

    def update(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if keyUp(event, pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)

            if keyUp(event, pygame.K_a):
                self.xvel = 0
            if keyUp(event, pygame.K_d):
                self.xvel = 0
            if keyUp(event, pygame.K_w):
                self.yvel = 0
            if keyUp(event, pygame.K_s):
                self.yvel = 0
            if keyUp(event, pygame.K_SPACE):
                self.shooting = False

            if keyDown(event, pygame.K_a):
                self.xvel = -self.max_vel
            if keyDown(event, pygame.K_d):
                self.xvel = self.max_vel
            if keyDown(event, pygame.K_w):
                self.yvel = -self.max_vel
            if keyDown(event, pygame.K_s):
                self.yvel = self.max_vel
            if keyDown(event, pygame.K_SPACE):
                self.shooting = True

        self.move(self.xvel, 0)
        self.hitWall(self.xvel, 0, screen)
        self.move(0, self.yvel)
        self.hitWall(0, self.yvel, screen)
        self.setDirection()

        if self.lives < 0:
            pass

    def shoot(self, screen):
        if self.shooting:
            if self.weapon == "PeaShooter":
                screen.append(Bullet(self.getPos(), self.direction))
            else:
                pass
        else:
            pass

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

    def setDirection(self):
        if self.xvel != 0 and self.yvel != 0:
            if self.xvel > 0:
                self.direction[0] = 1
            if self.xvel < 0:
                self.direction[0] = -1
            if self.yvel > 0:
                self.direction[1] = 1
            if self.yvel < 0:
                self.direction[1] = -1
        elif self.xvel == 0 and self.yvel == 0:
            if self.direction == [0, 0]:
                self.direction = [1, 0]
            if self.direction[0] != 0 and self.direction[1] != 0 :
                self.direction[1] = 0
        else:
            if self.xvel > 0:
                self.direction = [1, 0]
            if self.xvel < 0:
                self.direction = [-1, 0]
            if self.yvel > 0:
                self.direction = [0, 1]
            if self.yvel < 0:
                self.direction = [0, -1]


