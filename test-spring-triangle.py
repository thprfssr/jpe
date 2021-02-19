from vector import *
from constants import *
from physics import *

dt = 0.01

S = System()
pa = S.create_particle(position = Vector(-1, 0, 1))
pb = S.create_particle(position = Vector(1, 0, -1))
pc = S.create_particle(position = Vector(0, 2, 0))
S.add_forces(
        Spring(pa, pb),
        Spring(pb, pc),
        Spring(pc, pa),
        )
S.add_forces(Drag())

while True:
    A = (S.position(pb) - S.position(pc)).norm()
    B = (S.position(pc) - S.position(pa)).norm()
    C = (S.position(pa) - S.position(pb)).norm()
    print('%f\t%f\t%f' % (A, B, C))

    S.update(dt)
