import numpy as np
from .paramset import SimParamSet


class Simulation(object):
    def __init__(self, **kwargs):
        self.params = SimParamSet(**kwargs)
        self.setup()

    def setup(self):
        self.setup_patches()
        self.setup_agents()
        self.setup_network()

    def setup_agents(self):
        self.agents_mass = np.arange(self.params.number_agents)
        self.agents_base_output = np.arange(self.params.number_agents)

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
        pass

    def tick(self):
        """ each tick of the clock """
        pass
