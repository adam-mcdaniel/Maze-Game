import random
import os
import numpy
from astar import getPath
from random import shuffle, randrange


class Maze:
    def __init__(self, maze, cell_size):
        self.maze = maze
        self.cell_size = cell_size
        self.spaces = self.getSpaces()
        self.true_maze = self.makeTrueMaze(self.maze)
        self.player_coords = self.mazeCoords(self.cell_size, self.cell_size)

    def printMaze(self):
        os.system("clear")
        list(map(lambda a: print(str(a)), self.true_maze))

    def addPlayerToMap(self, player):
        self.true_maze[self.player_coords[1]][self.player_coords[0]] = 0
        self.player_coords = self.mazeCoords(player.rect.x, player.rect.y)
        self.true_maze[self.player_coords[1]][self.player_coords[0]] = 2

    def makeTrueMaze(self, maze):
        true_maze = [[]]
        y = 0
        for line in self.maze:
            for column in line:
                true_maze[y].append(self.isWall(column))
            y += 1
            true_maze.append([])

        return true_maze[:len(true_maze)-1]

    def mazeCoords(self, x, y):
        return int(x / self.cell_size), int(y / self.cell_size)

    def pixelCoords(self, x, y):
        return x * self.cell_size, y * self.cell_size

    def getSpaces(self):
        y = 0
        x = 0
        spaces = []
        for line in self.maze:
            for column in line:
                if column == " ":
                    spaces.append((x, y))
                x += self.cell_size
            y += self.cell_size
            x = 0
        return spaces

    def isWall(self, item):
        if item in ["+", "|", "-"]:
            return 1
        else:
            return 0

    def getRandomSpace(self):
        return random.choice(self.spaces)

    def getPath(self, x0, y0, x, y):
        return getPath(numpy.array(self.true_maze), x0, y0, x, y)


def MakeMaze(dimensions):
    w, h = dimensions
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue

            if xx == x:
                hor[max(y, yy)][x] = "+ "

            if yy == y:
                ver[y][max(x, xx)] = "  "

            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s


if __name__ == '__main__':
    print(MakeMaze())
