#!/usr/bin/env python3
import pygame
import sys
import numpy as np
import time
import image as im

from pygame.locals import *
from Robot import Robot
from Solver import Solver

#### Main ####

#Pygame init
pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.flip()

#Creating and solving the maze
solver = Solver()
solver.run()

X_init = np.array([[0],[0],[-np.pi/2],[0]])
robot  = Robot(X_init, solver.amers)

Tf = 1000
dt = 0.1

ended = 0
for t in np.arange(0,Tf,dt):
    
    solver.display_maze_ihm(screen)
    ended = robot.step(dt)
    robot.display(screen)
    
    if ended == True:
    	time.sleep(5)
    	pygame.quit()
    	print("Good job bro ! ")
    	sys.exit()
    #sys.exit()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        else:
            pass
    pygame.display.flip()

pygame.quit()
###
"""
Rob = RealRobot(X_init)
Rob.create_orders(Path)
Rob.create_amers()


running = 1

cpt = 0
Rob.image  = im.rob
Rob.screen = screen

dt = 0.1
t  = 1

#background with the maze and the path
display_maze_ihm(screen, maze, Path, 100)
#Actions of the robot
Rob.display(Rob.screen, Rob.image)

Rob.run(dt = 0.1)


pygame.quit()
"""