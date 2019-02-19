from django import forms
import capsim.sim.defaults as defaults

INT_FIELDS = ['ticks', 'number_agents']

FLOAT_FIELDS = [
    'gamma_1', 'gamma_2',
    'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6',
    'sigma_1', 'sigma_2',
    'agent_initial_mass_mean', 'agent_initial_mass_sigma',
    'agent_base_output_mean', 'agent_base_output_sigma',
    'recreation_activity_alpha',
    'recreation_activity_lambda',
    'domestic_activity_alpha',
    'domestic_activity_lambda',
    'transport_activity_alpha',
    'transport_activity_lambda',
    'education_activity_alpha',
    'education_activity_lambda',

    'recreation_activity_weight',
    'domestic_activity_weight',
    'transport_activity_weight',
    'education_activity_weight',

    'food_exposure_alpha',
    'food_exposure_lambda',
    'energy_density_alpha',
    'energy_density_lambda',
    'food_advertising_alpha',
    'food_advertising_lambda',
    'food_convenience_alpha',
    'food_convenience_lambda',
    'food_literacy_alpha',
    'food_literacy_lambda',

    'food_exposure_weight',
    'energy_density_weight',
    'food_advertising_weight',
    'food_convenience_weight',
    'food_literacy_weight',
]

ALL_FIELDS = INT_FIELDS + FLOAT_FIELDS


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


class ExperimentForm(forms.Form):
    title = forms.CharField(
        initial="a name for the experiment",
        label="Experiment Title",
        required=False,
        )

    independent_variable = forms.ChoiceField(
        initial="gamma_1",
        choices=list(zip(FLOAT_FIELDS, FLOAT_FIELDS)),
        label="Independent Variable",
        )
    independent_min = forms.FloatField(
        initial=0.0,
        label="Independent Variable Minimum",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    independent_max = forms.FloatField(
        initial=1.0,
        label="Independent Variable Maximum",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    independent_steps = forms.IntegerField(
        initial=1,
        label="Independent Variable Number of Steps",
        widget=forms.TextInput(attrs={'size': '4'}),
        )

    dependent_variable = forms.ChoiceField(
        initial="gamma_2",
        choices=list(zip(FLOAT_FIELDS, FLOAT_FIELDS)),
        label="Dependent Variable",
        )
    dependent_min = forms.FloatField(
        initial=0.0,
        label="Dependent Variable Minimum",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    dependent_max = forms.FloatField(
        initial=1.0,
        label="Dependent Variable Maximum",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
    dependent_steps = forms.IntegerField(
        initial=1,
        label="Dependent Variable Number of Steps",
        widget=forms.TextInput(attrs={'size': '4'}),
        )

    trials = forms.IntegerField(
        initial=1,
        label="Number of Trials",
        widget=forms.TextInput(attrs={'size': '4'}),
        )
