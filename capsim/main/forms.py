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
