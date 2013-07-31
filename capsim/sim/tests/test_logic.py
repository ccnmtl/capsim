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
        self.assertEquals(len(s.agents_mass), 10)
        self.assertEquals(len(s.agents_base_output), 10)

    def test_setup_patches(self):
        s = Simulation(grid_size=10)
        self.assertEquals(len(s.recreation_activity), 10)
        self.assertEquals(len(s.domestic_activity), 10)
        self.assertEquals(len(s.transport_activity), 10)
        self.assertEquals(len(s.education_activity), 10)

        self.assertEquals(len(s.food_exposure), 10)
        self.assertEquals(len(s.energy_density), 10)
        self.assertEquals(len(s.food_advertising), 10)
        self.assertEquals(len(s.food_convenience), 10)
        self.assertEquals(len(s.food_literacy), 10)

    def test_setup_network(self):
        s = Simulation(number_agents=10)
        self.assertEquals(s.neighbors.shape, (10, 10))

    def test_network_no_self_loops(self):
        """ an agent can't have itself as a neighbor.

        this means zeros in the adjacency matrix"""
        s = Simulation(number_agents=10)
        for i in range(10):
            self.assertEquals(s.neighbors[i][i], 0)

    def test_tick(self):
        s = Simulation()
        self.assertEqual(s.ticks, 0)
        s.tick()
        self.assertEqual(s.ticks, 1)
