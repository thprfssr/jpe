from physics import *
from vector import *
from constants import *

p = SphericalParticle()
U = Universe(p)
U.add_force(UniformGravity(), Drag(), Buoyancy())

while True:
    print(p.velocity.z)
    U.update(dt)
