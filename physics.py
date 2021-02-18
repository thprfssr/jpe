from vector import *
from constants import *

class Universe:
    def __init__(self, particles = set(), forces = set()):
        self.particles = particles
        self.forces = forces

    def add_particles(self, *particles):
        for p in particles:
            self.particles.add(p)

class Particle:
    def __init__(self,
            position = O,
            velocity = O,
            acceleration = O,
            mass = 1,
            ):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass

class Force:
    def __init__(self):
        pass # Defined in daughter classes

    def force_on(self, particle):
        pass # Defined in daughter classes
