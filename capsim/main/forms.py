from django import forms

DEFAULT_GAMMA = 1.
INITIAL_MASS_MEAN = 100.
INITIAL_MASS_SIGMA = 20.
BASE_OUTPUT_MEAN = 100.
BASE_OUTPUT_SIGMA = 5.
SIGMA_1 = 6.2
SIGMA_2 = 5.
DEFAULT_ALPHA = 0.5
DEFAULT_LAMBDA = 0.1


class RunForm(forms.Form):
    ticks = forms.IntegerField(
        initial=100,
        label="How many ticks?")
    number_agents = forms.IntegerField(
        initial=100,
        label="How many agents?")
    gamma_1 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 1",
        )
    gamma_2 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 2",
        )
    gamma_3 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 3",
        )
    gamma_4 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 4",
        )
    gamma_5 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 5",
        )
    gamma_6 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 6",
        )
    sigma_1 = forms.FloatField(
        initial=SIGMA_1,
        label="Sigma 1",
        )
    sigma_2 = forms.FloatField(
        initial=SIGMA_2,
        label="Sigma 2",
        )
    agent_initial_mass_mean = forms.FloatField(
        initial=INITIAL_MASS_MEAN,
        label="Agent Initial Mass Mean",
        )
    agent_initial_mass_sigma = forms.FloatField(
        initial=INITIAL_MASS_SIGMA,
        label="Agent Initial Mass Sigma",
        )
    agent_base_output_mean = forms.FloatField(
        initial=BASE_OUTPUT_MEAN,
        label="Agent Base Output Mean",
        )
    agent_base_output_sigma = forms.FloatField(
        initial=BASE_OUTPUT_SIGMA,
        label="Agent Base Output Sigma",
        )
            # recreation_activity_alpha=self.recreation_activity.alpha,
            # recreation_activity_lambda=self.recreation_activity.llambda,
            # domestic_activity_alpha=self.domestic_activity.alpha,
            # domestic_activity_lambda=self.domestic_activity.llambda,
            # transport_activity_alpha=self.transport_activity.alpha,
            # transport_activity_lambda=self.transport_activity.llambda,
            # education_activity_alpha=self.education_activity.alpha,
            # education_activity_lambda=self.education_activity.llambda,
            # food_exposure_alpha=self.food_exposure.alpha,
            # food_exposure_lambda=self.food_exposure.llambda,
            # energy_density_alpha=self.energy_density.alpha,
            # energy_density_lambda=self.energy_density.llambda,
            # food_advertising_alpha=self.food_advertising.alpha,
            # food_advertising_lambda=self.food_advertising.llambda,
            # food_convenience_alpha=self.food_convenience.alpha,
            # food_convenience_lambda=self.food_convenience.llambda,
            # food_literacy_alpha=self.food_literacy.alpha,
            # food_literacy_lambda=self.food_literacy.llambda,
