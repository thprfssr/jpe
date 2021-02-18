import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
from matplotlib.animation import FuncAnimation

from vector import *
from physics import *
from constants import *

dt = 0.01
k = 300
m = 1

particles = []
M = 10
N = 10
r = 3
for x in np.linspace(-r, r, M):
    for y in np.linspace(-r, r, N):
        vx, vy, vz = npr.uniform(-0.4, 0.4, 3)
        p = Particle(position = Vector(x, y),
                velocity = Vector(vx, vy, vz),
                mass = m)
        particles.append(p)
U = Universe(*particles)

for i in range(M*N):
    j = i + N
    if j in range(M*N):
        a = particles[i]
        b = particles[j]
        U.add_force(Spring(a, b, k = k))

for i in range(M*N):
    j = i + N + 1
    if j in range(M*N) and j % N != 0:
        a = particles[i]
        b = particles[j]
        U.add_force(Spring(a, b, k = k))

for i in range(M*N):
    j = i + 1
    if j in range(M*N) and j % N != 0:
        a = particles[i]
        b = particles[j]
        U.add_force(Spring(a, b, k = k))

U.add_force(Drag(beta = 6))

ca = FixedParticle(position = Vector(-9, 9))
cb = FixedParticle(position = Vector(9, 9))
U.add_force(Spring(ca, particles[9], k = 3*k))
U.add_force(Spring(cb, particles[99], k = 3*k))
U.add_force(UniformGravity(direction = -Y))

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

def init():
    a = 10
    ax.set_xlim(-a, a)
    ax.set_ylim(-a, a)
    ax.set_aspect('equal')
    return ln,

def update(frame):
    U.update(dt)
    x = [p.position.x for p in particles]
    y = [p.position.y for p in particles]
    ln.set_data(x, y)
    print(frame)
    return ln,

ani = FuncAnimation(fig, update, frames = range(0, 1000),
        init_func = init, blit = True)

plt.show()
