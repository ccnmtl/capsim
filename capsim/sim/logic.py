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
        self.recreation_activity = np.arange(self.params.grid_size)
        self.domestic_activity = np.arange(self.params.grid_size)
        self.transport_activity = np.arange(self.params.grid_size)
        self.education_activity = np.arange(self.params.grid_size)

        self.food_exposure = np.arange(self.params.grid_size)
        self.energy_density = np.arange(self.params.grid_size)
        self.food_advertising = np.arange(self.params.grid_size)
        self.food_convenience = np.arange(self.params.grid_size)
        self.food_literacy = np.arange(self.params.grid_size)

    def setup_network(self):
        # make an adjacency matrix
        n = self.params.number_agents
        self.neighbors = np.zeros(n * n).reshape((n, n))
        # fill it in

    def tick(self):
        """ each tick of the clock """
        self.ticks += 1
