from physics import *
from vector import *
from constants import *

dt = 1e-9

d = 7.66e-3
V = 500
e = fundamental_charge
p = Drop(
        radius = 4.75e-7,
        density = 800,
        charge = -2*e,
        )
U = Universe(p)
G = UniformGravity()
B = Buoyancy(medium_density = 1.225)
D = StokesDrag(viscosity = 1.812e-5)
E = UniformElectricField(strength = V/d)
U.add_force(G, B, D, E)

while True:
    v = p.velocity.z
    if v != 0:
        print(v, 0.5e-3 / v)
    U.update(dt)
