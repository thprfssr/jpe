from rewrite_physics import *
from vector import *
from constants import *

S = System()
p = S.create_particle(position = X, velocity = 1000*Y - 9*Z)
S.add_forces(RestoringForce())
S.add_forces(Drag())

while True:
    S.update(0.01)
    x, y, z = S.position(p)
    print('%f\t%f\t%f' % (x, y, z))
