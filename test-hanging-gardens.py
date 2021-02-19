from physics import *
from vector import *
from constants import *

import numpy as np
import matplotlib.pyplot as plt

FRAMES = 20
dt = 0.1

M = 10
N = 10

S = System()

# Make the top ring
top_ring_particles = []
for i in range(N):
    theta = 2 * np.pi * i/N
    R = 10
    r = R * np.cos(theta) * X + R * np.sin(theta) * Y
    p = FixedParticle()
    top_ring_particles.append(S.place_particle(p, position = r))

# Make the mesh particles
mesh_particles = []
for i in range(M*N):
    mesh_particles.append(S.create_particle())
P = np.resize(mesh_particles, (M, N))

# Connect the mesh to the top ring
for i in range(N):
    f = Spring(top_ring_particles[i], mesh_particles[i])
    S.add_forces(f)

# Make the horizontal mesh connections
for i in range(M):
    for j in range(N):
        f = Spring(P[i][j-1], P[i][j])
        S.add_forces(f)

# Make vertical mesh connections
for i in range(M-1):
    for j in range(N):
        f = Spring(P[i][j], P[i+1][j])
        S.add_forces(f)

# Make diagonal mesh connections
for i in range(M-1):
    for j in range(N):
        f = Spring(P[i][j-1], P[i+1][j])
        S.add_forces(f)

# Add gravity and drag
S.add_forces(UniformGravity(g=0.1), Drag())

# Compute the time-evolution of the system
#S.update(100)
evolution = []
for i in range(FRAMES):
    print('n = %d\tK = %f' % (i, S.total_kinetic_energy))
    evolution.append(S.state)
    S.update(100)

# Make the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

# Plot each point
state = evolution[i]
xs = [S.position(p).x for p in S.particles]
ys = [S.position(p).y for p in S.particles]
zs = [S.position(p).z for p in S.particles]
ax.scatter(xs, ys, zs)
plt.show()



'''
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
'''
