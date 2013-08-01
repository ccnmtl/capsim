import numpy as np


class NormalVarParams(object):
    """ parameters for a variable with a normal distribution """
    def __init__(self, mean, sigma):
        self.mean = mean
        self.sigma = sigma

    def generate(self, shape):
        return np.random.normal(self.mean, self.sigma, shape)


class GammaVarParams(object):
    """ parameters for a variable with a Gamma distribution """

    # remember, 'lambda' is a keyword in python, so we'll use
    # 'llambda' instead. I think it's closely related to an alphaca.
    def __init__(self, alpha, llambda):
        self.alpha = alpha
        self.llambda = llambda

    def generate(self, shape):
        return np.random.gamma(self.alpha, self.llambda, shape)


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
        self.number_agents = kwargs.get('number_agents', 4)
        assert type(self.number_agents) == int
        self.grid_size = kwargs.get('grid_size', 1)
        assert type(self.grid_size) == int
        assert self.grid_size > 0

        self.gamma_1 = kwargs.get('gamma_1', 1.)
        self.gamma_2 = kwargs.get('gamma_2', 1.)
        self.gamma_3 = kwargs.get('gamma_3', 1.)
        self.gamma_4 = kwargs.get('gamma_4', 1.)
        self.gamma_5 = kwargs.get('gamma_5', 1.)
        self.gamma_6 = kwargs.get('gamma_6', 1.)

        self.sigma_1 = kwargs.get('sigma_1', 6.2)
        self.sigma_2 = kwargs.get('sigma_2', 5.)

        self.agent_initial_mass = NormalVarParams(
            kwargs.get('agent_initial_mass_mean', 100.),
            kwargs.get('agent_initial_mass_sigma', 20.))
        self.agent_base_output = NormalVarParams(
            kwargs.get('agent_base_output_mean', 100.),
            kwargs.get('agent_base_output_sigma', 5.))

        self.recreation_activity = GammaVarParams(
            kwargs.get('recreation_activity_alpha', 0.5),
            kwargs.get('recreation_activity_lambda', 0.1))
        self.domestic_activity = GammaVarParams(
            kwargs.get('domestic_activity_alpha', 0.5),
            kwargs.get('domestic_activity_lambda', 0.1))
        self.transport_activity = GammaVarParams(
            kwargs.get('transport_activity_alpha', 0.5),
            kwargs.get('transport_activity_lambda', 0.1))
        self.education_activity = GammaVarParams(
            kwargs.get('education_activity_alpha', 0.5),
            kwargs.get('education_activity_lambda', 0.1))

        self.food_exposure = GammaVarParams(
            kwargs.get('food_exposure_alpha', 0.5),
            kwargs.get('food_exposure_lambda', 0.1))
        self.energy_density = GammaVarParams(
            kwargs.get('food_energy_density_alpha', 0.5),
            kwargs.get('food_energy_density_lambda', 0.1))
        self.food_advertising = GammaVarParams(
            kwargs.get('food_advertising_alpha', 0.5),
            kwargs.get('food_advertising_lambda', 0.1))
        self.food_convenience = GammaVarParams(
            kwargs.get('food_convenience_alpha', 0.5),
            kwargs.get('food_convenience_lambda', 0.1))
        self.food_literacy = GammaVarParams(
            kwargs.get('food_literacy_alpha', 0.5),
            kwargs.get('food_literacy_lambda', 0.1))
