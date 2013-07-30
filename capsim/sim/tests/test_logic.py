from unittest import TestCase
from capsim.sim.logic import SimParamSet, Simulation


class SimParamSetTest(TestCase):
    def test_creation_defaults(self):
        s = SimParamSet()
        self.assertTrue(s is not None)


class SimTest(TestCase):
    def test_creation(self):
        s = Simulation()
        self.assertTrue(s is not None)

    def test_setup_agents(self):
        s = Simulation(number_agents=10)
        self.assertEquals(len(s.agents_bmi), 10)

    def test_setup_patches(self):
        s = Simulation(grid_size=10)
        self.assertEquals(len(s.patches_food_exposure), 10)
