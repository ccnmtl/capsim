import numpy as np


class NormalVarParams(object):
    """ parameters for a variable with a normal distribution """
    def __init__(self, mean, sigma):
        self.mean = mean
        self.sigma = sigma


class GammaVarParams(object):
    """ parameters for a variable with a Gamma distribution """

    # remember, 'lambda' is a keyword in python, so we'll use
    # 'llambda' instead. I think it's closely related to an alphaca.
    def __init__(self, alpha, llambda):
        self.alpha = alpha
        self.llambda = llambda


class SimParamSet(object):
    """ bundle up the parameters that specify a simulation """
    def __init__(self, **kwargs):
        """
        Initialize a ParameterSet

        The original logo parameters:

        number-nodes
        agent-initial-mass-mean agent-initial-mass-sigma
        base-output-mean base-output-sigma

        recreation-activity-alpha recreation-activity-lambda
        domestic-activity-alpha domestic-activity-lambda
        transport-activity-alpha transport-activity-lambda
        education-activity-alpha education-activity-lambda

        food-exposure-alpha food-exposure-lambda
        food-energy-density-alpha food-energy-density-lambda
        food-advertising-alpha food-advertising-lambda
        food-convenience-alpha food-convenience-lambda
        food-literacy-alpha food-literacy-lambda
        """
        self.number_agents = kwargs.get('number_agents', 1)
        assert type(self.number_agents) == int
        self.grid_size = kwargs.get('grid_size', 1)
        assert type(self.grid_size) == int
        assert self.grid_size > 0

        self.agent_initial_mass = NormalVarParams(
            kwargs.get('agent_initial_mass_mean', 100.),
            kwargs.get('agent_initial_mass_sigma', 20.))
        self.agent_initial_mass = NormalVarParams(
            kwargs.get('agent_base_output_mean', 100.),
            kwargs.get('agent_base_output_sigma', 20.))

        self.recreation_activity = GammaVarParams(
            kwargs.get('recreation_activity_alpha', 1.),
            kwargs.get('recreation_activity_lambda', 1.))
        self.domestic_activity = GammaVarParams(
            kwargs.get('domestic_activity_alpha', 1.),
            kwargs.get('domestic_activity_lambda', 1.))
        self.transport_activity = GammaVarParams(
            kwargs.get('transport_activity_alpha', 1.),
            kwargs.get('transport_activity_lambda', 1.))
        self.education_activity = GammaVarParams(
            kwargs.get('education_activity_alpha', 1.),
            kwargs.get('education_activity_lambda', 1.))

        self.food_exposure = GammaVarParams(
            kwargs.get('food_exposure_alpha', 1.),
            kwargs.get('food_exposure_lambda', 1.))
        self.energy_density = GammaVarParams(
            kwargs.get('food_energy_density_alpha', 1.),
            kwargs.get('food_energy_density_lambda', 1.))
        self.food_advertising = GammaVarParams(
            kwargs.get('food_advertising_alpha', 1.),
            kwargs.get('food_advertising_lambda', 1.))
        self.food_convenience = GammaVarParams(
            kwargs.get('food_convenience_alpha', 1.),
            kwargs.get('food_convenience_lambda', 1.))
        self.food_literacy = GammaVarParams(
            kwargs.get('food_literacy_alpha', 1.),
            kwargs.get('food_literacy_lambda', 1.))


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
