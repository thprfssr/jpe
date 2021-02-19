from rewrite_physics import *
from vector import *
from constants import *

dt = 0.01

S = System()
p = S.create_particle()
S.add_forces(UniformGravity())
S.add_forces(Drag())

while True:
    print(S.velocity(p).z)
    S.update(dt)
