#!/usr/bin/env python3
#coding: utf-8

from random import choice, randrange as rand
import pygame
from pygame.locals import *
import image as im

##
# Dimensions du labyrinthe
width = 9
height = 9

##
# Constantes servant à décrire les directions des passages
N, S, E, W  = 1, 2, 4, 8
IN          = 0x10
FRONTIER    = 0x20
OPPOSITE    = {E: W, W: E, S: N, N: S}

##
# Structures de données
grid = [([0] * width) for _ in range(height)]
frontier = set()

##
# Méthodes utilitaires
def add_frontier(x, y):
    if (x >= 0 and y >= 0 and y < len(grid)
            and x < len(grid[y]) and grid[y][x] == 0):
        grid[y][x] |= FRONTIER
        frontier.add((x, y))

def mark(x, y):
    grid[y][x] |= IN
    add_frontier(x-1, y)
    add_frontier(x+1, y)
    add_frontier(x, y-1)
    add_frontier(x, y+1)


def neighbors(x, y):
    if x > 0 and (grid[y][x-1] & IN):
        yield (x-1, y)
    if x + 1 < len(grid[y]) and (grid[y][x+1] & IN):
        yield (x+1, y)
    if y > 0 and (grid[y-1][x] & IN):
        yield (x, y-1)
    if y + 1 < len(grid) and (grid[y+1][x] & IN):
        yield (x, y+1)


def direction(fx, fy, tx, ty):
    return {(fx < tx): E,
            (fx > tx): W,
            (fy < ty): S,
            (fy > ty): N}[True]


def is_empty(cell):
    return cell == 0 or cell == FRONTIER


def draw():
    print()
    print(' ' + '_' * (len(grid[0]) * 2 - 1))
    for y, row in enumerate(grid):
        line = '|'
        for x, cell in enumerate(row):
            # Dessin du mur ou du passage Sud
            if is_empty(cell) and y+1 < len(grid) and is_empty(grid[y+1][x]):
                line += ' '
            else:
                line += ' ' if cell & S else '_'

            # Dessin du mur ou du passage Est
            if is_empty(cell) and x+1 < len(row) and is_empty(row[x+1]):
                if y+1 < len(grid) and (is_empty(grid[y+1][x]) or
                        is_empty(grid[y+1][x+1])):
                    line += ' '
                else:
                    line += '_'
            elif cell & E:
                line += ' ' if (cell | row[x+1]) & S else '_'
            else:
                line += '|'
        print(line)

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
            file.write("{} ".format(cell & 0b1111))
        file.write("\n")

##
# Exécution du script
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 3:
        width, height = map(int, argv[1:])
        grid = [[0] * width for _ in range(height)]

    mark(rand(width), rand(height))
    while frontier:
        ##
        # Choix d'un voisin à la frontière
        x, y = choice(list(frontier))
        frontier.remove((x, y))
        nx, ny = choice(list(neighbors(x, y)))

        ##
        # Création d'un passage
        dir = direction(x, y, nx, ny)
        grid[y][x] |= dir
        grid[ny][nx] |= OPPOSITE[dir]
        mark(x, y)

    draw()
    file = open("map_prim.txt", 'w')
    writemap(file, grid)
