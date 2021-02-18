from copy import deepcopy

from vector import *
from constants import *

class Universe:
    def __init__(self, *particles):
        self.particles = particles

    def add_particle(self, *particles):
        for p in particles:
            self.particles.add(p)

    def add_force(self, *forces):
        for f in forces:
            for p in self.particles:
                p.add_force(f)

    def update(self, dt):
        for p in self.particles:
            p.update(dt)

class Particle:
    def __init__(self,
            position = O,
            velocity = O,
            mass = 1,
            ):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.forces = set()

    def add_force(self, *forces):
        for f in forces:
            self.forces.add(f)

    def net_force(self):
        F = O
        for force in self.forces:
            F += force.force_on(self)
        return F

    def update(self, dt):
        a = self.net_force() / self.mass
        self.velocity += a * dt
        self.position += self.velocity * dt

class FixedParticle(Particle):
    def __init__(self, position = O):
        super().__init__(
                mass = inf,
                position = position,
                velocity = O,
                )

    def net_force(self):
        return O

    def add_force(self, *forces):
        pass

    def update(self, dt):
        pass

class Force:
    def __init__(self):
        pass # Defined in daughter classes

    def force_on(self, particle):
        pass # Defined in daughter classes

class Spring(Force):
    def __init__(self, particle_a, particle_b, k = 1, rest_length = 1):
        self.particle_a = particle_a
        self.particle_b = particle_b

        self.k = k
        self.rest_length = rest_length

    def force_on(self, particle):
        u = self.particle_b.position - self.particle_a.position
        n = u.normalize()
        compression = u.norm() - self.rest_length
        if particle == self.particle_a:
            return n * self.k * compression
        elif particle == self.particle_b:
            return -n * self.k * compression
        else:
            return O

class Drag(Force):
    def __init__(self, beta = 1):
        self.beta = beta

    def force_on(self, particle):
        return - self.beta * particle.velocity

class UniformGravity(Force):
    def __init__(self, g = 9.8):
        self.g = g

    def force_on(self, particle):
        return - particle.mass * self.g * Z
