import numpy as np
import matplotlib.pyplot as plt
from roblib import *


def f(x,u):
    xdot = np.array([[x[3][0]*np.cos(x[2][0])],
                    [x[3][0]*np.sin(x[2][0])],
                    [u[0][0]                ],
                    [u[1][0]              ] ])
    return xdot



plt.close()
plt.figure()
dt = 1
L = 10
ecart = []

u = np.array([[0],
              [1]])

x = np.array([[  10     ],
              [  0      ],
              [  1      ],
              [  1      ]])

for t in np.arange(0,10,dt):
    plt.cla()
    plt.axis([-30,30,-30,30])

    draw_tank(x)

    x=x+dt*f(x,u);

    plt.draw()
    plt.pause(0.01)

plt.figure()
#plt.plot(ecart)
