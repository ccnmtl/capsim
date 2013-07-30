import numpy as np


class Simulation(object):
    def __init__(self, number_agents=1, number_patches=1):
        self.number_agents = number_agents
        self.number_patches = number_patches
        self.setup()

    def setup(self):
        self.setup_patches()
        self.setup_agents()
        self.setup_network()

    def setup_agents(self):
        self.agents_bmi = np.arange(self.number_agents)

    def setup_patches(self):
        self.patches_food_exposure = np.arange(self.number_patches)

    def setup_network(self):
        pass

    def tick(self):
        pass
