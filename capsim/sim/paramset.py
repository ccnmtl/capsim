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


# let's make some constants for defaults
NUM_AGENTS = 4
GRID_SIZE = 1
DEFAULT_GAMMA = 1.
INITIAL_MASS_MEAN = 100.
INITIAL_MASS_SIGMA = 20.
BASE_OUTPUT_MEAN = 100.
BASE_OUTPUT_SIGMA = 5.
SIGMA_1 = 6.2
SIGMA_2 = 5.
DEFAULT_ALPHA = 0.5
DEFAULT_LAMBDA = 0.1


class SimParamSet(object):
    """ bundle up the parameters that specify a simulation """
    def __init__(self, **kwargs):
        """
        Initialize a ParameterSet
        """
        self.number_agents = kwargs.get('number_agents', NUM_AGENTS)
        assert type(self.number_agents) == int
        self.grid_size = kwargs.get('grid_size', GRID_SIZE)
        assert type(self.grid_size) == int
        assert self.grid_size > 0

        self.gamma_1 = kwargs.get('gamma_1', DEFAULT_GAMMA)
        self.gamma_2 = kwargs.get('gamma_2', DEFAULT_GAMMA)
        self.gamma_3 = kwargs.get('gamma_3', DEFAULT_GAMMA)
        self.gamma_4 = kwargs.get('gamma_4', DEFAULT_GAMMA)
        self.gamma_5 = kwargs.get('gamma_5', DEFAULT_GAMMA)
        self.gamma_6 = kwargs.get('gamma_6', DEFAULT_GAMMA)

        self.sigma_1 = kwargs.get('sigma_1', SIGMA_1)
        self.sigma_2 = kwargs.get('sigma_2', SIGMA_2)

        self.agent_initial_mass = NormalVarParams(
            kwargs.get('agent_initial_mass_mean', INITIAL_MASS_MEAN),
            kwargs.get('agent_initial_mass_sigma', INITIAL_MASS_SIGMA))
        self.agent_base_output = NormalVarParams(
            kwargs.get('agent_base_output_mean', BASE_OUTPUT_MEAN),
            kwargs.get('agent_base_output_sigma', BASE_OUTPUT_SIGMA))

        self.recreation_activity = GammaVarParams(
            kwargs.get('recreation_activity_alpha', DEFAULT_ALPHA),
            kwargs.get('recreation_activity_lambda', DEFAULT_LAMBDA))
        self.domestic_activity = GammaVarParams(
            kwargs.get('domestic_activity_alpha', DEFAULT_ALPHA),
            kwargs.get('domestic_activity_lambda', DEFAULT_LAMBDA))
        self.transport_activity = GammaVarParams(
            kwargs.get('transport_activity_alpha', DEFAULT_ALPHA),
            kwargs.get('transport_activity_lambda', DEFAULT_LAMBDA))
        self.education_activity = GammaVarParams(
            kwargs.get('education_activity_alpha', DEFAULT_ALPHA),
            kwargs.get('education_activity_lambda', DEFAULT_LAMBDA))

        self.food_exposure = GammaVarParams(
            kwargs.get('food_exposure_alpha', DEFAULT_ALPHA),
            kwargs.get('food_exposure_lambda', DEFAULT_LAMBDA))
        self.energy_density = GammaVarParams(
            kwargs.get('food_energy_density_alpha', DEFAULT_ALPHA),
            kwargs.get('food_energy_density_lambda', DEFAULT_LAMBDA))
        self.food_advertising = GammaVarParams(
            kwargs.get('food_advertising_alpha', DEFAULT_ALPHA),
            kwargs.get('food_advertising_lambda', DEFAULT_LAMBDA))
        self.food_convenience = GammaVarParams(
            kwargs.get('food_convenience_alpha', DEFAULT_ALPHA),
            kwargs.get('food_convenience_lambda', DEFAULT_LAMBDA))
        self.food_literacy = GammaVarParams(
            kwargs.get('food_literacy_alpha', DEFAULT_ALPHA),
            kwargs.get('food_literacy_lambda', DEFAULT_LAMBDA))
