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
        return self.state[particle][0]

    def velocity(self, particle):
        return self.state[particle][1]

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

class Force:
    def __init__(self):
        pass # Defined in the child classes.

    def evaluate(self, particle, state):
        pass # Defined in the child classes.

    def can_act_on(self, particle):
        pass # Defined in the child classes.

class UniformGravity(Force):
    def __init__(self, g = 9.8, direction = -Z):
        self.g = g
        self.direction = direction

    def evaluate(self, particle, state):
        return particle.mass * self.g * self.direction

    def can_act_on(self, particle):
        return particle.mass != 0
