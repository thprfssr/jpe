from physics import *
from vector import *
from constants import *

p = Particle(position = X, velocity = 1000*Y - 9*Z)
U = Universe(p)
U.add_force(PotentialWell())
U.add_force(Drag())

while True:
    U.update(0.0001)
    x, y, z = p.position
    print('%f\t%f\t%f' % (x, y, z))
