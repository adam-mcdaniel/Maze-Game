import pygame
import easy_sdl
import maze
import sys
import os
from random import *
from entities import *

from entities.fatbot import *
from entities.wall import Wall
from entities.boss import Boss
from entities.weapon import WeaponCube
from entities.follower import Follower
from entities.healthbar import HealthBar
from entities.background import Background

from easy_sdl.tools import *
from easy_sdl.sprite import Sprite
from easy_sdl.sprite import keyUp, keyDown


MAZE_WIDTH, MAZE_HEIGHT = 4, 4

CELL_SIZE = 256
LEVEL_WIDTH, LEVEL_HEIGHT = 2 * (CELL_SIZE * MAZE_WIDTH) + CELL_SIZE, 2 * (CELL_SIZE * MAZE_HEIGHT) + CELL_SIZE

setup = {
         "level_width": LEVEL_WIDTH,
         "level_height": LEVEL_HEIGHT,
         "win_width": 1280,
         "win_height": 800,
         "maze_dimensions": (MAZE_WIDTH, MAZE_HEIGHT),
         }


class Game:
    def __init__(self, setup):
        self.map = self.GenerateMap(setup["maze_dimensions"])
        self.maze = maze.Maze(self.map, CELL_SIZE)
        # print('\n'.join(self.map))
        # coords = self.maze.getRandomSpace()
        # print(self.maze.mazeCoords(coords[0], coords[1]))
        # print('\n'.join(list(map(str, self.maze.true_maze))))
        self.screen = easy_sdl.setup.setup(win_width=setup["win_width"],
                                           win_height=setup["win_height"],
                                           level_width=setup["level_width"],
                                           level_height=setup["level_height"],
                                           full_screen=True)
        self.screen.add(self.convertMap(self.map))
        self.run()

    def GenerateMap(self, dimensions):
        map_string = maze.MakeMaze(dimensions).split("\n")
        for i, line in enumerate(map_string):
            if line == "\n":
                del map_string[i]

        map_string = list(filter(lambda line: line != "\n" and line != "",
                            map_string))
        return map_string

    def convertMap(self, m):
        walls = []
        x, y = 0, 0
        for line in m:
            for column in line:
                if column in ["+", "|", "-"]:
                    walls.append(Wall(x, y))
                x += CELL_SIZE
            y += CELL_SIZE
            x = 0
        return walls

    def run(self):
        player = Fatbot(CELL_SIZE, CELL_SIZE)
        self.screen.append(player)

        Bosses = []
        random_pos = self.maze.getRandomSpace()
        Bosses.append(Boss(random_pos[0], random_pos[1]))
        self.screen.add(Bosses)

        self.screen.addAction(TimedAction(0.25, lambda screen: player.shoot(screen)))
        self.screen.addAction(DamageAction())
        self.screen.addSurface(HealthBar())

        cubes = []
        random_pos = self.maze.getRandomSpace()
        cubes.append(WeaponCube(random_pos[0]+CELL_SIZE/2, random_pos[1]+CELL_SIZE/2))
        random_pos = self.maze.getRandomSpace()
        cubes.append(WeaponCube(random_pos[0]+CELL_SIZE/2, random_pos[1]+CELL_SIZE/2))
        random_pos = self.maze.getRandomSpace()
        cubes.append(WeaponCube(random_pos[0]+CELL_SIZE/2, random_pos[1]+CELL_SIZE/2))
        self.screen.add(cubes)

        while True:
            player_pos = self.maze.mazeCoords(player.rect.x,
                                              player.rect.y)

            list(map(lambda g: g.find_player(self.maze, player_pos), Bosses))
            # list(map(lambda f: f.follow(player), followers))

            self.screen.focus(player)
            self.screen.update()


if __name__ == "__main__":
    g = Game(setup)
