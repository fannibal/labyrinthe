import numpy as np
import pygame
from pygame.locals import *
import numpy as np
import time
from classes import Vertex,PrioQueue,isEmpty, Graph
import image as im
import sys

class RobotSimple:
    def __init__(self, x, y, th):
        self.states = ['idle', 'mission']
        self.dirs   = {'N' : [0,-1], 'S' : [0, 1], 'E':[1, 0], 'W':[-1, 0]}
        self.state = 'idle'
        self.x  = x
        self.y  = y
        self.th = th
        self.orders = []

    def move(self, dir):
        #print(type(dir), dir)
        #print(type(self.dirs), self.dirs)
        delta = self.dirs[dir]
        self.x += delta[0]
        self.y += delta[1]

    def turn(self, newdir):
        self.dir = newdir

    def check_end(self):
        pass

    def create_orders(self, path):
        for ind, el in enumerate(path[1:]):
            diff = el.label - path[ind].label
            if diff == 1:
                self.orders.append('E')
            elif diff == 9:
                self.orders.append('S')
            elif diff == -1:
                self.orders.append('W')
            elif diff == -9:
                self.orders.append('N')
            else:
                print("Error diff : ", diff)
                sys.exit(1)

    def display(self, screen, dir):
        size = 50
        screen.blit(im.rob[dir], (self.x*size,self.y*size))
