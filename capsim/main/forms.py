from django import forms
import capsim.sim.defaults as defaults


class RunForm(forms.Form):
    ticks = forms.IntegerField(
        initial=100,
        label="How many ticks?",
        widget=forms.TextInput(attrs={'size': '4'}))
    number_agents = forms.IntegerField(
        initial=100,
        label="How many agents?",
        widget=forms.TextInput(attrs={'size': '4'}))
    gamma_1 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 1",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    gamma_2 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 2",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    gamma_3 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 3",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    gamma_4 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 4",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    gamma_5 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 5",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    gamma_6 = forms.FloatField(
        initial=defaults.DEFAULT_GAMMA,
        label="Gamma 6",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    sigma_1 = forms.FloatField(
        initial=defaults.SIGMA_1,
        label="Sigma 1",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    sigma_2 = forms.FloatField(
        initial=defaults.SIGMA_2,
        label="Sigma 2",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    agent_initial_mass_mean = forms.FloatField(
        initial=defaults.INITIAL_MASS_MEAN,
        label="Agent Initial Mass Mean",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    agent_initial_mass_sigma = forms.FloatField(
        initial=defaults.INITIAL_MASS_SIGMA,
        label="Agent Initial Mass Sigma",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    agent_base_output_mean = forms.FloatField(
        initial=defaults.BASE_OUTPUT_MEAN,
        label="Agent Base Output Mean",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    agent_base_output_sigma = forms.FloatField(
        initial=defaults.BASE_OUTPUT_SIGMA,
        label="Agent Base Output Sigma",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    recreation_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Recreation Activity Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    recreation_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Recreation Activity Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    domestic_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Domestic Activity Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    domestic_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Domestic Activity Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    transport_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Transport Activity Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    transport_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Transport Activity Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    education_activity_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Education Activity Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    education_activity_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Education Activity Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_exposure_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Exposure Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_exposure_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Exposure Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    energy_density_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Energy Density Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    energy_density_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Energy Density Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_advertising_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Advertising Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_advertising_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Advertising Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_convenience_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Convenience Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_convenience_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Convenience Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_literacy_alpha = forms.FloatField(
        initial=defaults.DEFAULT_ALPHA,
        label="Food Literacy Alpha",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_literacy_lambda = forms.FloatField(
        initial=defaults.DEFAULT_LAMBDA,
        label="Food Literacy Lambda",
        widget=forms.TextInput(attrs={'size': '4'}),
        )

    # physical environment weights
    recreation_activity_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Recreation Activity Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    domestic_activity_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Domestic Activity Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    transport_activity_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Transport Activity Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    education_activity_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Education Activity Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )

    # food environment weights
    energy_density_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Energy Density Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_exposure_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Food Exposure Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_literacy_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Food Literacy Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_advertising_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Food Advertising Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    food_convenience_weight = forms.FloatField(
        initial=defaults.DEFAULT_WEIGHT,
        label="Food Convenience Weight",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
