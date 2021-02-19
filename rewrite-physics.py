from vectors import *
from constants import *

class System:
    def __init__(self, *particles):
        self.particles = particles
        self.forces = set()

class State:
    def __init__(self):
        pass

class Particle:
    def __init__(self,
            position = O,
            velocity = O,
            mass = 1,
            charge = 0,
            ):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.charge = charge
        self.forces = set()
        self.parent_system = None

class Force:
    def __init__(self):
        pass # Defined in the child classes.

    def evaluate(self, particle, state):
        pass # Defined in the child classes.

    def acts_on(self, particle, state):
        pass # Defined in the child classes.
