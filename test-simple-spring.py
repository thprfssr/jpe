from physics import *
from vector import *
from constants import *

dt = 0.0001

p = Particle(position = Vector(1, 1, 1), velocity = 1000*X)
c = FixedParticle()
U = Universe(p, c)
U.add_force(Spring(p, c))
U.add_force(UniformGravity())
U.add_force(Drag())

while True:
    x, y, z = p.position
    print('%f\t%f\t%f' % (x, y, z))
    U.update(dt)
