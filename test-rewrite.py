from rewrite_physics import *
from vector import *
from constants import *

import numpy as np

S = System()
p = S.create_particle()
for i in range(0):
    S.create_particle()
S.add_forces(UniformGravity())
evolution = S.update(10)
print(S.position(p))
