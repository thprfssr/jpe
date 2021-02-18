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
            if f.acts_on(self):
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

class SphericalParticle(Particle):
    def __init__(self, radius = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def volume(self):
        return 4/3 * pi * self.radius**3

    def density(self):
        return self.volume() / self.mass

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

    def acts_on(self, particle):
        pass # Defined in daughter classes

class Spring(Force):
    def __init__(self, particle_a, particle_b, k = 1, rest_length = 1):
        self.particle_a = particle_a
        self.particle_b = particle_b

        self.k = k
        self.rest_length = rest_length

    def particles(self):
        return {self.particle_a, self.particle_b}

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

    def acts_on(self, particle):
        return particle in {self.particle_a, self.particle_b}

class Drag(Force):
    def __init__(self, beta = 1):
        self.beta = beta

    def force_on(self, particle):
        return - self.beta * particle.velocity

    def acts_on(self, particle):
        return True

class UniformGravity(Force):
    def __init__(self, g = 9.8, direction = -Z):
        self.g = g
        self.direction = direction

    def force_on(self, particle):
        return particle.mass * self.g * self.direction

    def acts_on(self, particle):
        return True

class CentralForce(Force):
    def __init__(self, center = O, mu = 1):
        self.center = center
        self.mu = mu

    def force_on(self, particle):
        u = particle.position - self.center
        r = u.norm()
        n = u.normalize()
        if r != 0:
            return - self.mu / r**2 * n
        else:
            return O

    def acts_on(self, particle):
        return True

class PotentialWell(Force):
    def __init__(self, center = O, k = 1):
        self.k = 1
        self.center = center

    def force_on(self, particle):
        return - self.k * (particle.position - self.center)

    def acts_on(self, particle):
        return True

class InverseSquare(Force):
    def __init__(self, affected_particles = set(), mu = 1):
        self.mu = mu
        self.affected_particles = affected_particles

    def force_on(self, particle):
        F = O
        if particle in self.affected_particles:
            for p in self.affected_particles:
                u = particle.position - p.position
                r = u.norm()
                n = u.normalize()
                if r != 0:
                    F += - self.mu / r**2 * n
        return F

    def acts_on(self, particle):
        return particle in self.affected_particles

class Buoyancy(Force):
    def __init__(self, medium_density = 1, g = 9.8, direction = -Z):
        self.medium_density = medium_density
        self.g = g
        self.direction = direction

    def force_on(self, particle):
        if self.acts_on(particle):
            F = - self.medium_density * particle.volume() * self.g
            return F * self.direction
        else:
            return O

    def acts_on(self, particle):
        return type(particle) == SphericalParticle

class StokesDrag(Force):
    def __init__(self, viscosity = 1):
        self.viscosity = viscosity

    def force_on(self, particle):
        v = particle.velocity
        r = particle.radius
        return - 6 * pi * self.viscosity * r * v

    def acts_on(self, particle):
        return type(particle) == SphericalParticle
