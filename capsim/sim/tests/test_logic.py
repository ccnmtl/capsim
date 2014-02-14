import networkx as nx
import numpy as np
from unittest import TestCase
from capsim.sim.logic import SimParamSet, Simulation, Run
from capsim.sim.logic import (
    sigmoid, mass_delta
)


class SimParamSetTest(TestCase):
    def test_creation_defaults(self):
        s = SimParamSet()
        self.assertTrue(s is not None)

    def test_to_dict(self):
        s = SimParamSet(gamma_4=5.)
        result = s.to_dict()
        self.assertEqual(type(result), dict)
        self.assertTrue('grid_size' in result)
        self.assertEqual(result['gamma_4'], 5.)


class SimTest(TestCase):
    def test_creation(self):
        s = Simulation()
        self.assertTrue(s is not None)

    def test_setup_agents(self):
        s = Simulation(number_agents=10)
        self.assertEquals(len(s.agents_mass), 10)
        self.assertEquals(len(s.agents_base_output), 10)

    def test_setup_agents_odd_number(self):
        # this test is here because networkx.random_regular_graph
        # requires n * d to be even. so we make sure that we adjust
        # beforehand
        s = Simulation(number_agents=5)
        self.assertEquals(len(s.agents_mass), 5)

    def test_setup_patches(self):
        s = Simulation(grid_size=10)
        shape = (10, 10)
        self.assertEquals(s.recreation_activity.shape, shape)
        self.assertEquals(s.domestic_activity.shape, shape)
        self.assertEquals(s.transport_activity.shape, shape)
        self.assertEquals(s.education_activity.shape, shape)

        self.assertEquals(s.food_exposure.shape, shape)
        self.assertEquals(s.energy_density.shape, shape)
        self.assertEquals(s.food_advertising.shape, shape)
        self.assertEquals(s.food_convenience.shape, shape)
        self.assertEquals(s.food_literacy.shape, shape)

    def test_setup_network(self):
        s = Simulation(number_agents=10)
        self.assertEquals(nx.to_numpy_matrix(s.neighbors).shape, (10, 10))

    def test_network_no_self_loops(self):
        """ an agent can't have itself as a neighbor.

        this means zeros in the adjacency matrix"""
        s = Simulation(number_agents=10)
        neighbors = nx.to_numpy_matrix(s.neighbors).tolist()
        for i in range(10):
            self.assertEquals(neighbors[i][i], 0)

    def test_tick(self):
        s = Simulation()
        self.assertEqual(s.ticks, 0)
        s.tick()
        self.assertEqual(s.ticks, 1)

    def test_dict_roundtrip(self):
        s = Simulation()
        d = s.to_dict()
        self.assertTrue('MODEL_VERSION' in d)
        s2 = Simulation()
        s2.from_dict(d)
        self.assertEqual(s.ticks, s2.ticks)
        self.assertEqual(s.neighbors, s2.neighbors)


class RunTest(TestCase):
    def test_creation(self):
        r = Run()
        self.assertTrue(r is not None)
        r = Run(grid_size=10)
        self.assertTrue(r is not None)
        r = Run(num_agents=100)
        self.assertTrue(r is not None)
        r = Run(num_agents=100, ticks=100)
        self.assertTrue(r is not None)

    def test_run(self):
        r = Run(num_agents=100, ticks=10)
        out = r.run()
        self.assertTrue(r is not None)
        self.assertEqual(out.ticks, 10)
        self.assertEqual(out.params['num_agents'], 100)
        self.assertEqual(len(out.data), out.ticks)

        r = Run(num_agents=10, ticks=100)
        out = r.run()
        self.assertEqual(out.ticks, 100)
        self.assertEqual(out.params['num_agents'], 10)
        self.assertEqual(len(out.data), out.ticks)

    def test_serialization(self):
        r = Run(num_agents=100, ticks=10)
        d = r.to_dict()
        r2 = Run.from_dict(d)
        self.assertEqual(r.ticks, r2.ticks)
        self.assertEqual(r.params, r2.params)

    def test_runoutputserialization(self):
        r = Run(num_agents=100, ticks=10)
        out = r.run()
        d = out.to_dict()
        self.assertTrue('data' in d)
        self.assertEqual(d['ticks'], 10)


class TestHelpers(TestCase):
    def test_sigmoid(self):
        t = np.zeros(1)
        r = sigmoid(t)
        self.assertEqual(r, 0.5 + np.zeros(1))

        t = np.zeros(1) + 1.
        r = sigmoid(t)
        self.assertTrue((r - 0.73105858) < 0.001)

    def test_mass_delta(self):
        self.assertEqual(mass_delta(1.0, 1.0), 0.0)
        self.assertTrue((0.4998883466 - mass_delta(10.0, 0.9)) < 0.001)
