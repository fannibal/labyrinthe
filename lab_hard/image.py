import pygame
import os

pygame.init()

######################
#       Robot        #
######################

rob = []
for i in range(36):
    rob.append(pygame.image.load("image/Robot/robot{}.png".format(10*i)))
	#rob.append(pygame.image.load("image/Robot/Robot{}.png".format(45*i)))

######################
#       Cases        #
######################

_0  = pygame.image.load("image/0.png")
_1  = pygame.image.load("image/1.png")
_2  = pygame.image.load("image/2.png")
_3  = pygame.image.load("image/3.png")
_4  = pygame.image.load("image/4.png")
_5  = pygame.image.load("image/5.png")
_6  = pygame.image.load("image/6.png")
_7  = pygame.image.load("image/7.png")
_8  = pygame.image.load("image/8.png")
_9  = pygame.image.load("image/9.png")
_10 = pygame.image.load("image/10.png")
_11 = pygame.image.load("image/11.png")
_12 = pygame.image.load("image/12.png")
_13 = pygame.image.load("image/13.png")
_14 = pygame.image.load("image/14.png")
_15 = pygame.image.load("image/15.png")
cases = [_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15]

start  = pygame.image.load("image/start.png")
finish = pygame.image.load("image/finish.png")
path   = pygame.image.load("image/path.png")
