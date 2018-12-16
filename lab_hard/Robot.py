#!/usr/bin/env python3
import numpy as np
import pygame
import time
import sys

import image as im

from pygame.locals import *

DIST = 0.4

class Robot:
    
    ####################################################
    # Constructor
    ####################################################
    
    def __init__(self, X_init, amers):
        # Etat et commande
        self.X  = np.array([[X_init[0,0]],   # x
                            [X_init[1,0]],   # y
                            [X_init[2,0]],   # theta
                            [   0.3    ]])  # v
        self.u  =  0.0  

        self.cpt_amer  = 1
        self.amers     = amers
        self.amer_view = False
        self.target    = 0
        self.traj      = []

    
    ####################################################
    # Evolution model and control
    ####################################################

    def f(self):
        xdot = np.array([[self.X[3][0]*np.cos(self.X[2][0])],
                         [self.X[3][0]*np.sin(self.X[2][0])],
                         [            self.u               ],
                         [              0                  ]])
        return xdot

    def measure(self, amer):
            
            dist  = np.sqrt((amer[0,0]-self.X[0,0])**2 + (amer[1,0]-self.X[1,0])**2)
            if self.amer_view and dist>DIST:
                #Remise à zero du test d'amer
                self.amer_view = False
                self.u = 0.0 
                
            if  dist < DIST:
                self.amer_view = True
                return dist
            return dist
            
    ####################################################
    # Function to compute angles
    ####################################################

    def next_yaw(self, amer):
        nyaw = np.arctan2((amer[1,0]-self.X[1,0]),(amer[0,0]-self.X[0,0]))
        return nyaw

    def modulo(self, a, b):
        return (a-b+np.pi)%(2*np.pi) - np.pi

    ####################################################
    # Running
    ####################################################

    def step(self, dt):

        amer = self.amers[self.cpt_amer]
        
        # Measure the distance between the boat and the target
        dmin = self.measure(amer)
        
        if dmin < DIST:
            self.cpt_amer +=1

        if self.cpt_amer >= len(self.amers):
            return True

        # Future angle
        new_angle = self.next_yaw(amer)
        self.target = new_angle

        # Correction proportionelle
        k = 1
        delta = self.modulo(new_angle,self.X[2,0])
        self.u = k*delta
        
        #Euler method
        self.X = self.X + dt*self.f()

        self.traj.append(self.X)
        
        

    ####################################################
    # Display
    ####################################################

    def display(self, screen):
        size = 50

        pix_x = self.X[0,0]*size 
        pix_y = self.X[1,0]*size 
        pix_y = -pix_y

        if self.X[2,0] < 0:
            angle = 360 + self.X[2,0]*360/6.28
        else:
            angle = self.X[2,0]*360/6.28
        
        ind_angle = int((angle+5)//10)
        ind_angle = ind_angle%len(im.rob)
        
        screen.blit(im.rob[ind_angle], (pix_x,pix_y))