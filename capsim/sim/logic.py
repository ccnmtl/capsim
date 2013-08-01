import numpy as np
import networkx as nx
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
        self.agents_row = np.random.randint(self.params.grid_size, size=n)
        self.agents_col = np.random.randint(self.params.grid_size, size=n)

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
        # make a random graph of links, all nodes have
        # 3 neighbors. will want to add more controls
        # here later.
        self.neighbors = nx.random_regular_graph(3, n)

    def tick(self):
        """ each tick of the clock
        * calculate-total-output
        * calculate-input
        * set mass calculate-mass
        * move if starving
        """
        self.ticks += 1

        # temporary agent environment variables
        recreation = self.recreation_activity[self.agents_row, self.agents_col]
        domestic = self.domestic_activity[self.agents_row, self.agents_col]
        transport = self.transport_activity[self.agents_row, self.agents_col]
        education = self.education_activity[self.agents_row, self.agents_col]

        food_exposure = self.food_exposure[self.agents_row, self.agents_col]
        energy_density = self.energy_density[self.agents_row, self.agents_col]
        food_advertising = self.food_advertising[self.agents_row,
                                                 self.agents_col]
        food_convenience = self.food_convenience[self.agents_row,
                                                 self.agents_col]
        food_literacy = self.food_literacy[self.agents_row, self.agents_col]

        # values that need to be updated:
        # * friend_output
        # * friend_input

        self.physical_activity = calculate_physical_activity(
            recreation, domestic, transport, education)

        self.total_output = calculate_total_output(
            self.agents_base_output,
            self.physical_activity, self.params.gamma_5,
            self.friend_output, self.params.gamma_6,
            self.params.sigma_2)

        self.force_of_habit = calculate_force_of_habit(
            food_exposure, energy_density,
            food_advertising, food_convenience)

        self.c_control = calculate_c_control(food_literacy)

        self.input = calculate_input(
            self.total_output,
            self.force_of_habit, self.params.gamma_2,
            self.friend_input, self.params.gamma_3,
            self.c_control, self.params.gamma_4,
            self.params.sigma_1)

        self.agents_mass = calculate_mass(
            self.agents_mass, self.input,
            self.total_output, self.params.gamma_1)


def calculate_friend_input():
    """
    to-report friend-input ;; turtle-procedure
      report sigmoid (10 * (network-input-percent - 0.5)) - 0.5
    end
    """
    return sigmoid(10. * (network_input_percent() - 0.5)) - 0.5


def network_input_percent():
    """
    percentage of neighbors who have a higher input than the agent

    to-report network-input-percent ;; turtle procedure
      let my-input input
      ifelse empty? [input] of link-neighbors
      [report 0.0]
      [report (count link-neighbors with [input >= my-input])
               / (count link-neighbors)]
    end
    """
    
    

def calculate_friend_output():
    """
    to-report friend-output
      report sigmoid (10 * (network-output-percent - 0.50)) - 0.50
    end

    to-report network-output-percent ;; turtle procedure
      let my-output total-output
      ifelse empty? [total-output] of link-neighbors
      [report 0.0]
      [report (count link-neighbors with [total-output >= my-output])
               / (count link-neighbors)]
    end
    """


def calculate_c_control(food_literacy):
    """
    to-report c-control ;; turtle procedure
     report sigmoid (10 * (food-literacy - 0.5))
    end
    """
    return sigmoid(10. * (food_literacy - 0.5))


def calculate_force_of_habit(food_exposure, energy_density,
                             food_advertising, food_convenience):
    """
    to-report force-of-habit ;; turtle-procedure
      report sigmoid (10 * food-sum)
    end
    """
    return sigmoid(10. * food_sum(food_exposure, energy_density,
                                  food_advertising, food_convenience))


def food_sum(food_exposure, energy_density,
             food_advertising, food_convenience):
    """
    to-report food-sum
      report sum map minus-half (list food-exposure food-energy-density
                                      food-advertising food-convenience)
    end
    """
    return ((food_exposure - 0.5)
            + (energy_density - 0.5)
            + (food_advertising - 0.5)
            + (food_convenience - 0.5))


def calculate_physical_activity(recreation_activity, domestic_activity,
                                transport_activity, education_activity):
    """
    to-report physical-activity ;; turtle-procedure
      report sigmoid (10 * activity-sum)
    end
    """
    return sigmoid(
        10. * activity_sum(
            recreation_activity, domestic_activity,
            transport_activity, education_activity))


def activity_sum(recreation_activity, domestic_activity,
                 transport_activity, education_activity):
    """
    to-report activity-sum
      report sum map minus-half (list recreation-activity domestic-activity
                                     transport-activity education-activity)
    end

    to-report minus-half [x]
      report x - 0.5
    end
    """
    return ((recreation_activity - 0.5)
            + (domestic_activity - 0.5)
            + (transport_activity - 0.5)
            + (education_activity - 0.5))


def calculate_mass(mass, input, total_output, gamma_1):
    """
    to-report calculate-mass ;; turtle procedure
      report mass + mass-delta * gamma1
    end
    """
    return mass + mass_delta(input, total_output) * gamma_1


def mass_delta(input, total_output):
    """
    to-report mass-delta ;; turtle procedure
      report sigmoid (input - total-output) - 0.5
    end
    """
    return sigmoid(input - total_output) - 0.5


def sigmoid(t):
    """
    to-report sigmoid [t]
      report 1 / (1 + exp (-1 * t))
    end
    """
    return 1. / (1. + np.exp(-1. * t))


def calculate_input(total_output, force_of_habit, gamma_2,
                    friend_input, gamma_3,
                    c_control, gamma_4, sigma_1):
    """
    original netlogo:

    to-report calculate-input ;; turtle-procedure
      report total-output + force-of-habit * gamma2 + friend-input * gamma3
                          - c-control * gamma4 + random-normal 0 sigma1
    end
    """
    return (total_output
            + (force_of_habit * gamma_2)
            + (friend_input * gamma_3)
            + (c_control * gamma_4)
            + np.random.normal(0.0, sigma_1, total_output.shape))


def calculate_total_output(base_output, physical_activity, gamma_5,
                           friend_output, gamma_6, sigma_2):
    """
    original netlogo:

    to-report calculate-total-output ;; turtle procedure
      report base-output + physical-activity * gamma5 + friend-output * gamma6
             + random-normal 0 sigma2
    end
    """
    return (base_output
            + (physical_activity * gamma_5)
            + (friend_output * gamma_6)
            + np.random.normal(0.0, sigma_2, base_output.shape))
