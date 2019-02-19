import numpy as np
from capsim.sim import defaults


class NormalVarParams(object):
    """ parameters for a variable with a normal distribution """
    def __init__(self, mean, sigma):
        self.mean = float(mean)
        self.sigma = float(sigma)

    def generate(self, shape):
        return np.random.normal(self.mean, self.sigma, shape)


class GammaVarParams(object):
    """ parameters for a variable with a Gamma distribution """

    # remember, 'lambda' is a keyword in python, so we'll use
    # 'llambda' instead. I think it's closely related to an alphaca.
    def __init__(self, alpha, llambda):
        self.alpha = float(alpha)
        self.llambda = float(llambda)

    def generate(self, shape):
        return np.random.gamma(self.alpha, self.llambda, shape)


class SimParamSet(object):
    """ bundle up the parameters that specify a simulation """
    def __init__(self, **kwargs):
        """
        Initialize a ParameterSet
        """
        self.number_agents = int(kwargs.get('number_agents',
                                            defaults.NUM_AGENTS))
        self.grid_size = int(kwargs.get('grid_size', defaults.GRID_SIZE))
        assert self.grid_size > 0

        self.gamma_1 = float(kwargs.get('gamma_1', defaults.DEFAULT_GAMMA))
        self.gamma_2 = float(kwargs.get('gamma_2', defaults.DEFAULT_GAMMA))
        self.gamma_3 = float(kwargs.get('gamma_3', defaults.DEFAULT_GAMMA))
        self.gamma_4 = float(kwargs.get('gamma_4', defaults.DEFAULT_GAMMA))
        self.gamma_5 = float(kwargs.get('gamma_5', defaults.DEFAULT_GAMMA))
        self.gamma_6 = float(kwargs.get('gamma_6', defaults.DEFAULT_GAMMA))

        self.sigma_1 = float(kwargs.get('sigma_1', defaults.SIGMA_1))
        self.sigma_2 = float(kwargs.get('sigma_2', defaults.SIGMA_2))

        self.agent_initial_mass = NormalVarParams(
            kwargs.get('agent_initial_mass_mean', defaults.INITIAL_MASS_MEAN),
            kwargs.get('agent_initial_mass_sigma',
                       defaults.INITIAL_MASS_SIGMA))
        self.agent_base_output = NormalVarParams(
            kwargs.get('agent_base_output_mean', defaults.BASE_OUTPUT_MEAN),
            kwargs.get('agent_base_output_sigma', defaults.BASE_OUTPUT_SIGMA))

        self.recreation_activity = GammaVarParams(
            kwargs.get('recreation_activity_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('recreation_activity_lambda', defaults.DEFAULT_LAMBDA))
        self.domestic_activity = GammaVarParams(
            kwargs.get('domestic_activity_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('domestic_activity_lambda', defaults.DEFAULT_LAMBDA))
        self.transport_activity = GammaVarParams(
            kwargs.get('transport_activity_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('transport_activity_lambda', defaults.DEFAULT_LAMBDA))
        self.education_activity = GammaVarParams(
            kwargs.get('education_activity_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('education_activity_lambda', defaults.DEFAULT_LAMBDA))

        self.recreation_activity_weight = kwargs.get(
            'recreation_activity_weight',
            defaults.DEFAULT_WEIGHT)
        self.domestic_activity_weight = kwargs.get('domestic_activity_weight',
                                                   defaults.DEFAULT_WEIGHT)
        self.transport_activity_weight = kwargs.get(
            'transport_activity_weight',
            defaults.DEFAULT_WEIGHT)
        self.education_activity_weight = kwargs.get(
            'education_activity_weight',
            defaults.DEFAULT_WEIGHT)

        self.food_exposure = GammaVarParams(
            kwargs.get('food_exposure_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('food_exposure_lambda', defaults.DEFAULT_LAMBDA))
        self.energy_density = GammaVarParams(
            kwargs.get('food_energy_density_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('food_energy_density_lambda', defaults.DEFAULT_LAMBDA))
        self.food_advertising = GammaVarParams(
            kwargs.get('food_advertising_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('food_advertising_lambda', defaults.DEFAULT_LAMBDA))
        self.food_convenience = GammaVarParams(
            kwargs.get('food_convenience_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('food_convenience_lambda', defaults.DEFAULT_LAMBDA))
        self.food_literacy = GammaVarParams(
            kwargs.get('food_literacy_alpha', defaults.DEFAULT_ALPHA),
            kwargs.get('food_literacy_lambda', defaults.DEFAULT_LAMBDA))

        self.food_exposure_weight = kwargs.get('food_exposure_weight',
                                               defaults.DEFAULT_WEIGHT)
        self.energy_density_weight = kwargs.get('energy_density_weight',
                                                defaults.DEFAULT_WEIGHT)
        self.food_advertising_weight = kwargs.get('food_advertising_weight',
                                                  defaults.DEFAULT_WEIGHT)
        self.food_convenience_weight = kwargs.get('food_convenience_weight',
                                                  defaults.DEFAULT_WEIGHT)
        self.food_literacy_weight = kwargs.get('food_literacy_weight',
                                               defaults.DEFAULT_WEIGHT)

    def to_dict(self):
        """ return a simple dict of all the parameters """
        return dict(
            number_agents=self.number_agents,
            grid_size=self.grid_size,
            gamma_1=self.gamma_1,
            gamma_2=self.gamma_2,
            gamma_3=self.gamma_3,
            gamma_4=self.gamma_4,
            gamma_5=self.gamma_5,
            gamma_6=self.gamma_6,
            sigma_1=self.sigma_1,
            sigma_2=self.sigma_2,
            agent_initial_mass_mean=self.agent_initial_mass.mean,
            agent_initial_mass_sigma=self.agent_initial_mass.sigma,
            agent_base_output_mean=self.agent_base_output.mean,
            agent_base_output_sigma=self.agent_base_output.mean,
            recreation_activity_alpha=self.recreation_activity.alpha,
            recreation_activity_lambda=self.recreation_activity.llambda,
            domestic_activity_alpha=self.domestic_activity.alpha,
            domestic_activity_lambda=self.domestic_activity.llambda,
            transport_activity_alpha=self.transport_activity.alpha,
            transport_activity_lambda=self.transport_activity.llambda,
            education_activity_alpha=self.education_activity.alpha,
            education_activity_lambda=self.education_activity.llambda,
            recreation_activity_weight=self.recreation_activity_weight,
            domestic_activity_weight=self.domestic_activity_weight,
            transport_activity_weight=self.transport_activity_weight,
            education_activity_weight=self.education_activity_weight,
            food_exposure_alpha=self.food_exposure.alpha,
            food_exposure_lambda=self.food_exposure.llambda,
            energy_density_alpha=self.energy_density.alpha,
            energy_density_lambda=self.energy_density.llambda,
            food_advertising_alpha=self.food_advertising.alpha,
            food_advertising_lambda=self.food_advertising.llambda,
            food_convenience_alpha=self.food_convenience.alpha,
            food_convenience_lambda=self.food_convenience.llambda,
            food_literacy_alpha=self.food_literacy.alpha,
            food_literacy_lambda=self.food_literacy.llambda,
            food_exposure_weight=self.food_exposure_weight,
            energy_density_weight=self.energy_density_weight,
            food_advertising_weight=self.food_advertising_weight,
            food_convenience_weight=self.food_convenience_weight,
            food_literacy_weight=self.food_literacy_weight,
        )
