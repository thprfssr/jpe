from physics import *
from vector import *
from constants import *

u = 10
pa = Particle(position = Y, velocity = u*X)
pb = Particle(position = Z, velocity = u*Y)
pc = Particle(position = -X, velocity = u*Z)
pd = Particle(position = -Y, velocity = -u*X)

U = Universe(pa, pb, pc, pd)
U.add_force(PotentialWell(), InverseSquare(U.particles, -1), Drag())

while True:
    AB = (pa.position - pb.position).norm()
    AC = (pa.position - pc.position).norm()
    AD = (pa.position - pd.position).norm()
    BC = (pb.position - pc.position).norm()
    BD = (pb.position - pd.position).norm()
    CD = (pc.position - pd.position).norm()
    print('%f %f %f %f %f %f' % (AB, AC, AD, BC, BD, CD))
    U.update(dt)
