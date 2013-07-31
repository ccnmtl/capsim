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
        self.neighbors = np.zeros(n * n).reshape((n, n))
        # fill it in

    def tick(self):
        """ each tick of the clock
        * calculate-total-output
        * calculate-input
        * set mass calculate-mass
        * move if starving
        """
        self.ticks += 1

        self.total_output = calculate_total_output(
            self.agents_base_output,
            self.physical_activity, self.params.gamma_5,
            self.friend_output, self.params.gamma_6,
            self.params.sigma_2)

        self.input = calculate_input(
            self.total_output,
            self.force_of_habit, self.params.gamma_2,
            self.friend_input, self.params.gamma_3,
            self.c_control, self.params.gamma_4,
            self.params.sigma_1)

        self.agents_mass = calculate_mass(
            self.agents_mass, self.input,
            self.total_output, self.params.gamma_1)


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
