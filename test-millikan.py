from physics import *
from vector import *
from constants import *

dt = 1e-7

d = 7.66e-3
V = 500
E = V / d
e = fundamental_charge

viscosity = 1.82e-5

R = 4.65e-7
rho = 886
q = e * (3)

S = System()
p = Particle(
        radius = R,
        mass = 4/3 * pi * R**3 * rho,
        charge = q,
        )
S.add_particles(p)

S.add_forces(
        UniformGravity(),
        StokesDrag(viscosity = viscosity),
#        UniformElectricField(E = E),
        BuoyantForce(rho = 1.225),
        )

#G = UniformGravity()
#B = Buoyancy(medium_density = 1.225)
#D = StokesDrag(viscosity = 1.812e-5)
#E = UniformElectricField(strength = V/d)
#U.add_force(G, B, D, E)

while True:
    print(S.velocity(p))
    '''
    if v != 0:
        print(v, 0.5e-3 / v)
    '''
    S.update(dt)
