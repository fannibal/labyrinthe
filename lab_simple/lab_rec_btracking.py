#!/usr/bin/env python3

from random import sample
from time import sleep
import pygame
from pygame.locals import *
import image as im


width = 10
height = 10

N, S, E, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
MOVE = {N: lambda x, y: (x, y-1),
        S: lambda x, y: (x, y+1),
        E: lambda x, y: (x+1, y),
        W: lambda x, y: (x-1, y)}


def carve_maze():
    random_ways = lambda: sample((N, S, E, W), 4)
    maze = [[0] * width for _ in range(height)]
    walls = [(0, 0, d) for d in random_ways()]
    while walls:
        cx, cy, way = walls.pop()
        nx, ny = MOVE[way](cx, cy)
        if 0 <= ny < height and 0 <= nx < width and maze[ny][nx] == 0:
            maze[cy][cx] |= way
            maze[ny][nx] |= OPPOSITE[way]
            walls += [(nx, ny, d) for d in random_ways()]
            #draw(maze)
            #sleep(0.05)

    return maze


def draw(maze):
    print(' ' + '_' * (width * 2 - 1))
    for y, row in enumerate(maze):
        line = ['|']
        for x, cell in enumerate(row):
            line.append(' ' if cell & S else '_')
            if cell & E:
                line.append(' ' if (cell | maze[y][x+1]) & S else '_')
            else:
                line.append('|')
        print(''.join(line))
    print()

def file2map(file):
    map = []
    for i in range(9):
        line = file.readline().split(" ")
        line.pop(9)
        for i in range(9):
            line[i] = int(line[i])
        map.append(line)
    return map

def writemap(file, maze):
    for line in maze:
        for cell in line:
            file.write("{} ".format(cell))
        file.write("\n")


if __name__ == '__main__':
    from sys import argv

    if len(argv) >= 3:
        width, height = map(int, argv[1:3])

    if len(argv) == 4 and argv[3] == 'new':
        maze = carve_maze()
        draw(maze)
        map = open("map.txt", 'w')
        writemap(map, maze)
        map.close()

    else:
        maze = file2map(open("map.txt"   , 'r'))
        map_modified = file2map(open("newmap.txt", 'r'))
        draw(maze)
        draw(map_modified)
