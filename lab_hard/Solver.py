#!/usr/bin/env python3
import sys
import pygame
import numpy  as np
import time

import image as im

from pygame.locals import *
from classes       import Vertex,PrioQueue,isEmpty, Graph



class Solver:
	####################################################
	# Constructor
	####################################################

	def __init__(self):
		# Settings
		self.nb_lab   = -1
		self.ind_end  = -1
		self.filename = ""
		# Lab
		self.maze     = []
		# Graph
		self.g        = []
		self.pi       = []
		# Output
		self.path     = []
		self.amers    = []

	####################################################
	# Conversting the file into a list with intergers
	####################################################

	def file2map(self, file):
	    """
	    Function : read a file to create a list representing the maze
	    """
	    for i in range(9):
	        line = file.readline().split(" ")
	        line.pop(9)
	        for i in range(9):
	            line[i] = int(line[i])
	        self.maze.append(line)
	    
	####################################################
	# Creation the file with all the edges for the graph
	####################################################

	def create_edges(self):
	    """
	    Function : write the maze in a file following the format used to describe graphs
	    the maze is "translated to a graph"
	    """
	    file = open("data/graph.txt", "w")
	    file.write("81 \n")
	    for indl, line in enumerate(self.maze):
	        for indc, case in enumerate(line):
	            self.create_edges_one_case(9*indl+indc, case, file)
	    file.close()

	def create_edges_one_case(self, indc, case, file):
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

	####################################################
	# Creating the path from the Priority Queue
	####################################################

	def backtrack_pred(self):
	    """
	    Function : create a path from the result of the Dijkstra's algorithm
	    pi[str(path[-1])] give the predecessor of the actual Vertex
	    """
	    last_vertex = self.g._vertices[self.ind_end]
	    self.path = [last_vertex]
	    while len(self.path) <= last_vertex.distance:
	        self.path.append(self.pi[str(self.path[-1])])
	    self.path.reverse()

	def create_amers(self):
		init = np.array([[0],[0]])
		self.amers.append(init)
		for ind, el in enumerate(self.path[1:]):
			diff = el.label - self.path[ind].label
			amer = self.amers[-1].copy()
			if diff == 1:
				amer[0,0] += 1
			elif diff == 9:
				amer[1,0] -= 1
			elif diff == -1:
				amer[0,0] -= 1
			elif diff == -9:
				amer[1,0] += 1
			else:
				print("Error diff : ", diff)
				sys.exit(1)
			self.amers.append(amer)

	####################################################
	# Running
	####################################################

	def run(self):

		# Select the map
	    #self.nb_lab = int(input("Nombre (0 à 2) : "))
	    self.nb_lab = 0
	    if self.nb_lab == 0:
	        self.filename = "kept_map/newmap0.txt"
	        self.ind_end  = 30
	    elif self.nb_lab == 1:
	        self.filename = "kept_map/newmap1.txt"
	        self.ind_end  = 65
	    elif self.nb_lab == 2:
	        self.filename = "kept_map/newmap2.txt"
	        self.ind_end  = 32
	    else:
	        sys.exit()
			    
	    #translation file to list[list]
	    self.file2map(open(self.filename, 'r'))
	    self.create_edges() #create the file to create the graph after
	    self.g = Graph()
	    self.g.read("data/graph.txt") #read the file created just before to complete the graph
	    try :
	        self.pi=self.g.dijkstra() #apply dijsktra
	    except:
	        print("No way found to solve the maze")
	        sys.exit(1)
	    self.backtrack_pred() #path from start to end
	    self.create_amers()

	####################################################
	# Display
	####################################################

	def display_maze_ihm(self, screen):
	    """
	    Function : display the maze on a pygame screen
	    path reprensent the result from dijkstra
	    cpt represent the position of the robot in his path
	    """
	    size = 50
	    screen.fill((200, 200, 200))
	    for i in range(9):
	        for j in range(9):
	            screen.blit(im.cases[self.maze[i][j]], (j*size, i*size))
	    d = len(self.path)
	    for v in self.path:
	        screen.blit(im.path, (50*(v.label%9) + 5, 50*(v.label//9) + 5))
	    screen.blit(im.start, (5,5))
	    screen.blit(im.finish, ((self.ind_end%9)*50 + 5, (self.ind_end//9)*50 + 5))

