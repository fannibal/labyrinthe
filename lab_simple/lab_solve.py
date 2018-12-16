#!/usr/bin/env python3
import pygame
from pygame.locals import *
import numpy as np
import time
from classes import Vertex,PrioQueue,isEmpty, Graph
import image as im
from robot import RobotSimple


def create_edges_one_case(indc, case, file):
    """
    Function : decode a case to write the different path between each vertices

    Note: a case is written on 4 bits
        order : N-S-E-W
        0000 if full of walls, 1111 if empty
    """
    val = case
    W, val = val//8, val%8
    E, val = val//4, val%4
    S, val = val//2, val%2
    N      = val//1
    if N : file.write("{} {} {} \n".format(indc, indc-9, 1))
    if S : file.write("{} {} {} \n".format(indc, indc+9, 1))
    if E : file.write("{} {} {} \n".format(indc, indc+1, 1))
    if W : file.write("{} {} {} \n".format(indc, indc-1, 1))

def create_edges(maze):
    """
    Function : write the maze in a file following the format used to describe graphs
    the maze is "translated to a graph"
    """
    file = open("graph.txt", "w")
    file.write("81 \n")
    for indl, line in enumerate(maze):
        for indc, case in enumerate(line):
            create_edges_one_case(9*indl+indc, case, file)
    file.close()

def file2map(file):
    """
    Function : read a file to create a list representing the maze
    """
    map = []
    for i in range(9):
        line = file.readline().split(" ")
        line.pop(9)
        for i in range(9):
            line[i] = int(line[i])
        map.append(line)
    return map

def display_maze_ihm(screen, maze, path, cpt):
    """
    Function : display the maze on a pygame screen
    path reprensent the result from dijkstra
    cpt represent the position of the robot in his path
    """
    size = 50
    screen.fill((200, 200, 200))
    for i in range(9):
        for j in range(9):
            screen.blit(im.cases[maze[i][j]], (j*size, i*size))
    d = len(path)
    for v in path[:cpt]:
        screen.blit(im.path, (50*(v.label%9) + 5, 50*(v.label//9) + 5))
    screen.blit(im.start, (5,5))
    screen.blit(im.finish, ((FIN%9)*50 + 5, (FIN//9)*50 + 5))


def backtrack_pred(pi, v):
    """
    Function : create a path from the result of the Dijkstra's algorithm
    pi[str(path[-1])] give the predecessor of the actual Vertex
    """
    path = [v]
    while len(path) <= v.distance:
        path.append(pi[str(path[-1])])
    path.reverse()
    return path

if __name__ == '__main__':
    # Select the map
    nombre = int(input("Nombre (0 à 2) : "))
    if nombre == 0:
        filename = "kept_map/newmap0.txt"
        FIN = 30
    elif nombre == 1:
        filename = "kept_map/newmap1.txt"
        FIN = 65
    elif nombre == 2:
        filename = "kept_map/newmap2.txt"
        FIN = 32
    else:
        sys.exit()

    ###
    t0 = time.time()
    #translation file to list[list]
    maze = file2map(open(filename, 'r'))
    create_edges(maze) #create the file to create the graph after
    g = Graph()
    g.read("graph.txt") #read the file created just before to complete the graph
    try :
        pi=g.dijkstra() #apply dijsktra
    except:
        print("No way found to solve the maze")
        sys.exit(1)
    Path = backtrack_pred(pi, g._vertices[FIN]) #path from start to end
    print("temps ==> ", time.time()-t0)
    ###

    #Object representing the Robot
    #Firstly just the display
    #Then a real continue model
    Rob = RobotSimple(0,0,'S')
    Rob.create_orders(Path)

    #Pygame init
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    pygame.display.flip()
    running = 1
    cpt = 0
    #Rob.u[0,0] = 0
    while running:
        #background with the maze and the path
        display_maze_ihm(screen, maze, Path, cpt+1)
        #Actions of the robot
        if (Rob.x + 9*Rob.y != FIN):
            Rob.turn(cpt)
            Rob.move(Rob.orders[cpt])
            #Rob.applyCommand(0.1, 10)
            Rob.display(screen, Rob.orders[cpt])
        else:
            Rob.display(screen, Rob.orders[-1])
        cpt+=1
        time.sleep(0.1)
        #restart of the animation
        if cpt >= 300:
            cpt=0
        #Key action
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            else:
                pass
        pygame.display.flip()

    pygame.quit()
