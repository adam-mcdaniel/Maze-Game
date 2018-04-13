# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
from heapq import *


def rev(tup):
    ltup = list(tup)
    return tuple(ltup[::-1])


def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False

'''Here is an example of using my algo with a numpy array,
   astar(array, start, destination)
   astar function returns a list of points (shortest path)'''


# [(12, 9), (11, 8), (10, 8), (9, 8), (8, 8), (7, 8), (6, 8), (5, 8), (4, 8),
# (3, 8), (2, 8), (1, 7), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
# (8, 6), (9, 6), (10, 6), (11, 6), (12, 5), (11, 4), (10, 4), (9, 4), (8, 4),
# (7, 4), (6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 3), (2, 2), (3, 2),
# (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 1),
# (11, 0), (10, 0), (9, 0), (8, 0), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0),
# (2, 0), (1, 0)]

# print("x={}, y={}".format(len(nmap[0]), len(nmap)))


def getPath(m, x0, y0, x, y):
    # print(
    #     list(map(lambda a: rev(a), astar(m,
    #                                      rev((x, y)),
    #                                      rev((x0, y0)))))
    #     )
    # return []
    # return astar(m,
    #              rev((x, y)),
    #              rev((x0, y0)))
    return list(map(lambda a: rev(a), astar(m,
                                            rev((x, y)),
                                            rev((x0, y0)))[1:])) + [(x, y)]


# print(getPath(nmap, 13, 10, 0, 0))
