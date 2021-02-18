from vector import *
from constants import *
from physics import *

dt = 0.0001

pa = Particle(position = Vector(-1, 0, 1))
pb = Particle(position = Vector(1, 0, -1))
pc = Particle(position = Vector(0, 2, 0))
U = Universe(pa, pb, pc)
U.add_force(
        Spring(pa, pb),
        Spring(pb, pc),
        Spring(pc, pa),
        )
U.add_force(Drag())

while True:
    A = (pb.position - pc.position).norm()
    B = (pc.position - pa.position).norm()
    C = (pa.position - pb.position).norm()
    print('%f\t%f\t%f' % (A, B, C))

    U.update(dt)
