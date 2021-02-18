from physics import *
from vector import *
from constants import *

dt = 0.0001

p = Particle()
U = Universe(p)
U.add_force(UniformGravity())
U.add_force(Drag())

while True:
    print(p.velocity.z)
    U.update(dt)
