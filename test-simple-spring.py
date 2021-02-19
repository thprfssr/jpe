from physics import *
from vector import *
from constants import *

dt = 0.01

S = System()
p = S.create_particle(position = Vector(1, 1, 1), velocity = 1000*Z + 5000*X)
c = FixedParticle()
S.place_particle(c)
S.add_forces(Spring(p, c))
S.add_forces(UniformGravity())
S.add_forces(Drag())

while True:
    x, y, z = S.position(p)
    print('%f\t%f\t%f' % (x, y, z))
    S.update(dt)
