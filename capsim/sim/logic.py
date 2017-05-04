import numpy as np
import networkx as nx
import pandas as pd
from .paramset import SimParamSet


# some constants (probably want to turn these into parameters eventually)
NUM_NEIGHBORS = 3

# keep track of the version of the simulation model that is running
# update this string each time a change is made to the simulation logic
# (but not to other app infrastructure bits). It gets serialized
# with run parameters and outputs. This lets us connect data from
# runs back to the exact version of the code that ran it. Later on
# we can, eg, find runs that happened with code that had a bug that was
# found later and flag that data as suspicious.

# please keep it in the NNN-YYYY-MM-DD format, incrementing the number
# on the front each time, and setting the other fields to the current date

MODEL_VERSION = "002-2014-03-12"


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
        # a fixed number of neighbors. will want to add more controls
        # here later.
        self.neighbors = nx.random_regular_graph(NUM_NEIGHBORS, n + (n % 2))

    def to_dict(self):
        """ expose a simple dict version of the state of the simulation

        this should enable serialization and extracting the history
        of the whole simulation run """
        return dict(
            params=self.params.to_dict(),
            ticks=self.ticks,
            # agent arrays
            agents_mass=self.agents_mass,
            agents_base_output=self.agents_base_output,
            agents_row=self.agents_row,
            agents_col=self.agents_col,
            input=self.input,
            total_output=self.total_output,
            force_of_habit=self.force_of_habit,
            c_control=self.c_control,
            physical_activity=self.physical_activity,
            friend_input=self.friend_input,
            friend_output=self.friend_output,
            # neighbor graph
            neighbors=self.neighbors,
            # environment/patches
            recreation_activity=self.recreation_activity,
            domestic_activity=self.domestic_activity,
            transport_activity=self.transport_activity,
            education_activity=self.education_activity,
            food_exposure=self.food_exposure,
            energy_density=self.energy_density,
            food_advertising=self.food_advertising,
            food_convenience=self.food_convenience,
            food_literacy=self.food_literacy,
            MODEL_VERSION=MODEL_VERSION,
        )

    def from_dict(self, d):
        """ set our state from a dict

        we're expecting this to come from to_dict(), so there
        is no attempt at validating that the input dict
        has the keys we expect.
        """
        self.params = SimParamSet(**d['params'])
        self.ticks = d['ticks']
        # agent arrays
        self.agents_mass = d['agents_mass']
        self.agents_base_output = d['agents_base_output']
        self.agents_row = d['agents_row']
        self.agents_col = d['agents_col']
        self.input = d['input']
        self.total_output = d['total_output']
        self.force_of_habit = d['force_of_habit']
        self.c_control = d['c_control']
        self.physical_activity = d['physical_activity']
        self.friend_input = d['friend_input']
        self.friend_output = d['friend_output']
        # neighbor graph
        self.neighbors = d['neighbors']
        # environment/patches
        self.recreation_activity = d['recreation_activity']
        self.domestic_activity = d['domestic_activity']
        self.transport_activity = d['transport_activity']
        self.education_activity = d['education_activity']
        self.food_exposure = d['food_exposure']
        self.energy_density = d['energy_density']
        self.food_advertising = d['food_advertising']
        self.food_convenience = d['food_convenience']
        self.food_literacy = d['food_literacy']
        # the dict ought to also have a MODEL_VERSION entry
        # that we can compare to our current version
        # for now, we don't have any actual use for it
        # but it will help us manage backwards compatability
        # later.

    def tick(self):
        """ each tick of the clock
        * calculate-total-output
        * calculate-input
        * set mass calculate-mass
        * move if starving (TODO)
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

        # some circular stuff here. need to re-think
        self.friend_input = calculate_friend_input(self.input, self.neighbors)
        self.friend_output = calculate_friend_output(
            self.total_output, self.neighbors)

        self.physical_activity = calculate_physical_activity(
            recreation, domestic, transport, education,
            self.params.recreation_activity_weight,
            self.params.domestic_activity_weight,
            self.params.transport_activity_weight,
            self.params.education_activity_weight)

        self.total_output = calculate_total_output(
            self.agents_base_output,
            self.physical_activity, self.params.gamma_5,
            self.friend_output, self.params.gamma_6,
            self.params.sigma_2)

        self.force_of_habit = calculate_force_of_habit(
            food_exposure, energy_density,
            food_advertising, food_convenience,
            self.params.food_exposure_weight,
            self.params.energy_density_weight,
            self.params.food_advertising_weight,
            self.params.food_convenience_weight)

        self.c_control = calculate_c_control(
            food_literacy, self.params.food_literacy_weight)

        self.input = calculate_input(
            self.total_output,
            self.force_of_habit, self.params.gamma_2,
            self.friend_input, self.params.gamma_3,
            self.c_control, self.params.gamma_4,
            self.params.sigma_1)

        self.agents_mass = calculate_mass(
            self.agents_mass, self.input,
            self.total_output, self.params.gamma_1)


def calculate_friend_input(input, neighbors):
    """
    to-report friend-input ;; turtle-procedure
      report sigmoid (10 * (network-input-percent - 0.5)) - 0.5
    end
    """
    return sigmoid(10. * (network_input_percent(input, neighbors) - 0.5)) - 0.5


def network_input_percent(input, neighbors):
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
    return (count_neighbors_greater(neighbors, input) /
            np.maximum(count_neighbors(neighbors), 1.))


def count_neighbors_greater(neighbors, a):
    """ returns count of neighbors that are >= than each agent in array a """
    out = np.zeros(a.shape)
    for i in range(len(a)):
        out[i] = len(np.where(a[[neighbors.neighbors(i)]] >= a[i])[0])
    return out


def count_neighbors(neighbors):
    """ takes a nx.Graph and returns list np.array of # neighbors
    basically, the degrees of each """
    dlist = np.array(list(neighbors.degree_iter()))
    return dlist.T[1]


def calculate_friend_output(output, neighbors):
    """
    to-report friend-output
      report sigmoid (10 * (network-output-percent - 0.50)) - 0.50
    end
    """
    return (sigmoid(10. * (network_output_percent(output, neighbors) - 0.5)) -
            0.5)


def network_output_percent(output, neighbors):
    """
    to-report network-output-percent ;; turtle procedure
      let my-output total-output
      ifelse empty? [total-output] of link-neighbors
      [report 0.0]
      [report (count link-neighbors with [total-output >= my-output])
               / (count link-neighbors)]
    end
    """
    return (count_neighbors_greater(neighbors, output) /
            np.maximum(count_neighbors(neighbors), 1.))


def calculate_c_control(food_literacy, food_literacy_weight=1.):
    return sigmoid(10. * ((food_literacy * food_literacy_weight) - 0.5))


def calculate_force_of_habit(food_exposure, energy_density,
                             food_advertising, food_convenience,
                             food_exposure_weight=1.,
                             energy_density_weight=1.,
                             food_advertising_weight=1.,
                             food_convenience_weight=1.):
    return sigmoid(
        10. * food_sum(
            food_exposure, energy_density, food_advertising, food_convenience,
            food_exposure_weight, energy_density_weight,
            food_advertising_weight, food_convenience_weight))


def food_sum(food_exposure, energy_density,
             food_advertising, food_convenience,
             food_exposure_weight=1., energy_density_weight=1.,
             food_advertising_weight=1., food_convenience_weight=1.):
    return (((food_exposure * food_exposure_weight) - 0.5) +
            ((energy_density * energy_density_weight) - 0.5) +
            ((food_advertising * food_advertising_weight) - 0.5) +
            ((food_convenience * food_convenience_weight) - 0.5))


def calculate_physical_activity(recreation_activity, domestic_activity,
                                transport_activity, education_activity,
                                recreation_activity_weight=1.,
                                domestic_activity_weight=1.,
                                transport_activity_weight=1.,
                                education_activity_weight=1.):
    return sigmoid(
        10. * activity_sum(
            recreation_activity, domestic_activity,
            transport_activity, education_activity,
            recreation_activity_weight, domestic_activity_weight,
            transport_activity_weight, education_activity_weight))


def activity_sum(recreation_activity, domestic_activity,
                 transport_activity, education_activity,
                 recreation_activity_weight=1.,
                 domestic_activity_weight=1.,
                 transport_activity_weight=1.,
                 education_activity_weight=1.):
    return (((recreation_activity * recreation_activity_weight) - 0.5) +
            ((domestic_activity * domestic_activity_weight) - 0.5) +
            ((transport_activity * transport_activity_weight) - 0.5) +
            ((education_activity * education_activity_weight) - 0.5))


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
    to-report calculate-input ;; turtle-procedure
      report total-output + force-of-habit * gamma2 + friend-input * gamma3
                          - c-control * gamma4 + random-normal 0 sigma1
    end
    """
    return (total_output +
            (force_of_habit * gamma_2) +
            (friend_input * gamma_3) -
            (c_control * gamma_4) +
            np.random.normal(0.0, sigma_1, total_output.shape))


def calculate_total_output(base_output, physical_activity, gamma_5,
                           friend_output, gamma_6, sigma_2):
    """
    to-report calculate-total-output ;; turtle procedure
      report base-output + physical-activity * gamma5 + friend-output * gamma6
             + random-normal 0 sigma2
    end
    """
    return (base_output +
            (physical_activity * gamma_5) +
            (friend_output * gamma_6) +
            np.random.normal(0.0, sigma_2, base_output.shape))


class RunOutput(object):
    def __init__(self, ticks, params, data):
        self.ticks = ticks
        self.params = params
        self.data = pd.DataFrame(data).sort_values(by=['tick'])

    def to_dict(self):
        return dict(
            ticks=self.ticks,
            data=self.data.to_json(),
        )

    def display_data(self):
        ticks = self.ticks
        number_agents = self.params.get('number_agents', 100)
        output = self.data
        mass_stats = [dict(mean=np.array(d).mean(), std=np.array(d).std())
                      for d in output.agents_mass]
        intake_stats = [dict(mean=np.array(d).mean(), std=np.array(d).std())
                        for d in output.intake]
        expenditure_stats = [dict(mean=np.array(d).mean(),
                                  std=np.array(d).std())
                             for d in output.expenditure]
        return dict(
            number_agents=number_agents,
            ticks=ticks,
            output=output,
            mass_stats=mass_stats,
            intake_stats=intake_stats,
            expenditure_stats=expenditure_stats,
            mass_mean=np.array(output.agents_mass[ticks-1]).mean(),
            mass_stddev=np.array(output.agents_mass[ticks-1]).std(),
            intake_mean=np.array(output.intake[ticks-1]).mean(),
            intake_stddev=np.array(output.intake[ticks-1]).std(),
            expenditure_mean=np.array(output.expenditure[ticks-1]).mean(),
            expenditure_stddev=np.array(output.expenditure[ticks-1]).std())


class Run(object):
    def __init__(self, **kwargs):
        self.ticks = kwargs.get('ticks', 100)
        self.params = kwargs

    def run(self):
        results = []
        s = Simulation(**self.params)
        for tick in range(self.ticks):
            s.tick()
            results.append(
                dict(
                    agents_mass=s.agents_mass,
                    intake=s.input,
                    expenditure=s.total_output,
                    tick=tick,
                )
            )
        return RunOutput(ticks=self.ticks, params=self.params, data=results)

    def to_dict(self):
        return self.params

    @classmethod
    def from_dict(self, d):
        return Run(**d)
