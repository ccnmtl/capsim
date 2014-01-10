from django import forms
import capsim.sim.defaults as defaults


class RunForm(forms.Form):
    ticks = forms.IntegerField(
        initial=100,
        label="How many ticks?")
    number_agents = forms.IntegerField(
        initial=100,
        label="How many agents?")
    gamma_1 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 1",
        )
    gamma_2 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 2",
        )
    gamma_3 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 3",
        )
    gamma_4 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 4",
        )
    gamma_5 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 5",
        )
    gamma_6 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 6",
        )
    sigma_1 = forms.FloatField(
        initial=defaults.SIGMA_1,
        label="Sigma 1",
        )
    sigma_2 = forms.FloatField(
        initial=defaults.SIGMA_2,
        label="Sigma 2",
        )
    agent_initial_mass_mean = forms.FloatField(
        initial=defaults.INITIAL_MASS_MEAN,
        label="Agent Initial Mass Mean",
        )
    agent_initial_mass_sigma = forms.FloatField(
        initial=defaults.INITIAL_MASS_SIGMA,
        label="Agent Initial Mass Sigma",
        )
    agent_base_output_mean = forms.FloatField(
        initial=defaults.BASE_OUTPUT_MEAN,
        label="Agent Base Output Mean",
        )
    agent_base_output_sigma = forms.FloatField(
        initial=defaults.BASE_OUTPUT_SIGMA,
        label="Agent Base Output Sigma",
        )
    recreation_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Recreation Activity Alpha",
        )
    recreation_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Recreation Activity Lambda",
        )
    domestic_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Domestic Activity Alpha",
        )
    domestic_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Domestic Activity Lambda",
        )
    transport_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Transport Activity Alpha",
        )
    transport_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Transport Activity Lambda",
        )
    education_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Education Activity Alpha",
        )
    education_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Education Activity Lambda",
        )
    food_exposure_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Exposure Alpha",
        )
    food_exposure_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Exposure Lambda",
        )
    energy_density_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Energy Density Alpha",
        )
    energy_density_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Energy Density Lambda",
        )
    food_advertising_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Advertising Alpha",
        )
    food_advertising_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Advertising Lambda",
        )
    food_convenience_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Convenience Alpha",
        )
    food_convenience_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Convenience Lambda",
        )
    food_literacy_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Literacy Alpha",
        )
    food_literacy_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Literacy Lambda",
        )
