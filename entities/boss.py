import pygame
import os
import sys
from .wall import Wall
from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import AnimatedSprite
from easy_sdl.sprite import keyUp, keyDown


class Boss(Sprite):
    def __init__(self, x, y):
        # super().__init__(x, y, images=["brain.png",
        #                                "brain2.png",
        #                                "brain3.png",
        #                                "brain4.png"
        #                                ], frequency=0.25)
        super().__init__(x, y, image="boss.png")
        # super(Sprite, self).__init__(x, y, image=path("fatbot.png"))
        self.xvel = 0
        self.yvel = 0
        self.max_vel = 4

    def update(self, screen):
        self.move(self.xvel, 0)
        self.hitWall(self.xvel, 0, screen)
        self.move(0, self.yvel)
        self.hitWall(0, self.yvel, screen)

    def find_player(self, maze, player_pos):
        self_coords = maze.mazeCoords(self.getX(), self.getY())
        try:
            next_step = maze.getPath(self_coords[0], self_coords[1], player_pos[0], player_pos[1])[0]
            # print(next_step)
            # print(maze.getPath(self_coords[0], self_coords[1], player_pos[0], player_pos[1]))
            if next_step[0] > self_coords[0]:
                self.xvel = self.max_vel
            if next_step[0] < self_coords[0]:
                self.xvel = -self.max_vel
            if next_step[1] > self_coords[1]:
                self.yvel = self.max_vel
            if next_step[1] < self_coords[1]:
                self.yvel = -self.max_vel
        except Exception as e:
            self.xvel = 0
            self.yvel = 0

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