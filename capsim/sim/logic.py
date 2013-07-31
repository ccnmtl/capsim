import numpy as np
from .paramset import SimParamSet


class Simulation(object):
    def __init__(self, **kwargs):
        self.params = SimParamSet(**kwargs)
        self.setup()

    def setup(self):
        self.ticks = 0
        self.setup_patches()
        self.setup_agents()
        self.setup_network()

    def setup_agents(self):
        n = self.params.number_agents
        # for numpy
        shape = (n,)

        # randomly initialized
        self.agents_mass = self.params.agent_initial_mass.generate(shape)
        self.agents_base_output = self.params.agent_base_output.generate(shape)

        # randomly position them on the grid
        self.agents_row = np.arange(n)
        self.agents_col = np.arange(n)

        # state variables that will be calculated each turn:
        self.input = np.zeros(n)
        self.total_output = np.zeros(n)
        self.force_of_habit = np.zeros(n)
        self.c_control = np.zeros(n)
        self.physical_activity = np.zeros(n)
        self.friend_input = np.zeros(n)
        self.friend_output = np.zeros(n)

    def setup_patches(self):
        n = self.params.grid_size
        shape = (n, n)
        p = self.params
        self.recreation_activity = p.recreation_activity.generate(shape)
        self.domestic_activity = p.domestic_activity.generate(shape)
        self.transport_activity = p.transport_activity.generate(shape)
        self.education_activity = p.education_activity.generate(shape)

        self.food_exposure = p.food_exposure.generate(shape)
        self.energy_density = p.energy_density.generate(shape)
        self.food_advertising = p.food_advertising.generate(shape)
        self.food_convenience = p.food_convenience.generate(shape)
        self.food_literacy = p.food_literacy.generate(shape)

    def setup_network(self):
        # make an adjacency matrix
        n = self.params.number_agents
        self.neighbors = np.zeros(n * n).reshape((n, n))
        # fill it in

    def tick(self):
        """ each tick of the clock """
        self.ticks += 1
