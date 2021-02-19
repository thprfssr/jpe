from physics import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

FRAMES = 2000
dt = 0.1

# Create the system
S = System()
S.create_particle(position = 2*X, velocity = 0.7*Y)
S.place_particle(FixedParticle())
S.add_forces(CentralForce())
S.add_forces(UniformGravity(g = 0.003, up = Y))

# Find the time evolution of the system
evolution = []
for i in range(FRAMES):
    evolution.append(S.state)
    S.update(dt)

# Create the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

a = 4
ax.set_xlim(-a, a)
ax.set_ylim(-a, a)
ax.set_aspect('equal')


def init():
    a = 5
    ax.set_xlim(-a, a)
    ax.set_ylim(-a, a)
    ax.set_aspect('equal')
    return ln,

def update(i):
    S.state = evolution[i]
    x = [S.position(p).x for p in S.particles]
    y = [S.position(p).y for p in S.particles]
    ln.set_data(x, y)
    print(i)
    return ln,

plt.title('Central Force with Small Uniform Perturbation')
ani = FuncAnimation(fig, update, frames = range(FRAMES), blit = True)
ani.save("test.mp4", dpi = 300, fps = 60)
#plt.show()
