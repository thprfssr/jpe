from physics import *
from vector import *
from constants import *

p = SphericalParticle(radius = 0.6)
U = Universe(p)
U.add_force(UniformGravity(), StokesDrag(), Buoyancy())

while True:
    print(p.velocity.z)
    U.update(dt)
