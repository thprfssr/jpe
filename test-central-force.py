from physics import *
from vector import *
from constants import *

dt = 0.0001

p = Particle(position = X, velocity = 1.2*Y)
U = Universe(p)
U.add_force(CentralForce())

while True:
    print(p.position.norm())
    U.update(dt)
