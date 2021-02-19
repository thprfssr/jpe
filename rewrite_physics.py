from vector import *
from constants import *

import scipy.integrate as spi
import numpy as np

class System:
    def __init__(self, *particles):
        self.state = dict()

    def create_particle(self,
            position = O,
            velocity = O,
            mass = 1,
            charge = 1,
            radius = None,
            ):
        p = Particle(mass = mass, charge = charge, radius = radius)
        self.place_particle(p, position, velocity)
        return p

    @property
    def particles(self):
        return self.state.keys()

    @property
    def forces(self):
        forces = set()
        for p in self.particles:
            forces = forces.union(p.forces)
        return forces

    def add_particles(self, *particles):
        for p in particles:
            self.place_particle(p)

    def place_particle(self, particle, position = O, velocity = O):
        self.state[particle] = (position, velocity)

    def add_forces(self, *forces):
        for f in forces:
            for p in self.particles:
                if f.can_act_on(p):
                    p.forces.add(f)

    def position(self, particle):
        return particle.position(self.state)

    def velocity(self, particle):
        return particle.velocity(self.state)

    def acceleration(self, particle):
        return particle.acceleration(self.state)

    def __make_state_array(self, state = None):
        if state == None:
            state = self.state
        array = []
        for p in self.particles:
            position, velocity = state[p]
            rx, ry, rz = position
            vx, vy, vz = velocity
            array += [rx, ry, rz, vx, vy, vz]
        return array

    def __state_array_to_dict(self, state_array):
        N = len(state_array) // 6
        state_array = np.reshape(state_array, (N, 6))

        state = dict(zip(self.particles, state_array))
        for p in self.particles:
            rx, ry, rz, vx, vy, vz = state[p]
            position = Vector(rx, ry, rz)
            velocity = Vector(vx, vy, vz)
            state[p] = (position, velocity)
        return state

    def __state_derivative(self, state = None):
        if state == None:
            state = self.state
        derivative = {}
        for p in self.particles:
            position, velocity = state[p]
            acceleration = p.acceleration(state)
            derivative[p] = (velocity, acceleration)
        return derivative

    def __integrate(self, t):
        def diff(t, state_array, system):
            state = system.__state_array_to_dict(state_array)
            derivative = system.__state_derivative(state)
            return system.__make_state_array(derivative)
        t_span = (min(t), max(t))
        y0 = self.__make_state_array()
        sol = spi.solve_ivp(diff, t_span, y0, t_eval = t, args = (self,))
        matrix = np.transpose(sol.y)
        evolution = []
        for e in matrix:
            state = self.__state_array_to_dict(e)
            evolution.append(state)
        return evolution

    def update(self, dt):
        def diff(t, state_array, system):
            state = system.__state_array_to_dict(state_array)
            derivative = system.__state_derivative(state)
            return system.__make_state_array(derivative)
        t_span = (0, dt)
        y0 = self.__make_state_array()
        sol = spi.solve_ivp(diff, t_span, y0, args = (self,))
        matrix = np.transpose(sol.y)
        e = matrix[-1]
        self.state = self.__state_array_to_dict(e)

class Particle:
    def __init__(self,
            mass = 1,
            charge = 0,
            radius = None,
            ):
        self.mass = mass
        self.charge = charge
        self.forces = set()

    def position(self, state):
        return state[self][0]

    def velocity(self, state):
        return state[self][1]

    def acceleration(self, state):
        F = O
        for f in self.forces:
            F += f.evaluate(self, state)
        return F / self.mass

class FixedParticle(Particle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def velocity(self, state):
        return O

    def acceleration(self, state):
        return O

class Force:
    def __init__(self):
        pass # Defined in the child classes.

    def evaluate(self, particle, state):
        pass # Defined in the child classes.

    def can_act_on(self, particle):
        pass # Defined in the child classes.

class UniformGravity(Force):
    def __init__(self, g = 9.8, up = Z):
        self.g = g
        self.up = up

    def evaluate(self, particle, state):
        return - particle.mass * self.g * self.up

    def can_act_on(self, particle):
        return particle.mass != 0

class Spring(Force):
    def __init__(self, particle_a, particle_b, k = 1, rest_length = 1):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.k = k
        self.rest_length = rest_length

    def evaluate(self, particle, state):
        u = self.particle_b.position(state) - self.particle_a.position(state)
        n = u.normalize()
        compression = u.norm() - self.rest_length
        if particle == self.particle_a:
            return n * self.k * compression
        elif particle == self.particle_b:
            return -n * self.k * compression
        else:
            return O

    def can_act_on(self, particle):
        return particle in {self.particle_a, self.particle_b}

class Drag(Force):
    def __init__(self, beta = 1):
        self.beta = beta

    def evaluate(self, particle, state):
        return - self.beta * particle.velocity(state)

    def can_act_on(self, particle):
        return True

class CentralForce(Force):
    def __init__(self, center = O, mu = 1, softening = 1e-9):
        self.center = center
        self.mu = mu
        self.softening = softening

    def evaluate(self, particle, state):
        u = particle.position(state) - self.center
        r = u.norm()
        n = u.normalize()
        strength = self.mu * r / (r**2 + self.softening**2)**(3/2)
        return - n * strength 

    def can_act_on(self, particle):
        return True

class RestoringForce(Force):
    def __init__(self, center = O, k = 1):
        self.k = 1
        self.center = center

    def evaluate(self, particle, state):
        return - self.k * (particle.position(state) - self.center)

    def can_act_on(self, particle):
        return True

class InverseSquare(Force):
    def __init__(self, interacting_particles = set(), mu = 1, softening = 1e-9):
        self.mu = mu
        self.interacting_particles = interacting_particles
        self.softening = softening

    def evaluate(self, particle, state):
        F = O
        if particle in self.interacting_particles:
            for p in self.interacting_particles:
                center = p.position(state)
                f = CentralForce(center, self.mu, self.softening)
                F += f.evaluate(particle, state)
        return F

    def can_act_on(self, particle):
        return particle in self.interacting_particles
