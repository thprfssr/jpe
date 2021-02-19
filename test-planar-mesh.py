import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
from matplotlib.animation import FuncAnimation

from vector import *
from physics import *
from constants import *

dt = 0.01
k = 150
m = 2

particles = []
M = 10
N = 10
r = 3
S = System()
for x in np.linspace(-r, r, M):
    for y in np.linspace(-r, r, N):
        p = S.create_particle(position = Vector(x, y),
                mass = m)
        particles.append(p)

for i in range(M*N):
    j = i + N
    if j in range(M*N):
        a = particles[i]
        b = particles[j]
        S.add_forces(Spring(a, b, k = k))

for i in range(M*N):
    j = i + N + 1
    if j in range(M*N) and j % N != 0:
        a = particles[i]
        b = particles[j]
        S.add_forces(Spring(a, b, k = k))

for i in range(M*N):
    j = i + 1
    if j in range(M*N) and j % N != 0:
        a = particles[i]
        b = particles[j]
        S.add_forces(Spring(a, b, k = k))

S.add_forces(Drag(beta = 1))

ca = S.place_particle(FixedParticle(), position = Vector(-9, 9))
cb = S.place_particle(FixedParticle(), position = Vector(9, 9))
S.add_forces(Spring(ca, particles[9], k = 3*k))
S.add_forces(Spring(cb, particles[99], k = 3*k))
S.add_forces(UniformGravity(up = Y))

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')


evolution = [S.state] * 1000
for i in range(1000):
    evolution[i] = S.state
    S.update(dt)
    print(i)


def init():
    a = 10
    ax.set_xlim(-a, a)
    ax.set_ylim(-a, a)
    ax.set_aspect('equal')
    return ln,

def update(frame):
    S.state = evolution[frame]
    x = [S.position(p).x for p in particles]
    y = [S.position(p).y for p in particles]
    ln.set_data(x, y)
    print(frame)
    return ln,

ani = FuncAnimation(fig, update, frames = range(0, 1000),
        init_func = init, blit = True)
ani.save("test.mp4", dpi = 300, fps = 60)
#plt.show()
