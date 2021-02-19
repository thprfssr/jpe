from rewrite_physics import *
from vector import *
from constants import *

u = 10
S = System()
pa = S.create_particle(position = Y, velocity = u*X)
pb = S.create_particle(position = Z, velocity = u*Y)
pc = S.create_particle(position = -X, velocity = u*Z)
pd = S.create_particle(position = -Y, velocity = -u*X)

S.add_forces(RestoringForce(), InverseSquare(S.particles, -1), Drag())

while True:
    AB = (S.position(pa) - S.position(pb)).norm()
    AC = (S.position(pa) - S.position(pc)).norm()
    AD = (S.position(pa) - S.position(pd)).norm()
    BC = (S.position(pb) - S.position(pc)).norm()
    BD = (S.position(pb) - S.position(pd)).norm()
    CD = (S.position(pc) - S.position(pd)).norm()
    print('%f %f %f %f %f %f' % (AB, AC, AD, BC, BD, CD))
    S.update(0.01)
