from physics import *
from vector import *
from constants import *

dt = 0.01

S = System()
p = S.create_particle(position = X, velocity = 1.2*Y)
S.add_forces(CentralForce())

while True:
    print(S.position(p).norm())
    S.update(dt)
