from physics import *

from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

FRAMES = 200
dt = 0.05

# Create the system
S = System()
N = 60
particles = [Particle() for i in range(N)]
fa = S.place_particle(FixedParticle(), position = -5*X + 5*Y)
fb = S.place_particle(FixedParticle(), position = 5*X + 5*Y)
for i in range(N):
    p = particles[i]
    r = (-5 + 10*i/N)*X + 5*Y
    S.place_particle(p, position = r)
S.add_forces(Spring(fa, particles[0], k = 1000, rest_length = 0.1))
S.add_forces(Spring(fb, particles[-1], k = 1000, rest_length = 0.1))
for i in range(N-1):
    f = Spring(particles[i], particles[i+1], k = 1000, rest_length = 0.1)
    S.add_forces(f)
S.add_forces(UniformGravity(up = Y))
S.add_forces(Drag())


# Compute the time-evolution
evolution = []
for i in tqdm(range(FRAMES)):
    evolution.append(S.state)
    S.update(dt)


# Create the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

a = 5
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

ani = FuncAnimation(fig, update, frames = range(FRAMES), blit = True)
ani.save("test.mp4", dpi = 300, fps = 60)
#plt.show()
